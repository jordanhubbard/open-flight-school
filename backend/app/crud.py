from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from passlib.context import CryptContext
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def parse_datetime(date_str: str | datetime) -> datetime:
    """Parse a datetime string or datetime object into a datetime object."""
    if isinstance(date_str, datetime):
        return date_str
    try:
        return datetime.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None

# User CRUD operations
def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = pwd_context.hash(user.password)
    user_data = user.model_dump(exclude={"password"})
    if "medical_expiry" in user_data:
        user_data["medical_expiry"] = parse_datetime(user_data["medical_expiry"])
    db_user = models.User(hashed_password=hashed_password, **user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> models.User | None:
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> models.User | None:
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

# Aircraft CRUD operations
def get_aircraft(db: Session, aircraft_id: int) -> models.Aircraft:
    return db.query(models.Aircraft).filter(models.Aircraft.id == aircraft_id).first()

def get_aircraft_by_registration(db: Session, registration: str) -> models.Aircraft:
    return db.query(models.Aircraft).filter(models.Aircraft.registration == registration).first()

def get_aircrafts(db: Session, skip: int = 0, limit: int = 100) -> list[models.Aircraft]:
    return db.query(models.Aircraft).offset(skip).limit(limit).all()

def create_aircraft(db: Session, aircraft: schemas.AircraftCreate) -> models.Aircraft:
    aircraft_data = aircraft.model_dump()
    if "last_maintenance" in aircraft_data:
        aircraft_data["last_maintenance"] = parse_datetime(aircraft_data["last_maintenance"])
    if "next_maintenance" in aircraft_data:
        aircraft_data["next_maintenance"] = parse_datetime(aircraft_data["next_maintenance"])
    db_aircraft = models.Aircraft(**aircraft_data)
    db.add(db_aircraft)
    db.commit()
    db.refresh(db_aircraft)
    return db_aircraft

def update_aircraft(db: Session, aircraft_id: int, aircraft: schemas.AircraftUpdate) -> models.Aircraft | None:
    db_aircraft = get_aircraft(db, aircraft_id)
    if db_aircraft is None:
        return None
    
    for key, value in aircraft.dict(exclude_unset=True).items():
        setattr(db_aircraft, key, value)
    
    db.commit()
    db.refresh(db_aircraft)
    return db_aircraft

def delete_aircraft(db: Session, aircraft_id: int) -> models.Aircraft | None:
    db_aircraft = get_aircraft(db, aircraft_id)
    if db_aircraft is None:
        return None
    db.delete(db_aircraft)
    db.commit()
    return db_aircraft

# Instructor CRUD operations
def get_instructor(db: Session, instructor_id: int) -> models.Instructor:
    return db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()

def get_instructor_by_email(db: Session, email: str) -> models.Instructor:
    return db.query(models.Instructor).filter(models.Instructor.email == email).first()

def get_instructors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Instructor]:
    return db.query(models.Instructor).offset(skip).limit(limit).all()

def create_instructor(db: Session, instructor: schemas.InstructorCreate) -> models.Instructor:
    db_instructor = models.Instructor(**instructor.model_dump())
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

def update_instructor(db: Session, instructor_id: int, instructor: schemas.InstructorUpdate) -> models.Instructor | None:
    db_instructor = get_instructor(db, instructor_id)
    if db_instructor is None:
        return None
    
    for key, value in instructor.dict(exclude_unset=True).items():
        setattr(db_instructor, key, value)
    
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

def delete_instructor(db: Session, instructor_id: int) -> models.Instructor | None:
    db_instructor = get_instructor(db, instructor_id)
    if db_instructor is None:
        return None
    db.delete(db_instructor)
    db.commit()
    return db_instructor

# Flight CRUD operations
def get_flight(db: Session, flight_id: int) -> models.Flight:
    return db.query(models.Flight).filter(models.Flight.id == flight_id).first()

def get_flights(db: Session, skip: int = 0, limit: int = 100) -> list[models.Flight]:
    return db.query(models.Flight).offset(skip).limit(limit).all()

def create_flight(db: Session, flight: schemas.FlightCreate) -> models.Flight:
    flight_data = flight.model_dump()
    if "start_time" in flight_data:
        flight_data["start_time"] = parse_datetime(flight_data["start_time"])
    if "end_time" in flight_data:
        flight_data["end_time"] = parse_datetime(flight_data["end_time"])
    db_flight = models.Flight(**flight_data)
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

def update_flight(db: Session, flight_id: int, flight: schemas.FlightUpdate) -> models.Flight | None:
    db_flight = get_flight(db, flight_id)
    if db_flight is None:
        return None
    
    for key, value in flight.dict(exclude_unset=True).items():
        setattr(db_flight, key, value)
    
    db.commit()
    db.refresh(db_flight)
    return db_flight

def delete_flight(db: Session, flight_id: int) -> models.Flight | None:
    db_flight = get_flight(db, flight_id)
    if db_flight is None:
        return None
    db.delete(db_flight)
    db.commit()
    return db_flight 