import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import User, Aircraft, Instructor, Flight, FlightType, FlightStatus
from datetime import datetime, timedelta

# Test data
test_user_data = {
    "email": "test1@example.com",
    "password": "testpassword",
    "full_name": "Test User 1",
    "phone": "1234567890",
    "address": "123 Test St",
    "medical_class": "Class 1",
    "medical_expiry": (datetime.now() + timedelta(days=365)).isoformat(),
    "ratings": "Private Pilot",
    "endorsements": "None",
    "flight_reviews": "None",
    "currency": "Current",
    "notes": "Test notes",
    "is_active": True,
    "is_superuser": False
}

test_aircraft_data = {
    "registration": "N12345",
    "make_model": "Cessna 172",
    "year": 2020,
    "serial_number": "17201234",
    "total_time": 1000,
    "last_maintenance": (datetime.now() - timedelta(days=30)).isoformat(),
    "next_maintenance": (datetime.now() + timedelta(days=30)).isoformat(),
    "status": "Available",
    "category": "airplane",
    "class_type": "single-engine land",
    "notes": "Test aircraft"
}

test_instructor_data = {
    "email": "instructor1@example.com",
    "full_name": "John Doe",
    "phone": "1234567890",
    "ratings": "CFI, CFII, MEI",
    "endorsements": "Complex, High Performance",
    "flight_reviews": "Current",
    "currency": "Current",
    "availability": "Mon-Fri 9am-5pm",
    "notes": "Test instructor"
}

test_flight_data = {
    "student_id": 1,
    "instructor_id": 1,
    "aircraft_id": 1,
    "flight_type": "TRAINING",
    "status": "SCHEDULED",
    "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
    "end_time": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
    "notes": "Test flight"
}

# User tests
def test_create_user(client):
    user_data = test_user_data.copy()
    user_data["email"] = "test1@example.com"
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data

def test_create_user_duplicate_email(client):
    # First create a user
    user_data = test_user_data.copy()
    user_data["email"] = "test2@example.com"
    client.post("/api/v1/users/", json=user_data)
    # Try to create another user with the same email
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_get_users(client):
    # Create test users
    user_data1 = test_user_data.copy()
    user_data1["email"] = "test3@example.com"
    user_data1["full_name"] = "Test User 3"
    user_data2 = test_user_data.copy()
    user_data2["email"] = "test4@example.com"
    user_data2["full_name"] = "Test User 4"
    
    client.post("/api/v1/users/", json=user_data1)
    client.post("/api/v1/users/", json=user_data2)
    
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_user(client):
    # Create test user
    user_data = test_user_data.copy()
    user_data["email"] = "test5@example.com"
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]

def test_update_user(client):
    # First create a user
    user_data = test_user_data.copy()
    user_data["email"] = "test6@example.com"
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Update data
    update_data = user_data.copy()
    update_data["full_name"] = "Updated Name"
    
    # Update the user
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"

def test_delete_user(client):
    # First create a user
    user_data = test_user_data.copy()
    user_data["email"] = "test7@example.com"
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Delete the user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404

# Aircraft tests
def test_create_aircraft(client):
    aircraft_data = test_aircraft_data.copy()
    aircraft_data["registration"] = "N12345"
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    assert response.status_code == 201
    data = response.json()
    assert data["registration"] == aircraft_data["registration"]
    assert data["make_model"] == aircraft_data["make_model"]
    assert "id" in data

def test_create_aircraft_duplicate_registration(client):
    # First create an aircraft
    aircraft_data = test_aircraft_data.copy()
    aircraft_data["registration"] = "N54321"
    client.post("/api/v1/aircraft/", json=aircraft_data)
    # Try to create another aircraft with the same registration
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Registration already registered"

