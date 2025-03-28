import pytest
from sqlalchemy.orm import Session
from models import User, Flight, Aircraft, FlightType, FlightStatus

def test_create_user(test_db: Session):
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True
    assert user.is_superuser is False

def test_create_aircraft(test_db: Session):
    aircraft = Aircraft(
        registration="N12345",
        make_model="Cessna 172",
        category="airplane",
        class_type="single-engine land",
        is_active=True
    )
    test_db.add(aircraft)
    test_db.commit()
    test_db.refresh(aircraft)

    assert aircraft.id is not None
    assert aircraft.registration == "N12345"
    assert aircraft.make_model == "Cessna 172"
    assert aircraft.category == "airplane"
    assert aircraft.class_type == "single-engine land"
    assert aircraft.is_active is True

def test_create_flight(test_db: Session):
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

    flight = Flight(
        aircraft_id=aircraft.id,
        student_id=user.id,
        instructor_id=user.id,
        flight_type=FlightType.DUAL,
        status=FlightStatus.SCHEDULED,
        start_time="2024-03-20T10:00:00",
        end_time="2024-03-20T11:00:00",
        remarks="Test flight"
    )
    test_db.add(flight)
    test_db.commit()
    test_db.refresh(flight)

    assert flight.id is not None
    assert flight.aircraft_id == aircraft.id
    assert flight.student_id == user.id
    assert flight.instructor_id == user.id
    assert flight.flight_type == FlightType.DUAL
    assert flight.status == FlightStatus.SCHEDULED
    assert flight.start_time == "2024-03-20T10:00:00"
    assert flight.end_time == "2024-03-20T11:00:00"
    assert flight.remarks == "Test flight" 