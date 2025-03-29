from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from models import FlightType, FlightStatus

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: str
    address: str
    medical_class: str
    medical_expiry: datetime
    ratings: str
    endorsements: str
    flight_reviews: str
    currency: str
    notes: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

class AircraftBase(BaseModel):
    registration: str
    make_model: str
    year: int
    serial_number: str
    total_time: int
    last_maintenance: datetime
    next_maintenance: datetime
    status: str
    category: str
    class_type: str
    notes: Optional[str] = None

class AircraftCreate(AircraftBase):
    pass

class Aircraft(AircraftBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class InstructorBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    ratings: str
    endorsements: str
    flight_reviews: str
    currency: str
    availability: str
    notes: Optional[str] = None

class InstructorCreate(InstructorBase):
    pass

class Instructor(InstructorBase):
    id: int

    class Config:
        from_attributes = True

class FlightBase(BaseModel):
    student_id: int
    instructor_id: int
    aircraft_id: int
    flight_type: FlightType
    status: FlightStatus
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None

class FlightCreate(FlightBase):
    pass

class Flight(FlightBase):
    id: int

    class Config:
        from_attributes = True 