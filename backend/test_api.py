import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from . import models, schemas
from .database import Base
from .api import router
from fastapi import FastAPI

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test database tables
Base.metadata.create_all(bind=engine)

# Create a test app
app = FastAPI()
app.include_router(router, prefix="/api/v1")

# Create a test client
client = TestClient(app)

# Fixture to get a test database session
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test data
test_user_data = {
    "email": "test@example.com",
    "full_name": "Test User",
    "phone": "1234567890",
    "address": "123 Test St",
    "medical_class": "Class 1",
    "medical_expiry": "2023-12-31T00:00:00",
    "ratings": "Private Pilot",
    "endorsements": "None",
    "flight_reviews": "None",
    "currency": "Current",
    "notes": "Test notes",
    "password": "testpassword"
}

test_aircraft_data = {
    "registration": "N12345",
    "make_model": "Cessna 172",
    "year": 2020,
    "serial_number": "12345",
    "total_time": 1000,
    "last_maintenance": "2023-01-01T00:00:00",
    "next_maintenance": "2024-01-01T00:00:00",
    "status": "Available",
    "notes": "Test aircraft"
}

test_instructor_data = {
    "name": "Test Instructor",
    "email": "instructor@example.com",
    "phone": "0987654321",
    "ratings": "CFI",
    "endorsements": "None",
    "flight_reviews": "None",
    "currency": "Current",
    "availability": "Full-time",
    "notes": "Test instructor"
}

test_booking_data = {
    "student_id": 1,
    "instructor_id": 1,
    "aircraft_id": 1,
    "start_time": "2023-12-31T10:00:00",
    "end_time": "2023-12-31T12:00:00",
    "status": "Scheduled",
    "notes": "Test booking"
}

# Test User endpoints
def test_create_user():
    response = client.post("/api/v1/users/", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["full_name"] == test_user_data["full_name"]

def test_read_users():
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_user():
    response = client.get("/api/v1/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]

def test_update_user():
    updated_data = test_user_data.copy()
    updated_data["full_name"] = "Updated User"
    response = client.put("/api/v1/users/1", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated User"

def test_delete_user():
    response = client.delete("/api/v1/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]

# Test Aircraft endpoints
def test_create_aircraft():
    response = client.post("/api/v1/aircraft/", json=test_aircraft_data)
    assert response.status_code == 200
    data = response.json()
    assert data["registration"] == test_aircraft_data["registration"]

def test_read_aircrafts():
    response = client.get("/api/v1/aircraft/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_aircraft():
    response = client.get("/api/v1/aircraft/1")
    assert response.status_code == 200
    data = response.json()
    assert data["registration"] == test_aircraft_data["registration"]

def test_update_aircraft():
    updated_data = test_aircraft_data.copy()
    updated_data["status"] = "Maintenance"
    response = client.put("/api/v1/aircraft/1", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Maintenance"

def test_delete_aircraft():
    response = client.delete("/api/v1/aircraft/1")
    assert response.status_code == 200
    data = response.json()
    assert data["registration"] == test_aircraft_data["registration"]

# Test Instructor endpoints
def test_create_instructor():
    response = client.post("/api/v1/instructors/", json=test_instructor_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_instructor_data["email"]

def test_read_instructors():
    response = client.get("/api/v1/instructors/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_instructor():
    response = client.get("/api/v1/instructors/1")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_instructor_data["email"]

def test_update_instructor():
    updated_data = test_instructor_data.copy()
    updated_data["availability"] = "Part-time"
    response = client.put("/api/v1/instructors/1", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["availability"] == "Part-time"

def test_delete_instructor():
    response = client.delete("/api/v1/instructors/1")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_instructor_data["email"]

# Test Booking endpoints
def test_create_booking():
    response = client.post("/api/v1/bookings/", json=test_booking_data)
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == test_booking_data["student_id"]

def test_read_bookings():
    response = client.get("/api/v1/bookings/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_booking():
    response = client.get("/api/v1/bookings/1")
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == test_booking_data["student_id"]

def test_update_booking():
    updated_data = test_booking_data.copy()
    updated_data["status"] = "Completed"
    response = client.put("/api/v1/bookings/1", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Completed"

def test_delete_booking():
    response = client.delete("/api/v1/bookings/1")
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == test_booking_data["student_id"] 