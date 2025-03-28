from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from . import models, schemas

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

# Aircraft CRUD operations
def get_aircraft(db: Session, aircraft_id: int):
    return db.query(models.Aircraft).filter(models.Aircraft.id == aircraft_id).first()

def get_aircraft_by_registration(db: Session, registration: str):
    return db.query(models.Aircraft).filter(models.Aircraft.registration == registration).first()

def get_aircrafts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Aircraft).offset(skip).limit(limit).all()

def create_aircraft(db: Session, aircraft: schemas.AircraftCreate):
    db_aircraft = models.Aircraft(**aircraft.dict())
    db.add(db_aircraft)
    db.commit()
    db.refresh(db_aircraft)
    return db_aircraft

def update_aircraft(db: Session, aircraft_id: int, aircraft: schemas.AircraftCreate):
    db_aircraft = db.query(models.Aircraft).filter(models.Aircraft.id == aircraft_id).first()
    for key, value in aircraft.dict().items():
        setattr(db_aircraft, key, value)
    db.commit()
    db.refresh(db_aircraft)
    return db_aircraft

def delete_aircraft(db: Session, aircraft_id: int):
    db_aircraft = db.query(models.Aircraft).filter(models.Aircraft.id == aircraft_id).first()
    db.delete(db_aircraft)
    db.commit()
    return db_aircraft

# Instructor CRUD operations
def get_instructor(db: Session, instructor_id: int):
    return db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()

def get_instructor_by_email(db: Session, email: str):
    return db.query(models.Instructor).filter(models.Instructor.email == email).first()

def get_instructors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Instructor).offset(skip).limit(limit).all()

def create_instructor(db: Session, instructor: schemas.InstructorCreate):
    db_instructor = models.Instructor(**instructor.dict())
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

def update_instructor(db: Session, instructor_id: int, instructor: schemas.InstructorCreate):
    db_instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    for key, value in instructor.dict().items():
        setattr(db_instructor, key, value)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

def delete_instructor(db: Session, instructor_id: int):
    db_instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    db.delete(db_instructor)
    db.commit()
    return db_instructor

# Booking CRUD operations
def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()

def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking(db: Session, booking_id: int, booking: schemas.BookingCreate):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    for key, value in booking.dict().items():
        setattr(db_booking, key, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    db.delete(db_booking)
    db.commit()
    return db_booking 