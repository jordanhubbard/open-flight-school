import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from . import models
from .database import Base

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test database tables
Base.metadata.create_all(bind=engine)

# Fixture to get a test database session
@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# Test User model
def test_create_user(db_session):
    user = models.User(
        email="test@example.com",
        hashed_password="testpassword",
        is_active=True,
        is_superuser=False,
        full_name="Test User",
        phone="1234567890",
        address="123 Test St",
        medical_class="Class 1",
        medical_expiry="2023-12-31",
        ratings="Private Pilot",
        endorsements="None",
        flight_reviews="None",
        currency="Current",
        notes="Test notes"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"

# Test Aircraft model
def test_create_aircraft(db_session):
    aircraft = models.Aircraft(
        registration="N12345",
        make_model="Cessna 172",
        year=2020,
        serial_number="12345",
        total_time=1000,
        last_maintenance="2023-01-01",
        next_maintenance="2024-01-01",
        status="Available",
        notes="Test aircraft"
    )
    db_session.add(aircraft)
    db_session.commit()
    db_session.refresh(aircraft)
    assert aircraft.registration == "N12345"
    assert aircraft.make_model == "Cessna 172"

# Test Instructor model
def test_create_instructor(db_session):
    instructor = models.Instructor(
        name="Test Instructor",
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
    db_session.refresh(instructor)
    assert instructor.email == "instructor@example.com"
    assert instructor.name == "Test Instructor"

# Test Booking model
def test_create_booking(db_session):
    user = models.User(
        email="test@example.com",
        hashed_password="testpassword",
        is_active=True,
        is_superuser=False,
        full_name="Test User",
        phone="1234567890",
        address="123 Test St",
        medical_class="Class 1",
        medical_expiry="2023-12-31",
        ratings="Private Pilot",
        endorsements="None",
        flight_reviews="None",
        currency="Current",
        notes="Test notes"
    )
    db_session.add(user)
    db_session.commit()

    aircraft = models.Aircraft(
        registration="N12345",
        make_model="Cessna 172",
        year=2020,
        serial_number="12345",
        total_time=1000,
        last_maintenance="2023-01-01",
        next_maintenance="2024-01-01",
        status="Available",
        notes="Test aircraft"
    )
    db_session.add(aircraft)
    db_session.commit()

    instructor = models.Instructor(
        name="Test Instructor",
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

    booking = models.Booking(
        student_id=user.id,
        instructor_id=instructor.id,
        aircraft_id=aircraft.id,
        start_time="2023-12-31T10:00:00",
        end_time="2023-12-31T12:00:00",
        status="Scheduled",
        notes="Test booking"
    )
    db_session.add(booking)
    db_session.commit()
    db_session.refresh(booking)
    assert booking.student_id == user.id
    assert booking.instructor_id == instructor.id
    assert booking.aircraft_id == aircraft.id 