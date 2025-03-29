from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .database import get_db
from . import crud, models, schemas

router = APIRouter(prefix="/api/v1")

# User endpoints
@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.put("/users/{user_id}", response_model=schemas.User)
def update_user_endpoint(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

# Aircraft endpoints
@router.post("/aircraft/", response_model=schemas.Aircraft, status_code=status.HTTP_201_CREATED)
def create_aircraft_endpoint(aircraft: schemas.AircraftCreate, db: Session = Depends(get_db)):
    db_aircraft = crud.get_aircraft_by_registration(db, registration=aircraft.registration)
    if db_aircraft:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration already registered"
        )
    return crud.create_aircraft(db=db, aircraft=aircraft)

@router.get("/aircraft/", response_model=List[schemas.Aircraft])
def read_aircrafts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_aircrafts(db, skip=skip, limit=limit)

@router.get("/aircraft/{aircraft_id}", response_model=schemas.Aircraft)
def read_aircraft(aircraft_id: int, db: Session = Depends(get_db)):
    db_aircraft = crud.get_aircraft(db, aircraft_id=aircraft_id)
    if db_aircraft is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aircraft not found"
        )
    return db_aircraft

@router.put("/aircraft/{aircraft_id}", response_model=schemas.Aircraft)
def update_aircraft_endpoint(aircraft_id: int, aircraft: schemas.AircraftCreate, db: Session = Depends(get_db)):
    db_aircraft = crud.update_aircraft(db=db, aircraft_id=aircraft_id, aircraft=aircraft)
    if db_aircraft is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aircraft not found"
        )
    return db_aircraft

@router.delete("/aircraft/{aircraft_id}", response_model=schemas.Aircraft)
def delete_aircraft_endpoint(aircraft_id: int, db: Session = Depends(get_db)):
    db_aircraft = crud.delete_aircraft(db=db, aircraft_id=aircraft_id)
    if db_aircraft is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aircraft not found"
        )
    return db_aircraft

# Instructor endpoints
@router.post("/instructors/", response_model=schemas.Instructor, status_code=status.HTTP_201_CREATED)
def create_instructor_endpoint(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = crud.get_instructor_by_email(db, email=instructor.email)
    if db_instructor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_instructor(db=db, instructor=instructor)

@router.get("/instructors/", response_model=List[schemas.Instructor])
def read_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_instructors(db, skip=skip, limit=limit)

@router.get("/instructors/{instructor_id}", response_model=schemas.Instructor)
def read_instructor(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = crud.get_instructor(db, instructor_id=instructor_id)
    if db_instructor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    return db_instructor

@router.put("/instructors/{instructor_id}", response_model=schemas.Instructor)
def update_instructor_endpoint(instructor_id: int, instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = crud.update_instructor(db=db, instructor_id=instructor_id, instructor=instructor)
    if db_instructor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    return db_instructor

@router.delete("/instructors/{instructor_id}", response_model=schemas.Instructor)
def delete_instructor_endpoint(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = crud.delete_instructor(db=db, instructor_id=instructor_id)
    if db_instructor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    return db_instructor

# Flight endpoints
@router.post("/flights/", response_model=schemas.Flight, status_code=status.HTTP_201_CREATED)
def create_flight_endpoint(flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    # Verify that student, instructor, and aircraft exist
    student = crud.get_user(db, user_id=flight.student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    instructor = crud.get_instructor(db, instructor_id=flight.instructor_id)
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    
    aircraft = crud.get_aircraft(db, aircraft_id=flight.aircraft_id)
    if not aircraft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aircraft not found"
        )
    
    return crud.create_flight(db=db, flight=flight)

@router.get("/flights/", response_model=List[schemas.Flight])
def read_flights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_flights(db, skip=skip, limit=limit)

@router.get("/flights/{flight_id}", response_model=schemas.Flight)
def read_flight(flight_id: int, db: Session = Depends(get_db)):
    db_flight = crud.get_flight(db, flight_id=flight_id)
    if db_flight is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    return db_flight

@router.put("/flights/{flight_id}", response_model=schemas.Flight)
def update_flight_endpoint(flight_id: int, flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    # Verify that student, instructor, and aircraft exist
    student = crud.get_user(db, user_id=flight.student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    instructor = crud.get_instructor(db, instructor_id=flight.instructor_id)
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    
    aircraft = crud.get_aircraft(db, aircraft_id=flight.aircraft_id)
    if not aircraft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aircraft not found"
        )
    
    db_flight = crud.update_flight(db=db, flight_id=flight_id, flight=flight)
    if db_flight is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    return db_flight

@router.delete("/flights/{flight_id}", response_model=schemas.Flight)
def delete_flight_endpoint(flight_id: int, db: Session = Depends(get_db)):
    db_flight = crud.delete_flight(db=db, flight_id=flight_id)
    if db_flight is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    return db_flight 