from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, current_app, session
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message, Mail
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from flask_login import LoginManager
import logging
import sys
import bcrypt
from functools import wraps
from models import User, Aircraft, Instructor, Booking
from extensions import db, login_manager, mail, migrate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger('__main__')

# Ensure logger captures all messages
logger.setLevel(logging.INFO)

load_dotenv()

app = Flask(__name__)

# Set testing mode
app.config['TESTING'] = os.getenv('TESTING', 'False').lower() == 'true'

# Basic configuration
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key-please-change-in-production'),
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/flight_school'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SESSION_TYPE='filesystem',
    MAIL_SERVER=os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_USERNAME'),
    MAIL_SUPPRESS_SEND=app.config.get('TESTING', False),
    BASE_URL=os.getenv('BASE_URL', 'http://localhost:5001')
)

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protect against CSRF

# Initialize extensions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'
mail = Mail(app)

# Initialize database
with app.app_context():
    init_db()

@login_manager.user_loader
def load_user(user_id):
    logger.debug(f"Loading user with ID: {user_id}")
    return User.get_by_id(int(user_id))

def check_session_timeout():
    if current_user.is_authenticated:
        last_active = session.get('last_active')
        if last_active:
            last_active = datetime.fromisoformat(last_active)
            if datetime.utcnow() - last_active > app.config['PERMANENT_SESSION_LIFETIME']:
                logout_user()
                session.clear()
                return True
    return False

@app.before_request
def before_request():
    if check_session_timeout():
        return redirect(url_for('login_page', message='Your session has expired. Please log in again.'))
    if current_user.is_authenticated:
        session['last_active'] = datetime.utcnow().isoformat()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You need administrator privileges to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        # Redirect admin users to admin dashboard, regular users to booking page
        return redirect(url_for('admin_dashboard') if current_user.is_admin else url_for('booking_page'))
    logger.debug("Rendering index page")
    return render_template('home.html', title='Welcome to Open Flight School')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get_by_email(email)
        if user and user.check_password(password):
            login_user(user)
            flash('Welcome back!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        if not all([username, email, password, password_confirm]):
            flash('All fields are required', 'error')
            return redirect(url_for('register_page'))
        
        if password != password_confirm:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register_page'))
        
        if User.get_by_email(email):
            flash('Email already registered', 'error')
            return redirect(url_for('register_page'))
        
        user = User.create(
            username=username,
            email=email,
            password=password
        )
        flash('Registration successful', 'success')
        return redirect(url_for('login_page'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.get_by_email(email):
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User.create(
        username=username,
        email=email,
        password=password
    )
    
    return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.get_by_email(email)
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    login_user(user)
    return jsonify({'message': 'Login successful', 'user_id': user.id}), 200

@app.route('/api/bookings', methods=['GET'])
@login_required
def get_bookings():
    bookings = Booking.get_by_user(current_user.id)
    return jsonify([booking.to_dict() for booking in bookings]), 200

@app.route('/api/bookings', methods=['POST'])
@login_required
def create_booking():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        start_time = datetime.fromisoformat(data.get('start_time'))
        end_time = datetime.fromisoformat(data.get('end_time'))
        aircraft_id = data.get('aircraft_id')
        instructor_id = data.get('instructor_id')
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid date format'}), 400
    
    if not all([start_time, end_time, aircraft_id, instructor_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if start_time >= end_time:
        return jsonify({'error': 'Start time must be before end time'}), 400
    
    if Booking.check_conflicts(start_time, end_time, aircraft_id, instructor_id):
        return jsonify({'error': 'Booking conflicts with existing booking'}), 409
    
    booking = Booking.create(
        start_time=start_time,
        end_time=end_time,
        user_id=current_user.id,
        aircraft_id=aircraft_id,
        instructor_id=instructor_id
    )
    
    return jsonify({'message': 'Booking created successfully', 'booking_id': booking.id}), 201

def send_reset_email(user, token):
    reset_url = url_for('reset_password', token=token, _external=True)
    msg = Message('Password Reset Request',
                 sender=app.config['MAIL_DEFAULT_SENDER'],
                 recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route('/api/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    user = User.get_by_email(email)
    if not user:
        return jsonify({'message': 'If an account exists with that email, a password reset link will be sent.'}), 200
    
    token = User.generate_reset_token(user.id)
    try:
        send_reset_email(user, token)
        return jsonify({'message': 'Password reset email sent'}), 200
    except Exception as e:
        logger.error(f'Failed to send reset email: {str(e)}')
        return jsonify({'error': 'Failed to send reset email'}), 500

@app.route('/api/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    password = data.get('password')
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    user = User.verify_reset_token(token)
    if not user:
        return jsonify({'error': 'Invalid or expired reset token'}), 400
    
    User.update_password(user.id, password)
    return jsonify({'message': 'Password has been reset'}), 200

@app.route('/booking')
@login_required
def booking_page():
    return render_template('booking.html')

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin.html')

@app.route('/api/aircraft', methods=['GET'])
@login_required
def get_aircraft():
    aircraft = Aircraft.get_all()
    return jsonify(aircraft)

@app.route('/api/instructors', methods=['GET'])
@login_required
def get_instructors():
    instructors = Instructor.get_all()
    return jsonify(instructors)

@app.route('/api/available-aircraft', methods=['GET'])
@login_required
def get_available_aircraft():
    start_time = datetime.fromisoformat(request.args.get('start_time'))
    end_time = datetime.fromisoformat(request.args.get('end_time'))
    
    # Get all aircraft
    aircraft = Aircraft.get_all()
    
    # Filter out aircraft with conflicts
    available_aircraft = []
    for a in aircraft:
        if Booking.check_availability(start_time, end_time, aircraft_id=a['id']):
            available_aircraft.append(a)
    
    return jsonify(available_aircraft)

@app.route('/api/available-instructors', methods=['GET'])
@login_required
def get_available_instructors():
    start_time = datetime.fromisoformat(request.args.get('start_time'))
    end_time = datetime.fromisoformat(request.args.get('end_time'))
    
    # Get all instructors
    instructors = Instructor.get_all()
    
    # Filter out instructors with conflicts
    available_instructors = []
    for i in instructors:
        if Booking.check_availability(start_time, end_time, instructor_id=i['id']):
            available_instructors.append(i)
    
    return jsonify(available_instructors)

@app.route('/api/calendar-bookings', methods=['GET'])
@login_required
def get_calendar_bookings():
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=30)
    
    bookings = Booking.get_by_date_range(start_date, end_date)
    
    # Format bookings for calendar
    calendar_events = []
    for booking in bookings:
        calendar_events.append({
            'id': booking['id'],
            'title': f"{booking['aircraft_name']} - {booking['instructor_name']}",
            'start': booking['start_time'],
            'end': booking['end_time'],
            'status': booking['status']
        })
    
    return jsonify(calendar_events)

@app.route('/api/check-availability', methods=['POST'])
@login_required
def check_availability():
    data = request.get_json()
    start_time = datetime.fromisoformat(data['start_time'])
    end_time = datetime.fromisoformat(data['end_time'])
    aircraft_id = data.get('aircraft_id')
    instructor_id = data.get('instructor_id')
    
    if not aircraft_id and not instructor_id:
        return jsonify({'error': 'At least one of aircraft_id or instructor_id is required'}), 400
    
    is_available = Booking.check_availability(start_time, end_time, aircraft_id, instructor_id)
    return jsonify({'available': is_available})

if __name__ == '__main__':
    app.run(debug=True) 
