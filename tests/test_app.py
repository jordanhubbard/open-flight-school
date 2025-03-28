import pytest
from app import app
from database import init_db, User, Aircraft, Instructor, Booking
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DATABASE'] = 'test.db'
    init_db()
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    if os.path.exists('test.db'):
        os.remove('test.db')

def test_app_exists():
    assert app is not None

def test_app_is_testing():
    assert app.config['TESTING'] is True

def test_app_has_secret_key():
    assert app.config['SECRET_KEY'] is not None

def test_app_has_database():
    assert app.config['DATABASE'] is not None
    assert 'test.db' in app.config['DATABASE']

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