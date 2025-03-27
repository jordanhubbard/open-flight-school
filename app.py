from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, current_app, session
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from extensions import db, login_manager, mail
from models import User, Aircraft, Instructor, Booking
from urllib.parse import urljoin
from functools import wraps
import logging
import sys

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
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')

# Database configuration
database_url = os.getenv('DATABASE_URL', 'sqlite:///instance/flight_school.db')
if database_url.startswith('sqlite:///'):
    # Ensure the instance folder exists
    os.makedirs(os.path.dirname(os.path.abspath(database_url.replace('sqlite:///', ''))), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protect against CSRF

# Email configuration
if app.config.get('TESTING'):
    app.config['MAIL_SUPPRESS_SEND'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'test@example.com'
    app.config['MAIL_SERVER'] = 'localhost'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None
else:
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:5001')

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login_page'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'
mail.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    logger.debug(f"Loading user with ID: {user_id}")
    return User.query.get(int(user_id))

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
        if not current_user.is_authenticated or not current_user.is_admin:
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
    return render_template('home.html')

@app.route('/login', methods=['GET'])
def login_page():
    if current_user.is_authenticated:
        # Redirect admin users to admin dashboard, regular users to booking page
        return redirect(url_for('admin_dashboard') if current_user.is_admin else url_for('booking_page'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('home'))

@app.route('/api/register', methods=['POST'])
def register():
    logger.debug("Registration request received")
    data = request.get_json()
    logger.debug(f"Registration data: {data}")
    
    if User.query.filter_by(email=data['email']).first():
        logger.debug(f"Email {data['email']} already registered")
        return jsonify({'error': 'Email already registered'}), 400
    
    try:
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            is_admin=False
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        logger.debug(f"User {data['email']} registered successfully")
        return jsonify({'message': 'Registration successful'}), 201
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    logger.debug("Login request received")
    data = request.get_json()
    logger.debug(f"Login attempt for email: {data['email']}")
    
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        # Set up secure session
        session.permanent = True
        login_user(user)
        logger.debug(f"User {data['email']} logged in successfully")
        # Redirect admin users to admin dashboard, regular users to booking page
        redirect_url = url_for('admin_dashboard') if user.is_admin else url_for('booking_page')
        return jsonify({
            'message': 'Login successful',
            'redirect': redirect_url
        })
    
    logger.debug(f"Login failed for email: {data['email']}")
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/bookings', methods=['GET'])
@login_required
def get_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': b.id,
        'start_time': b.start_time.isoformat(),  # Return in ISO format
        'end_time': b.end_time.isoformat(),      # Return in ISO format
        'aircraft': b.aircraft.make_model if b.aircraft else None,
        'instructor': b.instructor.name if b.instructor else None,
        'aircraft_id': b.aircraft_id,
        'instructor_id': b.instructor_id,
        'status': b.status
    } for b in bookings])

@app.route('/api/bookings', methods=['POST'])
@login_required
def create_booking():
    data = request.get_json()
    logger.info(f"Creating booking with data: {data}")
    
    try:
        # Parse datetime strings from ISO format
        start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
        
        # Validate booking duration
        duration = end_time - start_time
        if duration.total_seconds() < 0:
            return jsonify({'error': 'End time must be after start time'}), 400
        if duration.total_seconds() > 8 * 3600:  # 8 hours max
            return jsonify({'error': 'Booking duration cannot exceed 8 hours'}), 400
        
        # Check for conflicts with non-cancelled bookings
        conflicts = Booking.query.filter(
            Booking.status != 'cancelled',
            ((Booking.aircraft_id == data['aircraft_id']) | (Booking.instructor_id == data['instructor_id'])),
            ((Booking.start_time <= end_time) & (Booking.end_time >= start_time))
        ).first()
        
        if conflicts:
            logger.info(f"Found conflicting booking: {conflicts.id}")
            return jsonify({'error': 'Time slot is not available'}), 400
        
        booking = Booking(
            start_time=start_time,
            end_time=end_time,
            user_id=current_user.id,
            aircraft_id=data['aircraft_id'],
            instructor_id=data['instructor_id'],
            status='confirmed'
        )
        
        db.session.add(booking)
        db.session.commit()
        logger.info(f"Successfully created booking {booking.id}")
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': {
                'id': booking.id,
                'start_time': booking.start_time.isoformat(),
                'end_time': booking.end_time.isoformat(),
                'aircraft': booking.aircraft.make_model,
                'instructor': booking.instructor.name,
                'status': booking.status
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        return jsonify({'error': str(e)}), 400