def test_get_aircraft(client):
    # First create an aircraft
    aircraft_data = test_aircraft_data.copy()
    aircraft_data["registration"] = "N67890"
    create_response = client.post("/api/v1/aircraft/", json=aircraft_data)
    aircraft_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/aircraft/{aircraft_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["registration"] == aircraft_data["registration"]
    assert data["make_model"] == aircraft_data["make_model"]

def test_update_aircraft(client):
    # First create an aircraft
    aircraft_data = test_aircraft_data.copy()
    aircraft_data["registration"] = "N09876"
    create_response = client.post("/api/v1/aircraft/", json=aircraft_data)
    aircraft_id = create_response.json()["id"]
    
    # Update data
    update_data = aircraft_data.copy()
    update_data["notes"] = "Updated notes"
    
    # Update the aircraft
    response = client.put(f"/api/v1/aircraft/{aircraft_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["notes"] == "Updated notes"

def test_delete_aircraft(client):
    # First create an aircraft
    aircraft_data = test_aircraft_data.copy()
    aircraft_data["registration"] = "N11111"
    create_response = client.post("/api/v1/aircraft/", json=aircraft_data)
    aircraft_id = create_response.json()["id"]
    
    # Delete the aircraft
    response = client.delete(f"/api/v1/aircraft/{aircraft_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/aircraft/{aircraft_id}")
    assert get_response.status_code == 404

# Instructor tests
def test_create_instructor(client):
    instructor_data = test_instructor_data.copy()
    instructor_data["email"] = "instructor1@example.com"
    response = client.post("/api/v1/instructors/", json=instructor_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == instructor_data["email"]
    assert data["full_name"] == instructor_data["full_name"]
    assert "id" in data

def test_create_instructor_duplicate_email(client):
    # First create an instructor
    instructor_data = test_instructor_data.copy()
    instructor_data["email"] = "instructor2@example.com"
    client.post("/api/v1/instructors/", json=instructor_data)
    # Try to create another instructor with the same email
    response = client.post("/api/v1/instructors/", json=instructor_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_get_instructor(client):
    # First create an instructor
    instructor_data = test_instructor_data.copy()
    instructor_data["email"] = "instructor3@example.com"
    create_response = client.post("/api/v1/instructors/", json=instructor_data)
    instructor_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/instructors/{instructor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == instructor_data["email"]
    assert data["full_name"] == instructor_data["full_name"]

def test_update_instructor(client):
    # First create an instructor
    instructor_data = test_instructor_data.copy()
    instructor_data["email"] = "instructor4@example.com"
    create_response = client.post("/api/v1/instructors/", json=instructor_data)
    instructor_id = create_response.json()["id"]
    
    # Update data
    update_data = instructor_data.copy()
    update_data["notes"] = "Updated notes"
    
    # Update the instructor
    response = client.put(f"/api/v1/instructors/{instructor_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["notes"] == "Updated notes"

def test_delete_instructor(client):
    # First create an instructor
    instructor_data = test_instructor_data.copy()
    instructor_data["email"] = "instructor5@example.com"
    create_response = client.post("/api/v1/instructors/", json=instructor_data)
    instructor_id = create_response.json()["id"]
    
    # Delete the instructor
    response = client.delete(f"/api/v1/instructors/{instructor_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/instructors/{instructor_id}")
    assert get_response.status_code == 404

# Flight tests
def test_create_flight(client):
    # First create required entities
    user_data = test_user_data.copy()
    user_data["email"] = "test8@example.com"
    user_response = client.post("/api/v1/users/", json=user_data)
    
    instructor_data = test_instructor_data.copy()
    instructor_data["email"] = "instructor6@example.com"
    instructor_response = client.post("/api/v1/instructors/", json=instructor_data)
    
    aircraft_data = test_aircraft_data.copy()
    aircraft_data["registration"] = "N22222"
    aircraft_response = client.post("/api/v1/aircraft/", json=aircraft_data)
    
    flight_data = test_flight_data.copy()
    flight_data["student_id"] = user_response.json()["id"]
    flight_data["instructor_id"] = instructor_response.json()["id"]
    flight_data["aircraft_id"] = aircraft_response.json()["id"]
    
    response = client.post("/api/v1/flights/", json=flight_data)
    assert response.status_code == 201
    data = response.json()
    assert data["student_id"] == flight_data["student_id"]
    assert data["instructor_id"] == flight_data["instructor_id"]
    assert data["aircraft_id"] == flight_data["aircraft_id"]
    assert "id" in data

def test_get_flight(client):
    # First create required entities
    user_data = test_user_data.copy()
    user_data["email"] = "test9@example.com"
    user_response = client.post("/api/v1/users/", json=user_data)
    
    instructor_data = test_instructor_data.copy()
    instructor_data["email"] = "instructor7@example.com"
    instructor_response = client.post("/api/v1/instructors/", json=instructor_data)
    
    aircraft_data = test_aircraft_data.copy()
    aircraft_data["registration"] = "N33333"
    aircraft_response = client.post("/api/v1/aircraft/", json=aircraft_data)
    
    flight_data = test_flight_data.copy()
    flight_data["student_id"] = user_response.json()["id"]
    flight_data["instructor_id"] = instructor_response.json()["id"]
    flight_data["aircraft_id"] = aircraft_response.json()["id"]
    
    create_response = client.post("/api/v1/flights/", json=flight_data)
    flight_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/flights/{flight_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == flight_data["student_id"]
    assert data["instructor_id"] == flight_data["instructor_id"]
    assert data["aircraft_id"] == flight_data["aircraft_id"]

def test_update_flight(client):
    # First create required entities
    user_data = test_user_data.copy()
    user_data["email"] = "test10@example.com"
    user_response = client.post("/api/v1/users/", json=user_data)
    
    instructor_data = test_instructor_data.copy()
    instructor_data["email"] = "instructor8@example.com"
    instructor_response = client.post("/api/v1/instructors/", json=instructor_data)
    
    aircraft_data = test_aircraft_data.copy()
    aircraft_data["registration"] = "N44444"
    aircraft_response = client.post("/api/v1/aircraft/", json=aircraft_data)
    
    flight_data = test_flight_data.copy()
    flight_data["student_id"] = user_response.json()["id"]
    flight_data["instructor_id"] = instructor_response.json()["id"]
    flight_data["aircraft_id"] = aircraft_response.json()["id"]
    
    create_response = client.post("/api/v1/flights/", json=flight_data)
    flight_id = create_response.json()["id"]
    
    # Update data
    update_data = flight_data.copy()
    update_data["notes"] = "Updated notes"
    
    # Update the flight
    response = client.put(f"/api/v1/flights/{flight_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["notes"] == "Updated notes"

def test_delete_flight(client):
    # First create required entities
    user_data = test_user_data.copy()
    user_data["email"] = "test11@example.com"
    user_response = client.post("/api/v1/users/", json=user_data)
    
    instructor_data = test_instructor_data.copy()
    instructor_data["email"] = "instructor9@example.com"
    instructor_response = client.post("/api/v1/instructors/", json=instructor_data)
    
    aircraft_data = test_aircraft_data.copy()
    aircraft_data["registration"] = "N55555"
    aircraft_response = client.post("/api/v1/aircraft/", json=aircraft_data)
    
    flight_data = test_flight_data.copy()
    flight_data["student_id"] = user_response.json()["id"]
    flight_data["instructor_id"] = instructor_response.json()["id"]
    flight_data["aircraft_id"] = aircraft_response.json()["id"]
    
    create_response = client.post("/api/v1/flights/", json=flight_data)
    flight_id = create_response.json()["id"]
    
    # Delete the flight
    response = client.delete(f"/api/v1/flights/{flight_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/flights/{flight_id}")
    assert get_response.status_code == 404 