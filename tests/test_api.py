import pytest
from app import create_app
from models import User, Aircraft, Instructor, Booking
from extensions import db
from datetime import datetime, timedelta
import json
import os
import logging
from werkzeug.security import generate_password_hash

# Configure logging for tests
logger = logging.getLogger('__main__')
logger.setLevel(logging.INFO)

@pytest.fixture
def capture_logs(caplog):
    caplog.set_level(logging.INFO, logger='__main__')
    return caplog

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:postgres@db:5432/flight_school_test'),
        'MAIL_SUPPRESS_SEND': True,
        'MAIL_DEFAULT_SENDER': 'test@example.com',
        'MAIL_SERVER': 'localhost',
        'MAIL_PORT': 25,
        'MAIL_USE_TLS': False,
        'MAIL_USERNAME': None,
        'MAIL_PASSWORD': None,
        'WTF_CSRF_ENABLED': False
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Create a test user."""
    user = User(
        username='testuser',
        email='test@example.com',
        password=generate_password_hash('password123'),
        role='student'
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_admin(app):
    """Create a test admin user."""
    admin = User(
        username='admin',
        email='admin@example.com',
        password=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    return admin

@pytest.fixture
def test_aircraft(app):
    """Create a test aircraft."""
    aircraft = Aircraft(
        tail_number='N12345',
        make_model='Cessna 172',
        aircraft_type='Single Engine',
        status='available'
    )
    db.session.add(aircraft)
    db.session.commit()
    return aircraft

@pytest.fixture
def test_instructor(app):
    """Create a test instructor."""
    instructor = Instructor(
        name='John Doe',
        email='john@example.com',
        phone='123-456-7890',
        ratings='CFI,CFII,MEI'
    )
    db.session.add(instructor)
    db.session.commit()
    return instructor

@pytest.fixture
def test_booking(app, test_user, test_aircraft, test_instructor):
    """Create a test booking."""
    booking = Booking(
        user_id=test_user.id,
        aircraft_id=test_aircraft.id,
        instructor_id=test_instructor.id,
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        status='confirmed'
    )
    db.session.add(booking)
    db.session.commit()
    return booking

def test_register(client):
    response = client.post('/api/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'newpass123'
    })
    assert response.status_code == 201
    assert 'user_id' in response.json

def test_login(client):
    # First register a user
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123'
    })
    
    # Then try to login
    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    assert response.status_code == 200
    assert 'message' in response.json

def test_get_bookings(client, test_user, test_aircraft, test_instructor):
    # Login first
    client.post('/api/login', json={
        'email': test_user.email,
        'password': 'password123'
    })
    
    # Create a test booking
    booking = Booking(
        user_id=test_user.id,
        aircraft_id=test_aircraft.id,
        instructor_id=test_instructor.id,
        start_time=datetime.utcnow() + timedelta(days=1),
        end_time=datetime.utcnow() + timedelta(days=1, hours=2),
        status='confirmed'
    )
    db.session.add(booking)
    db.session.commit()
    
    response = client.get('/api/bookings')
    assert response.status_code == 200

def test_create_booking(client, test_user, test_aircraft, test_instructor, capture_logs):
    # Login first
    client.post('/api/login', json={
        'email': test_user.email,
        'password': 'password123'
    })
    
    # Create a test booking
    response = client.post('/api/bookings', json={
        'start_time': (datetime.utcnow() + timedelta(days=1)).isoformat(),
        'end_time': (datetime.utcnow() + timedelta(days=1, hours=2)).isoformat(),
        'aircraft_id': test_aircraft.id,
        'instructor_id': test_instructor.id
    })
    assert response.status_code == 201
    assert 'booking_id' in response.json

def test_password_reset(client, test_user, capture_logs):
    # Request password reset
    response = client.post('/api/request-password-reset', json={
        'email': test_user.email
    })
    assert response.status_code == 200
    assert 'message' in response.json

def test_booking_conflicts(client, test_user, test_aircraft, test_instructor):
    # Login first
    client.post('/api/login', json={
        'email': test_user.email,
        'password': 'password123'
    })
    
    # Create first booking
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    booking1 = Booking(
        user_id=test_user.id,
        aircraft_id=test_aircraft.id,
        instructor_id=test_instructor.id,
        start_time=start_time,
        end_time=end_time,
        status='confirmed'
    )
    db.session.add(booking1)
    db.session.commit()
    
    # Try to create conflicting booking
    response = client.post('/api/bookings', json={
        'start_time': (start_time + timedelta(hours=1)).isoformat(),
        'end_time': (end_time + timedelta(hours=1)).isoformat(),
        'aircraft_id': test_aircraft.id,
        'instructor_id': test_instructor.id
    })
    assert response.status_code == 400
    assert 'error' in response.json