import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import User, Flight, Aircraft, FlightType, FlightStatus

def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User",
            "is_active": True,
            "is_superuser": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert data["is_active"] is True
    assert data["is_superuser"] is False

def test_create_aircraft(client: TestClient):
    response = client.post(
        "/aircraft/",
        json={
            "registration": "N12345",
            "make_model": "Cessna 172",
            "category": "airplane",
            "class_type": "single-engine land",
            "is_active": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["registration"] == "N12345"
    assert data["make_model"] == "Cessna 172"
    assert data["category"] == "airplane"
    assert data["class_type"] == "single-engine land"
    assert data["is_active"] is True

def test_create_flight(client: TestClient, test_db: Session):
    # Create required aircraft first
    aircraft = Aircraft(
        registration="N12345",
        make_model="Cessna 172",
        category="airplane",
        class_type="single-engine land",
        is_active=True
    )
    test_db.add(aircraft)
    test_db.commit()

    # Create required user first
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )
    test_db.add(user)
    test_db.commit()

    response = client.post(
        "/flights/",
        json={
            "aircraft_id": aircraft.id,
            "student_id": user.id,
            "instructor_id": user.id,
            "flight_type": FlightType.DUAL,
            "status": FlightStatus.SCHEDULED,
            "start_time": "2024-03-20T10:00:00",
            "end_time": "2024-03-20T11:00:00",
            "remarks": "Test flight"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["aircraft_id"] == aircraft.id
    assert data["student_id"] == user.id
    assert data["instructor_id"] == user.id
    assert data["flight_type"] == FlightType.DUAL
    assert data["status"] == FlightStatus.SCHEDULED
    assert data["start_time"] == "2024-03-20T10:00:00"
    assert data["end_time"] == "2024-03-20T11:00:00"
    assert data["remarks"] == "Test flight" 