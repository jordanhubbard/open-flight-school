import pytest
from app import app, db, User, Aircraft, Instructor, Booking
from datetime import datetime, timedelta
import json
import os
import logging
import io
import sys

# Set testing mode before importing app
os.environ['FLASK_ENV'] = 'testing'
os.environ['TESTING'] = 'true'

# Configure logging for tests
logger = logging.getLogger('__main__')
logger.setLevel(logging.INFO)

@pytest.fixture
def capture_logs(caplog):
    caplog.set_level(logging.INFO, logger='__main__')
    return caplog

@pytest.fixture
def app_context():
    app.testing = True
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/flight_school_test')
    app.config['MAIL_SUPPRESS_SEND'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'test@example.com'
    app.config['MAIL_SERVER'] = 'localhost'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None
    
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_context):
    with app.test_client() as client:
        # Create test user
        with app.app_context():
            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User'
            )
            user.set_password('test123')
            db.session.add(user)
            db.session.commit()
        yield client

def test_register(client):
    response = client.post('/api/register', json={
        'first_name': 'New',
        'last_name': 'User',
        'email': 'new@example.com',
        'password': 'newpass123',
        'address': '456 New St',
        'phone': '555-0124'
    })
    assert response.status_code == 201
    assert b'Registration successful' in response.data

def test_login(client):
    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    assert response.status_code == 200
    assert b'Login successful' in response.data

def test_get_bookings(client):
    # Login first
    client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    
    # Create test aircraft and instructor
    with app.app_context():
        aircraft = Aircraft(
            tail_number='N12345',
            make_model='Cessna 172',
            type='Single Engine'
        )
        instructor = Instructor(
            name='Test Instructor',
            email='instructor@example.com',
            phone='555-0125',
            ratings='CFI'
        )
        db.session.add(aircraft)
        db.session.add(instructor)
        db.session.commit()
        
        # Create a test booking
        booking = Booking(
            start_time=datetime.utcnow() + timedelta(days=1),
            end_time=datetime.utcnow() + timedelta(days=1, hours=2),
            user_id=1,
            aircraft_id=1,
            instructor_id=1
        )
        db.session.add(booking)
        db.session.commit()
    
    response = client.get('/api/bookings')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0

def test_create_booking(client, capture_logs):
    # Login first
    client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })

    # Create test aircraft and instructor
    with app.app_context():
        # Ensure testing mode is set
        app.testing = True
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True

        aircraft = Aircraft(
            tail_number='N12345',
            make_model='Cessna 172',
            type='Single Engine'
        )
        instructor = Instructor(
            name='Test Instructor',
            email='instructor@example.com',
            phone='555-0125',
            ratings='CFI'
        )
        db.session.add(aircraft)
        db.session.add(instructor)
        db.session.commit()

    # Create booking
    response = client.post('/api/bookings', json={
        'start_time': (datetime.utcnow() + timedelta(days=1)).isoformat(),
        'end_time': (datetime.utcnow() + timedelta(days=1, hours=2)).isoformat(),
        'aircraft_id': 1,
        'instructor_id': 1
    })
    assert response.status_code == 201
    assert b'Booking created successfully' in response.data

    # Print captured logs for debugging
    print("\nCaptured logs:")
    for record in capture_logs.records:
        print(f"Logger: {record.name}, Level: {record.levelname}, Message: {record.message}")

    # Verify that confirmation email was logged
    assert any('[TEST] Would send email:' in record.message for record in capture_logs.records)

def test_password_reset(client, capture_logs):
    # Request password reset
    response = client.post('/api/request-password-reset', json={
        'email': 'test@example.com'
    })
    assert response.status_code == 200
    assert b'Password reset email sent' in response.data
    
    # Verify that password reset email was logged
    assert any('[TEST] Would send email:' in record.message for record in capture_logs.records)
    assert any('Subject: Password Reset Request' in record.message for record in capture_logs.records)
    assert any('To: [\'test@example.com\']' in record.message for record in capture_logs.records)
    assert any('To reset your password, visit the following link:' in record.message for record in capture_logs.records)

def test_booking_conflicts(client):
    # Login first
    client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    
    # Create test aircraft and instructor
    with app.app_context():
        aircraft = Aircraft(
            tail_number='N12345',
            make_model='Cessna 172',
            type='Single Engine'
        )
        instructor = Instructor(
            name='Test Instructor',
            email='instructor@example.com',
            phone='555-0125',
            ratings='CFI'
        )
        db.session.add(aircraft)
        db.session.add(instructor)
        db.session.commit()
    
    # Create first booking
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    client.post('/api/bookings', json={
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'aircraft_id': 1,
        'instructor_id': 1
    })
    
    # Try to create conflicting booking
    response = client.post('/api/bookings', json={
        'start_time': (start_time + timedelta(hours=1)).isoformat(),
        'end_time': (end_time + timedelta(hours=1)).isoformat(),
        'aircraft_id': 1,
        'instructor_id': 1
    })
    assert response.status_code == 400
    assert b'Time slot is not available' in response.data 