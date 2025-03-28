from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import SessionLocal

router = APIRouter()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User endpoints
@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Aircraft endpoints
@router.post("/aircraft/", response_model=schemas.Aircraft)
def create_aircraft(aircraft: schemas.AircraftCreate, db: Session = Depends(get_db)):
    db_aircraft = crud.get_aircraft_by_registration(db, registration=aircraft.registration)
    if db_aircraft:
        raise HTTPException(status_code=400, detail="Registration already registered")
    return crud.create_aircraft(db=db, aircraft=aircraft)

@router.get("/aircraft/", response_model=List[schemas.Aircraft])
def read_aircrafts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    aircrafts = crud.get_aircrafts(db, skip=skip, limit=limit)
    return aircrafts

@router.get("/aircraft/{aircraft_id}", response_model=schemas.Aircraft)
def read_aircraft(aircraft_id: int, db: Session = Depends(get_db)):
    db_aircraft = crud.get_aircraft(db, aircraft_id=aircraft_id)
    if db_aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return db_aircraft

@router.put("/aircraft/{aircraft_id}", response_model=schemas.Aircraft)
def update_aircraft(aircraft_id: int, aircraft: schemas.AircraftCreate, db: Session = Depends(get_db)):
    db_aircraft = crud.update_aircraft(db=db, aircraft_id=aircraft_id, aircraft=aircraft)
    if db_aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return db_aircraft

@router.delete("/aircraft/{aircraft_id}", response_model=schemas.Aircraft)
def delete_aircraft(aircraft_id: int, db: Session = Depends(get_db)):
    db_aircraft = crud.delete_aircraft(db=db, aircraft_id=aircraft_id)
    if db_aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return db_aircraft

# Instructor endpoints
@router.post("/instructors/", response_model=schemas.Instructor)
def create_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = crud.get_instructor_by_email(db, email=instructor.email)
    if db_instructor:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_instructor(db=db, instructor=instructor)

@router.get("/instructors/", response_model=List[schemas.Instructor])
def read_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    instructors = crud.get_instructors(db, skip=skip, limit=limit)
    return instructors

@router.get("/instructors/{instructor_id}", response_model=schemas.Instructor)
def read_instructor(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = crud.get_instructor(db, instructor_id=instructor_id)
    if db_instructor is None:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return db_instructor

@router.put("/instructors/{instructor_id}", response_model=schemas.Instructor)
def update_instructor(instructor_id: int, instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = crud.update_instructor(db=db, instructor_id=instructor_id, instructor=instructor)
    if db_instructor is None:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return db_instructor

@router.delete("/instructors/{instructor_id}", response_model=schemas.Instructor)
def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = crud.delete_instructor(db=db, instructor_id=instructor_id)
    if db_instructor is None:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return db_instructor

# Booking endpoints
@router.post("/bookings/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=booking)

@router.get("/bookings/", response_model=List[schemas.Booking])
def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings

@router.get("/bookings/{booking_id}", response_model=schemas.Booking)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.put("/bookings/{booking_id}", response_model=schemas.Booking)
def update_booking(booking_id: int, booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    db_booking = crud.update_booking(db=db, booking_id=booking_id, booking=booking)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.delete("/bookings/{booking_id}", response_model=schemas.Booking)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = crud.delete_booking(db=db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking 