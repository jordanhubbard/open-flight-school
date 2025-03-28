import pytest
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Aircraft, Instructor, Booking
from extensions import db
import os

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    
    # Use the test database URL from environment
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:postgres@db:5432/flight_school_test')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_create_user(app):
    """Test creating a new user."""
    user = User(
        username='testuser',
        email='test@example.com',
        password=generate_password_hash('password123'),
        role='student'
    )
    db.session.add(user)
    db.session.commit()
    
    assert user.id is not None
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.role == 'student'
    assert user.check_password('password123')

def test_update_user(app):
    """Test updating a user."""
    user = User(
        username='oldname',
        email='old@example.com',
        password=generate_password_hash('password123'),
        role='student'
    )
    db.session.add(user)
    db.session.commit()
    
    user.username = 'newname'
    user.email = 'new@example.com'
    db.session.commit()
    
    updated_user = User.query.get(user.id)
    assert updated_user.username == 'newname'
    assert updated_user.email == 'new@example.com'

def test_delete_user(app):
    """Test deleting a user."""
    user = User(
        username='testuser',
        email='test@example.com',
        password=generate_password_hash('password123'),
        role='student'
    )
    db.session.add(user)
    db.session.commit()
    
    db.session.delete(user)
    db.session.commit()
    
    assert User.query.get(user.id) is None

def test_create_aircraft(app):
    """Test creating a new aircraft."""
    aircraft = Aircraft(
        tail_number='N12345',
        make_model='Cessna 172',
        aircraft_type='Single Engine',
        status='available'
    )
    db.session.add(aircraft)
    db.session.commit()
    
    assert aircraft.id is not None
    assert aircraft.tail_number == 'N12345'
    assert aircraft.make_model == 'Cessna 172'
    assert aircraft.status == 'available'

def test_update_aircraft(app):
    """Test updating an aircraft."""
    aircraft = Aircraft(
        tail_number='N12345',
        make_model='Cessna 172',
        aircraft_type='Single Engine',
        status='available'
    )
    db.session.add(aircraft)
    db.session.commit()
    
    aircraft.status = 'maintenance'
    aircraft.make_model = 'Cessna 182'
    db.session.commit()
    
    updated_aircraft = Aircraft.query.get(aircraft.id)
    assert updated_aircraft.status == 'maintenance'
    assert updated_aircraft.make_model == 'Cessna 182'

def test_delete_aircraft(app):
    """Test deleting an aircraft."""
    aircraft = Aircraft(
        tail_number='N12345',
        make_model='Cessna 172',
        aircraft_type='Single Engine',
        status='available'
    )
    db.session.add(aircraft)
    db.session.commit()
    
    db.session.delete(aircraft)
    db.session.commit()
    
    assert Aircraft.query.get(aircraft.id) is None

def test_create_instructor(app):
    """Test creating a new instructor."""
    instructor = Instructor(
        name='John Doe',
        email='john@example.com',
        phone='123-456-7890',
        ratings='CFI,CFII,MEI'
    )
    db.session.add(instructor)
    db.session.commit()
    
    assert instructor.id is not None
    assert instructor.name == 'John Doe'
    assert instructor.email == 'john@example.com'
    assert instructor.ratings == 'CFI,CFII,MEI'

def test_update_instructor(app):
    """Test updating an instructor."""
    instructor = Instructor(
        name='John Doe',
        email='john@example.com',
        phone='123-456-7890',
        ratings='CFI'
    )
    db.session.add(instructor)
    db.session.commit()
    
    instructor.name = 'Jane Doe'
    instructor.ratings = 'CFI,CFII'
    db.session.commit()
    
    updated_instructor = Instructor.query.get(instructor.id)
    assert updated_instructor.name == 'Jane Doe'
    assert updated_instructor.ratings == 'CFI,CFII'

def test_delete_instructor(app):
    """Test deleting an instructor."""
    instructor = Instructor(
        name='John Doe',
        email='john@example.com',
        phone='123-456-7890',
        ratings='CFI,CFII,MEI'
    )
    db.session.add(instructor)
    db.session.commit()
    
    db.session.delete(instructor)
    db.session.commit()
    
    assert Instructor.query.get(instructor.id) is None

def test_create_booking(app):
    """Test creating a new booking."""
    # Create required related records
    user = User(username='testuser', email='test@example.com', 
                password=generate_password_hash('password123'), role='student')
    aircraft = Aircraft(tail_number='N12345', make_model='Cessna 172',
                       aircraft_type='Single Engine', status='available')
    instructor = Instructor(name='John Doe', email='john@example.com',
                          phone='123-456-7890', ratings='CFI')
    
    db.session.add_all([user, aircraft, instructor])
    db.session.commit()
    
    # Create booking
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    booking = Booking(
        user_id=user.id,
        aircraft_id=aircraft.id,
        instructor_id=instructor.id,
        start_time=start_time,
        end_time=end_time,
        status='confirmed'
    )
    db.session.add(booking)
    db.session.commit()
    
    assert booking.id is not None
    assert booking.user_id == user.id
    assert booking.aircraft_id == aircraft.id
    assert booking.status == 'confirmed'