def send_confirmation_email(booking):
    if not app.config.get('MAIL_USERNAME') or not app.config.get('MAIL_PASSWORD'):
        logger.warning("Email configuration not set, skipping confirmation email")
        return
        
    msg = Message('Booking Confirmation',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[booking.user.email])
    msg.body = f'''Your booking has been confirmed:
    Start: {booking.start_time}
    End: {booking.end_time}
    Aircraft: {booking.aircraft.make_model if booking.aircraft else 'None'}
    Instructor: {booking.instructor.name if booking.instructor else 'None'}
    '''
    
    if app.testing or app.config.get('TESTING', False):
        logger.info(f"[TEST] Would send email:\nSubject: {msg.subject}\nTo: {msg.recipients}\n\n{msg.body}")
    else:
        try:
            mail.send(msg)
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            # Don't re-raise the exception, just log it

def send_password_reset_email(user):
    token = user.generate_reset_token()
    reset_url = urljoin(app.config['BASE_URL'], url_for('reset_password', token=token, _external=True))
    
    msg = Message('Password Reset Request',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request then simply ignore this email.
'''
    
    if app.config.get('TESTING', False):
        logger.info(f"[TEST] Would send email:\nSubject: {msg.subject}\nTo: {msg.recipients}\n\n{msg.body}")
    else:
        mail.send(msg)

@app.route('/api/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user:
        send_password_reset_email(user)
        return jsonify({'message': 'Password reset email sent'})
    
    # Return success even if email doesn't exist to prevent email enumeration
    return jsonify({'message': 'If the email exists, a password reset link has been sent'})

@app.route('/api/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.is_reset_token_valid():
        return jsonify({'error': 'Invalid or expired reset token'}), 400
    
    user.set_password(data['password'])
    user.reset_token = None
    user.reset_token_expires = None
    db.session.commit()
    
    return jsonify({'message': 'Password has been reset'})

# Admin routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/api/admin/aircraft', methods=['GET'])
@login_required
@admin_required
def get_all_aircraft():
    aircraft = Aircraft.query.all()
    return jsonify([{
        'id': a.id,
        'tail_number': a.tail_number,
        'make_model': a.make_model,
        'type': a.type
    } for a in aircraft])

@app.route('/api/admin/aircraft', methods=['POST'])
@login_required
@admin_required
def create_aircraft():
    data = request.get_json()
    aircraft = Aircraft(
        tail_number=data['tail_number'],
        make_model=data['make_model'],
        type=data['type']
    )
    db.session.add(aircraft)
    db.session.commit()
    return jsonify({
        'id': aircraft.id,
        'tail_number': aircraft.tail_number,
        'make_model': aircraft.make_model,
        'type': aircraft.type
    }), 201

@app.route('/api/admin/aircraft/<int:id>', methods=['PUT'])
@login_required
@admin_required
def update_aircraft(id):
    aircraft = Aircraft.query.get_or_404(id)
    data = request.get_json()
    aircraft.tail_number = data['tail_number']
    aircraft.make_model = data['make_model']
    aircraft.type = data['type']
    db.session.commit()
    return jsonify({
        'id': aircraft.id,
        'tail_number': aircraft.tail_number,
        'make_model': aircraft.make_model,
        'type': aircraft.type
    })

@app.route('/api/admin/aircraft/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_aircraft(id):
    aircraft = Aircraft.query.get_or_404(id)
    db.session.delete(aircraft)
    db.session.commit()
    return jsonify({'message': 'Aircraft deleted successfully'})

@app.route('/api/admin/aircraft/<int:id>', methods=['GET'])
@login_required
@admin_required
def get_aircraft(id):
    aircraft = Aircraft.query.get_or_404(id)
    return jsonify({
        'id': aircraft.id,
        'tail_number': aircraft.tail_number,
        'make_model': aircraft.make_model,
        'type': aircraft.type
    })

@app.route('/api/admin/instructors', methods=['GET'])
@login_required
@admin_required
def get_all_instructors():
    instructors = Instructor.query.all()
    return jsonify([{
        'id': i.id,
        'name': i.name,
        'email': i.email,
        'phone': i.phone,
        'ratings': i.ratings.split(',') if i.ratings else []
    } for i in instructors])

@app.route('/api/admin/instructors', methods=['POST'])
@login_required
@admin_required
def create_instructor():
    data = request.get_json()
    instructor = Instructor(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        ratings=','.join(data['ratings']) if data.get('ratings') else ''
    )
    db.session.add(instructor)
    db.session.commit()
    return jsonify({
        'id': instructor.id,
        'name': instructor.name,
        'email': instructor.email,
        'phone': instructor.phone,
        'ratings': instructor.ratings.split(',') if instructor.ratings else []
    }), 201

@app.route('/api/admin/instructors/<int:id>', methods=['PUT'])
@login_required
@admin_required
def update_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    data = request.get_json()
    instructor.name = data['name']
    instructor.email = data['email']
    instructor.phone = data['phone']
    instructor.ratings = ','.join(data['ratings']) if data.get('ratings') else ''
    db.session.commit()
    return jsonify({
        'id': instructor.id,
        'name': instructor.name,
        'email': instructor.email,
        'phone': instructor.phone,
        'ratings': instructor.ratings.split(',') if instructor.ratings else []
    })

@app.route('/api/admin/instructors/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    db.session.delete(instructor)
    db.session.commit()
    return jsonify({'message': 'Instructor deleted successfully'})

@app.route('/api/admin/users', methods=['GET'])
@login_required
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'first_name': u.first_name,
        'last_name': u.last_name,
        'email': u.email,
        'phone': u.phone,
        'is_admin': u.is_admin,
        'created_at': u.created_at.isoformat()
    } for u in users])

@app.route('/api/admin/users/<int:id>', methods=['PUT'])
@login_required
@admin_required
def update_user_admin(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.is_admin = data.get('is_admin', user.is_admin)
    
    if 'password' in data:
        user.set_password(data['password'])
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/api/admin/bookings', methods=['GET'])
@login_required
@admin_required
def get_all_bookings():
    bookings = Booking.query.all()
    return jsonify([{
        'id': b.id,
        'user': {
            'id': b.user.id,
            'name': f"{b.user.first_name} {b.user.last_name}"
        },
        'start_time': b.start_time.isoformat(),
        'end_time': b.end_time.isoformat(),
        'aircraft': b.aircraft.make_model if b.aircraft else None,
        'instructor': b.instructor.name if b.instructor else None,
        'status': b.status
    } for b in bookings])

@app.route('/api/bookings/<int:id>', methods=['PUT'])
@login_required
def update_booking(id):
    booking = Booking.query.get_or_404(id)
    
    # Check if the booking belongs to the current user
    if booking.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Only allow editing of non-cancelled bookings
    if booking.status == 'cancelled':
        return jsonify({'error': 'Cannot edit this booking'}), 400
    
    data = request.get_json()
    
    # Check for conflicts with other bookings
    conflicts = Booking.query.filter(
        Booking.id != id,
        ((Booking.aircraft_id == data.get('aircraft_id', booking.aircraft_id)) | 
         (Booking.instructor_id == data.get('instructor_id', booking.instructor_id))) &
        ((Booking.start_time <= data.get('end_time', booking.end_time.isoformat())) & 
         (Booking.end_time >= data.get('start_time', booking.start_time.isoformat())))
    ).first()
    
    if conflicts:
        return jsonify({'error': 'Time slot is not available'}), 400
    
    booking.start_time = datetime.fromisoformat(data.get('start_time', booking.start_time.isoformat()))
    booking.end_time = datetime.fromisoformat(data.get('end_time', booking.end_time.isoformat()))
    booking.aircraft_id = data.get('aircraft_id', booking.aircraft_id)
    booking.instructor_id = data.get('instructor_id', booking.instructor_id)
    
    db.session.commit()
    return jsonify({'message': 'Booking updated successfully'})

@app.route('/api/admin/bookings/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted successfully'})

@app.route('/booking')
@login_required
def booking_page():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    # Get user's bookings
    user_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('booking.html', user_bookings=user_bookings)

@app.route('/bookings')
@login_required
def bookings_redirect():
    # Redirect admin users to admin dashboard
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('booking_page'))

@app.route('/api/available-aircraft', methods=['GET'])
@login_required
def get_available_aircraft():
    try:
        # Get all aircraft
        aircraft = Aircraft.query.all()
        logger.info(f"Returning {len(aircraft)} aircraft")
        return jsonify([a.to_dict() for a in aircraft])
    except Exception as e:
        logger.error(f"Error in get_available_aircraft: {str(e)}")
        return jsonify({'error': 'Failed to get available aircraft'}), 500

@app.route('/api/available-instructors', methods=['GET'])
@login_required
def get_available_instructors():
    try:
        # Get all instructors
        instructors = Instructor.query.all()
        logger.info(f"Returning {len(instructors)} instructors")
        return jsonify([i.to_dict() for i in instructors])
    except Exception as e:
        logger.error(f"Error in get_available_instructors: {str(e)}")
        return jsonify({'error': 'Failed to get available instructors'}), 500

@app.route('/api/bookings/calendar', methods=['GET'])
@login_required
def get_calendar_bookings():
    # Get all bookings for the next 30 days
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=30)
    
    bookings = Booking.query.filter(
        Booking.start_time >= start_date,
        Booking.start_time <= end_date
    ).all()
    
    return jsonify([{
        'id': b.id,
        'start': b.start_time.isoformat(),
        'end': b.end_time.isoformat(),
        'aircraft': b.aircraft.make_model if b.aircraft else None,
        'instructor': b.instructor.name if b.instructor else None,
        'is_own_booking': b.user_id == current_user.id,
        'status': b.status
    } for b in bookings])

@app.route('/api/check-availability', methods=['POST'])
@login_required
def check_availability():
    data = request.get_json()
    
    # Parse datetime strings from ISO format
    start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
    end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
    
    # Validate time range
    if end_time <= start_time:
        return jsonify({'error': 'End time must be after start time'}), 400
    
    # Get all non-cancelled bookings that overlap with the requested time slot
    overlapping_bookings = Booking.query.filter(
        Booking.status != 'cancelled',
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).all()
    
    # Get all aircraft and instructors
    all_aircraft = Aircraft.query.all()
    all_instructors = Instructor.query.all()
    
    # Mark which ones are available
    booked_aircraft_ids = {b.aircraft_id for b in overlapping_bookings if b.aircraft_id}
    booked_instructor_ids = {b.instructor_id for b in overlapping_bookings if b.instructor_id}
    
    aircraft_list = [{
        'id': a.id,
        'make_model': a.make_model,
        'tail_number': a.tail_number,
        'type': a.type,
        'available': a.id not in booked_aircraft_ids
    } for a in all_aircraft]
    
    instructor_list = [{
        'id': i.id,
        'name': i.name,
        'email': i.email,
        'phone': i.phone,
        'ratings': i.ratings.split(',') if i.ratings else [],
        'available': i.id not in booked_instructor_ids
    } for i in all_instructors]
    
    return jsonify({
        'aircraft': aircraft_list,
        'instructors': instructor_list
    })

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/api/user', methods=['GET'])
@login_required
def get_user():
    return jsonify({
        'id': current_user.id,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email,
        'phone': current_user.phone,
        'address': current_user.address,
        'credit_card': current_user.credit_card,
        'is_admin': current_user.is_admin
    })

@app.route('/api/user', methods=['PUT'])
@login_required
def update_user():
    data = request.get_json()
    
    # Check if email is being changed and if it's already taken
    if data.get('email') and data['email'] != current_user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
    
    # Update user fields
    current_user.first_name = data.get('first_name', current_user.first_name)
    current_user.last_name = data.get('last_name', current_user.last_name)
    current_user.email = data.get('email', current_user.email)
    current_user.phone = data.get('phone', current_user.phone)
    current_user.address = data.get('address', current_user.address)
    current_user.credit_card = data.get('credit_card', current_user.credit_card)
    
    # Update password if provided
    if data.get('password'):
        current_user.set_password(data['password'])
    
    try:
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_booking(id):
    booking = Booking.query.get_or_404(id)
    
    # Check if the booking belongs to the current user
    if booking.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Only allow cancellation of non-cancelled bookings
    if booking.status == 'cancelled':
        return jsonify({'error': 'Cannot cancel this booking'}), 400
    
    booking.status = 'cancelled'
    db.session.commit()
    
    return jsonify({'message': 'Booking cancelled successfully'})

@app.route('/my-bookings')
@login_required
def my_bookings():
    # Redirect admin users to admin dashboard
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    return render_template('bookings.html')

@app.route('/health')
def health_check():
    try:
        # Try to query the database
        User.query.first()
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
