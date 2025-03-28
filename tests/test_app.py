import pytest
from app import create_app
from extensions import db
import os

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    
    # Use the test database URL from environment
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:postgres@db:5432/flight_school_test')
    
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
def runner(app):
    """Create a test runner for the app's CLI commands."""
    return app.test_cli_runner()

def test_app_exists(app):
    assert app is not None

def test_app_is_testing(app):
    assert app.config['TESTING'] is True

def test_app_has_secret_key(app):
    assert app.config['SECRET_KEY'] is not None

def test_app_has_database(app):
    """Test that the app has the correct database configuration."""
    expected_uri = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:postgres@db:5432/flight_school_test')
    assert app.config['SQLALCHEMY_DATABASE_URI'] == expected_uri

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Open Flight School' in response.data

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_booking_page_requires_login(client):
    response = client.get('/booking')
    assert response.status_code == 302
    assert '/login?next=%2Fbooking' in response.location

def test_register_user(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'password_confirm': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful' in response.data

def test_login_user(client):
    # First register a user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'password_confirm': 'password123'
    })
    
    # Then try to login
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome back' in response.data

def test_logout_user(client):
    # First register and login
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'password_confirm': 'password123'
    })
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Then logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out' in response.data 