def test_update_booking(app):
    """Test updating a booking."""
    # Create required related records
    user = User(username='testuser', email='test@example.com',
                password=generate_password_hash('password123'), role='student')
    aircraft = Aircraft(tail_number='N12345', make_model='Cessna 172',
                       aircraft_type='Single Engine', status='available')
    instructor = Instructor(name='John Doe', email='john@example.com',
                          phone='123-456-7890', ratings='CFI')
    
    db.session.add_all([user, aircraft, instructor])
    db.session.commit()
    
    # Create booking
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    booking = Booking(
        user_id=user.id,
        aircraft_id=aircraft.id,
        instructor_id=instructor.id,
        start_time=start_time,
        end_time=end_time,
        status='pending'
    )
    db.session.add(booking)
    db.session.commit()
    
    # Update booking
    booking.status = 'confirmed'
    new_end_time = end_time + timedelta(hours=1)
    booking.end_time = new_end_time
    db.session.commit()
    
    updated_booking = Booking.query.get(booking.id)
    assert updated_booking.status == 'confirmed'
    assert updated_booking.end_time == new_end_time

def test_delete_booking(app):
    """Test deleting a booking."""
    # Create required related records
    user = User(username='testuser', email='test@example.com',
                password=generate_password_hash('password123'), role='student')
    aircraft = Aircraft(tail_number='N12345', make_model='Cessna 172',
                       aircraft_type='Single Engine', status='available')
    instructor = Instructor(name='John Doe', email='john@example.com',
                          phone='123-456-7890', ratings='CFI')
    
    db.session.add_all([user, aircraft, instructor])
    db.session.commit()
    
    # Create booking
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    booking = Booking(
        user_id=user.id,
        aircraft_id=aircraft.id,
        instructor_id=instructor.id,
        start_time=start_time,
        end_time=end_time,
        status='confirmed'
    )
    db.session.add(booking)
    db.session.commit()
    
    # Delete booking
    db.session.delete(booking)
    db.session.commit()
    
    assert Booking.query.get(booking.id) is None

def test_booking_relationships(app):
    """Test that booking relationships are working correctly."""
    # Create required related records
    user = User(username='testuser', email='test@example.com',
                password=generate_password_hash('password123'), role='student')
    aircraft = Aircraft(tail_number='N12345', make_model='Cessna 172',
                       aircraft_type='Single Engine', status='available')
    instructor = Instructor(name='John Doe', email='john@example.com',
                          phone='123-456-7890', ratings='CFI')
    
    db.session.add_all([user, aircraft, instructor])
    db.session.commit()
    
    # Create booking
    booking = Booking(
        user_id=user.id,
        aircraft_id=aircraft.id,
        instructor_id=instructor.id,
        start_time=datetime.utcnow() + timedelta(days=1),
        end_time=datetime.utcnow() + timedelta(days=1, hours=2),
        status='confirmed'
    )
    db.session.add(booking)
    db.session.commit()
    
    # Test relationships
    assert booking.user == user
    assert booking.aircraft == aircraft
    assert booking.instructor == instructor
    assert booking in user.bookings
    assert booking in aircraft.bookings
    assert booking in instructor.bookings

def test_booking_conflict_detection(app):
    """Test that booking conflict detection works correctly."""
    # Create required related records
    user = User(username='testuser', email='test@example.com',
                password=generate_password_hash('password123'), role='student')
    aircraft = Aircraft(tail_number='N12345', make_model='Cessna 172',
                       aircraft_type='Single Engine', status='available')
    instructor = Instructor(name='John Doe', email='john@example.com',
                          phone='123-456-7890', ratings='CFI')
    
    db.session.add_all([user, aircraft, instructor])
    db.session.commit()
    
    # Create first booking
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    booking1 = Booking(
        user_id=user.id,
        aircraft_id=aircraft.id,
        instructor_id=instructor.id,
        start_time=start_time,
        end_time=end_time,
        status='confirmed'
    )
    db.session.add(booking1)
    db.session.commit()
    
    # Create conflicting booking
    booking2 = Booking(
        user_id=user.id,
        aircraft_id=aircraft.id,
        instructor_id=instructor.id,
        start_time=start_time + timedelta(minutes=30),
        end_time=end_time + timedelta(minutes=30),
        status='pending'
    )
    
    # Check for conflict
    assert booking2.check_conflict() is True 