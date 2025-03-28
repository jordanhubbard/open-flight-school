import pytest
from app import app
from database import User, Aircraft, Instructor, Booking
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
    app.config['MAIL_SUPPRESS_SEND'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'test@example.com'
    app.config['MAIL_SERVER'] = 'localhost'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None
    
    with app.app_context():
        yield

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def test_user():
    user = User.create(
        username='testuser',
        email='test@example.com',
        password='password123',
        role='student'
    )
    return user

@pytest.fixture
def test_admin():
    admin = User.create(
        username='admin',
        email='admin@example.com',
        password='admin123',
        role='admin'
    )
    return admin

@pytest.fixture
def test_aircraft():
    aircraft = Aircraft.create(
        tail_number='N12345',
        make_model='Cessna 172',
        type_='Single Engine'
    )
    return aircraft

@pytest.fixture
def test_instructor():
    instructor = Instructor.create(
        name='John Doe',
        email='john@example.com',
        phone='123-456-7890',
        ratings='CFI,CFII,MEI'
    )
    return instructor

@pytest.fixture
def test_booking(test_user, test_aircraft, test_instructor):
    booking = Booking.create(
        user_id=test_user['id'],
        aircraft_id=test_aircraft['id'],
        instructor_id=test_instructor['id'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1)
    )
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

def test_get_bookings(client):
    # Login first
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123'
    })
    client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    
    # Create test aircraft and instructor
    aircraft = Aircraft.create(
        tail_number='N12346',
        make_model='Cessna 172',
        type_='Single Engine'
    )
    instructor = Instructor.create(
        name='Test Instructor 1',
        email='instructor1@example.com',
        phone='555-0125',
        ratings='CFI'
    )
    
    # Create a test booking
    booking = Booking.create(
        start_time=datetime.utcnow() + timedelta(days=1),
        end_time=datetime.utcnow() + timedelta(days=1, hours=2),
        user_id=1,
        aircraft_id=aircraft['id'],
        instructor_id=instructor['id']
    )
    
    response = client.get('/api/bookings')
    assert response.status_code == 200

def test_create_booking(client, capture_logs):
    # Login first
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123'
    })
    client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    
    # Create test aircraft and instructor
    aircraft = Aircraft.create(
        tail_number='N12347',
        make_model='Cessna 172',
        type_='Single Engine'
    )
    instructor = Instructor.create(
        name='Test Instructor 2',
        email='instructor2@example.com',
        phone='555-0126',
        ratings='CFI'
    )
    
    # Create a test booking
    response = client.post('/api/bookings', json={
        'start_time': (datetime.utcnow() + timedelta(days=1)).isoformat(),
        'end_time': (datetime.utcnow() + timedelta(days=1, hours=2)).isoformat(),
        'aircraft_id': aircraft['id'],
        'instructor_id': instructor['id']
    })
    assert response.status_code == 201
    assert 'booking_id' in response.json

def test_password_reset(client, capture_logs):
    # First register a user
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123'
    })
    
    # Request password reset
    response = client.post('/api/request-password-reset', json={
        'email': 'test@example.com'
    })
    assert response.status_code == 200
    assert 'message' in response.json

def test_booking_conflicts(client):
    # Login first
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123'
    })
    client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    
    # Create test aircraft and instructor
    aircraft = Aircraft.create(
        tail_number='N12348',
        make_model='Cessna 172',
        type_='Single Engine'
    )
    instructor = Instructor.create(
        name='Test Instructor 3',
        email='instructor3@example.com',
        phone='555-0127',
        ratings='CFI'
    )
    
    # Create first booking
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    Booking.create(
        start_time=start_time,
        end_time=end_time,
        user_id=1,
        aircraft_id=aircraft['id'],
        instructor_id=instructor['id']
    )
    
    # Try to create conflicting booking
    response = client.post('/api/bookings', json={
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'aircraft_id': aircraft['id'],
        'instructor_id': instructor['id']
    })
    assert response.status_code == 400
    assert 'error' in response.json