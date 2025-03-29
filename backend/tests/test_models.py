import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy.orm import Session
from models import User, Aircraft, Instructor, Flight, FlightType, FlightStatus
from datetime import datetime, timedelta

def test_create_user(db_session):
    medical_expiry = datetime.now() + timedelta(days=365)
    user = User(
        email="test@example.com",
        hashed_password="testpassword",
        is_active=True,
        is_superuser=False,
        full_name="Test User",
        phone="1234567890",
        address="123 Test St",
        medical_class="Class 1",
        medical_expiry=medical_expiry,
        ratings="Private Pilot",
        endorsements="None",
        flight_reviews="None",
        currency="Current",
        notes="Test notes"
    )
    db_session.add(user)
    db_session.commit()
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.phone == "1234567890"
    assert user.address == "123 Test St"
    assert user.medical_class == "Class 1"
    assert user.medical_expiry == medical_expiry
    assert user.ratings == "Private Pilot"
    assert user.notes == "Test notes"
    assert user.created_at is not None
    assert user.updated_at is not None

def test_create_aircraft(db_session):
    last_maintenance = datetime.now() - timedelta(days=30)
    next_maintenance = datetime.now() + timedelta(days=30)
    aircraft = Aircraft(
        registration="N12345",
        make_model="Cessna 172",
        year=2020,
        serial_number="12345",
        total_time=1000,
        last_maintenance=last_maintenance,
        next_maintenance=next_maintenance,
        status="Available",
        category="airplane",
        class_type="single-engine land",
        is_active=True,
        notes="Test aircraft"
    )
    db_session.add(aircraft)
    db_session.commit()
    assert aircraft.id is not None
    assert aircraft.registration == "N12345"
    assert aircraft.make_model == "Cessna 172"
    assert aircraft.year == 2020
    assert aircraft.serial_number == "12345"
    assert aircraft.total_time == 1000
    assert aircraft.last_maintenance == last_maintenance
    assert aircraft.next_maintenance == next_maintenance
    assert aircraft.status == "Available"
    assert aircraft.category == "airplane"
    assert aircraft.class_type == "single-engine land"
    assert aircraft.is_active is True
    assert aircraft.notes == "Test aircraft"
    assert aircraft.created_at is not None
    assert aircraft.updated_at is not None

def test_create_instructor(db_session):
    instructor = Instructor(
        full_name="Test Instructor",
        email="instructor@example.com",
        phone="0987654321",
        ratings="CFI",
        endorsements="None",
        flight_reviews="None",
        currency="Current",
        availability="Full-time",
        notes="Test instructor"
    )
    db_session.add(instructor)
    db_session.commit()
    assert instructor.id is not None
    assert instructor.full_name == "Test Instructor"
    assert instructor.email == "instructor@example.com"
    assert instructor.phone == "0987654321"
    assert instructor.ratings == "CFI"
    assert instructor.endorsements == "None"
    assert instructor.flight_reviews == "None"
    assert instructor.currency == "Current"
    assert instructor.availability == "Full-time"
    assert instructor.notes == "Test instructor"
    assert instructor.created_at is not None
    assert instructor.updated_at is not None

def test_create_booking(db_session):
    medical_expiry = datetime.now() + timedelta(days=365)
    user = User(
        email="test@example.com",
        hashed_password="testpassword",
        is_active=True,
        is_superuser=False,
        full_name="Test User",
        phone="1234567890",
        address="123 Test St",
        medical_class="Class 1",
        medical_expiry=medical_expiry,
        ratings="Private Pilot",
        endorsements="None",
        flight_reviews="None",
        currency="Current",
        notes="Test notes"
    )
    db_session.add(user)

    instructor = Instructor(
        full_name="Test Instructor",
        email="instructor@example.com",
        phone="0987654321",
        ratings="CFI",
        endorsements="None",
        flight_reviews="None",
        currency="Current",
        availability="Full-time",
        notes="Test instructor"
    )
    db_session.add(instructor)

    last_maintenance = datetime.now() - timedelta(days=30)
    next_maintenance = datetime.now() + timedelta(days=30)
    aircraft = Aircraft(
        registration="N12345",
        make_model="Cessna 172",
        year=2020,
        serial_number="12345",
        total_time=1000,
        last_maintenance=last_maintenance,
        next_maintenance=next_maintenance,
        status="Available",
        category="airplane",
        class_type="single-engine land",
        is_active=True,
        notes="Test aircraft"
    )
    db_session.add(aircraft)
    db_session.commit()

    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    flight = Flight(
        student_id=user.id,
        instructor_id=instructor.id,
        aircraft_id=aircraft.id,
        flight_type=FlightType.TRAINING,
        status=FlightStatus.SCHEDULED,
        start_time=start_time,
        end_time=end_time,
        notes="Test flight"
    )
    db_session.add(flight)
    db_session.commit()
    assert flight.id is not None
    assert flight.student_id == user.id
    assert flight.instructor_id == instructor.id
    assert flight.aircraft_id == aircraft.id
    assert flight.flight_type == FlightType.TRAINING
    assert flight.status == FlightStatus.SCHEDULED
    assert flight.start_time == start_time
    assert flight.end_time == end_time
    assert flight.notes == "Test flight"
    assert flight.created_at is not None
    assert flight.updated_at is not None