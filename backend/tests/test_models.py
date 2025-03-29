import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models import User, Aircraft, Instructor, Flight, FlightType, FlightStatus

def test_create_user(db_session):
    medical_expiry = datetime.now() + timedelta(days=365)
    user = User(
        email="test@example.com",
        hashed_password="testpassword",
        is_active=True,
        is_superuser=False,
        first_name="Test",
        last_name="User",
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
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.phone == "1234567890"
    assert user.address == "123 Test St"
    assert user.medical_class == "Class 1"
    assert user.medical_expiry == medical_expiry
    assert user.ratings == "Private Pilot"
    assert user.notes == "Test notes"
    assert user.created_at is not None
    assert user.updated_at is not None

def test_create_aircraft(db_session):
    aircraft = Aircraft(
        registration="N12345",
        type="Cessna",
        model="172",
        year=2020,
        serial_number="17201234",
        total_time=1000,
        last_maintenance=datetime.now() - timedelta(days=30),
        next_maintenance=datetime.now() + timedelta(days=30),
        status="Active",
        category="airplane",
        class_type="single-engine land",
        is_active=True,
        notes="Test aircraft"
    )
    db_session.add(aircraft)
    db_session.commit()
    assert aircraft.id is not None
    assert aircraft.registration == "N12345"
    assert aircraft.type == "Cessna"
    assert aircraft.model == "172"
    assert aircraft.year == 2020
    assert aircraft.serial_number == "17201234"
    assert aircraft.total_time == 1000
    assert aircraft.status == "Active"
    assert aircraft.category == "airplane"
    assert aircraft.class_type == "single-engine land"
    assert aircraft.is_active is True
    assert aircraft.notes == "Test aircraft"
    assert aircraft.created_at is not None
    assert aircraft.updated_at is not None

def test_create_instructor(db_session):
    instructor = Instructor(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="1234567890",
        ratings="CFI, CFII, MEI",
        endorsements="Complex, High Performance",
        flight_reviews="Current",
        currency="Current",
        availability="Mon-Fri 9am-5pm",
        notes="Test instructor"
    )
    db_session.add(instructor)
    db_session.commit()
    assert instructor.id is not None
    assert instructor.first_name == "John"
    assert instructor.last_name == "Doe"
    assert instructor.email == "john@example.com"
    assert instructor.phone == "1234567890"
    assert instructor.ratings == "CFI, CFII, MEI"
    assert instructor.endorsements == "Complex, High Performance"
    assert instructor.flight_reviews == "Current"
    assert instructor.currency == "Current"
    assert instructor.availability == "Mon-Fri 9am-5pm"
    assert instructor.notes == "Test instructor"
    assert instructor.created_at is not None
    assert instructor.updated_at is not None

def test_create_flight(db_session):
    # Create required entities first
    user = User(
        email="student@example.com",
        hashed_password="testpassword",
        is_active=True,
        is_superuser=False,
        first_name="Test",
        last_name="Student",
        phone="1234567890",
        address="123 Test St",
        medical_class="Class 1",
        medical_expiry=datetime.now() + timedelta(days=365),
        ratings="Private Pilot",
        endorsements="None",
        flight_reviews="None",
        currency="Current",
        notes="Test student"
    )
    db_session.add(user)
    db_session.commit()

    instructor = Instructor(
        first_name="Test",
        last_name="Instructor",
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

    aircraft = Aircraft(
        registration="N12345",
        type="Cessna",
        model="172",
        year=2020,
        serial_number="12345",
        total_time=1000,
        last_maintenance=datetime.now() - timedelta(days=30),
        next_maintenance=datetime.now() + timedelta(days=30),
        status="Active",
        category="airplane",
        class_type="single-engine land",
        is_active=True,
        notes="Test aircraft"
    )
    db_session.add(aircraft)
    db_session.commit()

    # Create flight
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
        duration=timedelta(hours=2),
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
    assert flight.duration == timedelta(hours=2)
    assert flight.notes == "Test flight"
    assert flight.created_at is not None
    assert flight.updated_at is not None 