from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from crud import (
    get_user, get_user_by_email, get_users, create_user, update_user, delete_user,
    get_aircraft, get_aircraft_by_registration, get_aircrafts, create_aircraft, update_aircraft, delete_aircraft,
    get_instructor, get_instructor_by_email, get_instructors, create_instructor, update_instructor, delete_instructor,
    get_flight, get_flights, create_flight, update_flight, delete_flight
)
from schemas import (
    User, UserCreate,
    Aircraft, AircraftCreate,
    Instructor, InstructorCreate,
    Flight, FlightCreate
)

router = APIRouter()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User endpoints
@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_user(db=db, user=user)

@router.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.put("/users/{user_id}", response_model=User)
def update_user_endpoint(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.delete("/users/{user_id}", response_model=User)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

# Aircraft endpoints
@router.post("/aircraft/", response_model=Aircraft, status_code=status.HTTP_201_CREATED)
def create_aircraft_endpoint(aircraft: AircraftCreate, db: Session = Depends(get_db)):
    db_aircraft = get_aircraft_by_registration(db, registration=aircraft.registration)
    if db_aircraft:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration already registered"
        )
    return create_aircraft(db=db, aircraft=aircraft)

@router.get("/aircraft/", response_model=List[Aircraft])
def read_aircrafts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_aircrafts(db, skip=skip, limit=limit)

@router.get("/aircraft/{aircraft_id}", response_model=Aircraft)
def read_aircraft(aircraft_id: int, db: Session = Depends(get_db)):
    db_aircraft = get_aircraft(db, aircraft_id=aircraft_id)
    if db_aircraft is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aircraft not found"
        )
    return db_aircraft

@router.put("/aircraft/{aircraft_id}", response_model=Aircraft)
def update_aircraft_endpoint(aircraft_id: int, aircraft: AircraftCreate, db: Session = Depends(get_db)):
    db_aircraft = update_aircraft(db=db, aircraft_id=aircraft_id, aircraft=aircraft)
    if db_aircraft is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aircraft not found"
        )
    return db_aircraft

@router.delete("/aircraft/{aircraft_id}", response_model=Aircraft)
def delete_aircraft_endpoint(aircraft_id: int, db: Session = Depends(get_db)):
    db_aircraft = delete_aircraft(db=db, aircraft_id=aircraft_id)
    if db_aircraft is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aircraft not found"
        )
    return db_aircraft

# Instructor endpoints
@router.post("/instructors/", response_model=Instructor, status_code=status.HTTP_201_CREATED)
def create_instructor_endpoint(instructor: InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = get_instructor_by_email(db, email=instructor.email)
    if db_instructor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_instructor(db=db, instructor=instructor)

@router.get("/instructors/", response_model=List[Instructor])
def read_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_instructors(db, skip=skip, limit=limit)

@router.get("/instructors/{instructor_id}", response_model=Instructor)
def read_instructor(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = get_instructor(db, instructor_id=instructor_id)
    if db_instructor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    return db_instructor

@router.put("/instructors/{instructor_id}", response_model=Instructor)
def update_instructor_endpoint(instructor_id: int, instructor: InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = update_instructor(db=db, instructor_id=instructor_id, instructor=instructor)
    if db_instructor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    return db_instructor

@router.delete("/instructors/{instructor_id}", response_model=Instructor)
def delete_instructor_endpoint(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = delete_instructor(db=db, instructor_id=instructor_id)
    if db_instructor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    return db_instructor

# Flight endpoints
@router.post("/flights/", response_model=Flight, status_code=status.HTTP_201_CREATED)
def create_flight_endpoint(flight: FlightCreate, db: Session = Depends(get_db)):
    # Verify that student, instructor, and aircraft exist
    student = get_user(db, user_id=flight.student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    instructor = get_instructor(db, instructor_id=flight.instructor_id)
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    
    aircraft = get_aircraft(db, aircraft_id=flight.aircraft_id)
    if not aircraft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aircraft not found"
        )
    
    return create_flight(db=db, flight=flight)

@router.get("/flights/", response_model=List[Flight])
def read_flights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_flights(db, skip=skip, limit=limit)

@router.get("/flights/{flight_id}", response_model=Flight)
def read_flight(flight_id: int, db: Session = Depends(get_db)):
    db_flight = get_flight(db, flight_id=flight_id)
    if db_flight is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    return db_flight

@router.put("/flights/{flight_id}", response_model=Flight)
def update_flight_endpoint(flight_id: int, flight: FlightCreate, db: Session = Depends(get_db)):
    # Verify that student, instructor, and aircraft exist
    student = get_user(db, user_id=flight.student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    instructor = get_instructor(db, instructor_id=flight.instructor_id)
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    
    aircraft = get_aircraft(db, aircraft_id=flight.aircraft_id)
    if not aircraft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aircraft not found"
        )
    
    db_flight = update_flight(db=db, flight_id=flight_id, flight=flight)
    if db_flight is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    return db_flight

@router.delete("/flights/{flight_id}", response_model=Flight)
def delete_flight_endpoint(flight_id: int, db: Session = Depends(get_db)):
    db_flight = delete_flight(db=db, flight_id=flight_id)
    if db_flight is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    return db_flight 