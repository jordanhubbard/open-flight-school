from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from passlib.context import CryptContext
from models import User, Aircraft, Instructor, Flight
from schemas import UserCreate, AircraftCreate, InstructorCreate, FlightCreate

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
def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = pwd_context.hash(user.password)
    user_data = user.model_dump(exclude={"password"})
    if "medical_expiry" in user_data:
        user_data["medical_expiry"] = parse_datetime(user_data["medical_expiry"])
    db_user = User(hashed_password=hashed_password, **user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserCreate) -> User | None:
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    
    user_data = user.model_dump(exclude={"password"})
    if user.password:
        user_data["hashed_password"] = pwd_context.hash(user.password)
    if "medical_expiry" in user_data:
        user_data["medical_expiry"] = parse_datetime(user_data["medical_expiry"])
    
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> User | None:
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

# Aircraft CRUD operations
def get_aircraft(db: Session, aircraft_id: int) -> Aircraft:
    return db.query(Aircraft).filter(Aircraft.id == aircraft_id).first()

def get_aircraft_by_registration(db: Session, registration: str) -> Aircraft:
    return db.query(Aircraft).filter(Aircraft.registration == registration).first()

def get_aircrafts(db: Session, skip: int = 0, limit: int = 100) -> list[Aircraft]:
    return db.query(Aircraft).offset(skip).limit(limit).all()

def create_aircraft(db: Session, aircraft: AircraftCreate) -> Aircraft:
    aircraft_data = aircraft.model_dump()
    if "last_maintenance" in aircraft_data:
        aircraft_data["last_maintenance"] = parse_datetime(aircraft_data["last_maintenance"])
    if "next_maintenance" in aircraft_data:
        aircraft_data["next_maintenance"] = parse_datetime(aircraft_data["next_maintenance"])
    db_aircraft = Aircraft(**aircraft_data)
    db.add(db_aircraft)
    db.commit()
    db.refresh(db_aircraft)
    return db_aircraft

def update_aircraft(db: Session, aircraft_id: int, aircraft: AircraftCreate) -> Aircraft | None:
    db_aircraft = get_aircraft(db, aircraft_id)
    if db_aircraft is None:
        return None
    
    aircraft_data = aircraft.model_dump()
    if "last_maintenance" in aircraft_data:
        aircraft_data["last_maintenance"] = parse_datetime(aircraft_data["last_maintenance"])
    if "next_maintenance" in aircraft_data:
        aircraft_data["next_maintenance"] = parse_datetime(aircraft_data["next_maintenance"])
    
    for key, value in aircraft_data.items():
        setattr(db_aircraft, key, value)
    
    db.commit()
    db.refresh(db_aircraft)
    return db_aircraft

def delete_aircraft(db: Session, aircraft_id: int) -> Aircraft | None:
    db_aircraft = get_aircraft(db, aircraft_id)
    if db_aircraft is None:
        return None
    db.delete(db_aircraft)
    db.commit()
    return db_aircraft

# Instructor CRUD operations
def get_instructor(db: Session, instructor_id: int) -> Instructor:
    return db.query(Instructor).filter(Instructor.id == instructor_id).first()

def get_instructor_by_email(db: Session, email: str) -> Instructor:
    return db.query(Instructor).filter(Instructor.email == email).first()

def get_instructors(db: Session, skip: int = 0, limit: int = 100) -> list[Instructor]:
    return db.query(Instructor).offset(skip).limit(limit).all()

def create_instructor(db: Session, instructor: InstructorCreate) -> Instructor:
    db_instructor = Instructor(**instructor.model_dump())
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

def update_instructor(db: Session, instructor_id: int, instructor: InstructorCreate) -> Instructor | None:
    db_instructor = get_instructor(db, instructor_id)
    if db_instructor is None:
        return None
    
    for key, value in instructor.model_dump().items():
        setattr(db_instructor, key, value)
    
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

def delete_instructor(db: Session, instructor_id: int) -> Instructor | None:
    db_instructor = get_instructor(db, instructor_id)
    if db_instructor is None:
        return None
    db.delete(db_instructor)
    db.commit()
    return db_instructor

# Flight CRUD operations
def get_flight(db: Session, flight_id: int) -> Flight:
    return db.query(Flight).filter(Flight.id == flight_id).first()

def get_flights(db: Session, skip: int = 0, limit: int = 100) -> list[Flight]:
    return db.query(Flight).offset(skip).limit(limit).all()

def create_flight(db: Session, flight: FlightCreate) -> Flight:
    flight_data = flight.model_dump()
    if "start_time" in flight_data:
        flight_data["start_time"] = parse_datetime(flight_data["start_time"])
    if "end_time" in flight_data:
        flight_data["end_time"] = parse_datetime(flight_data["end_time"])
    db_flight = Flight(**flight_data)
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

def update_flight(db: Session, flight_id: int, flight: FlightCreate) -> Flight | None:
    db_flight = get_flight(db, flight_id)
    if db_flight is None:
        return None
    
    flight_data = flight.model_dump()
    if "start_time" in flight_data:
        flight_data["start_time"] = parse_datetime(flight_data["start_time"])
    if "end_time" in flight_data:
        flight_data["end_time"] = parse_datetime(flight_data["end_time"])
    
    for key, value in flight_data.items():
        setattr(db_flight, key, value)
    
    db.commit()
    db.refresh(db_flight)
    return db_flight

def delete_flight(db: Session, flight_id: int) -> Flight | None:
    db_flight = get_flight(db, flight_id)
    if db_flight is None:
        return None
    db.delete(db_flight)
    db.commit()
    return db_flight 