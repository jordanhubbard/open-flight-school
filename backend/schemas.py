from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

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
    notes: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True

class AircraftBase(BaseModel):
    registration: str
    make_model: str
    year: int
    serial_number: str
    total_time: int
    last_maintenance: datetime
    next_maintenance: datetime
    status: str
    notes: str

class AircraftCreate(AircraftBase):
    pass

class Aircraft(AircraftBase):
    id: int

    class Config:
        orm_mode = True

class InstructorBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    ratings: str
    endorsements: str
    flight_reviews: str
    currency: str
    availability: str
    notes: str

class InstructorCreate(InstructorBase):
    pass

class Instructor(InstructorBase):
    id: int

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    student_id: int
    instructor_id: int
    aircraft_id: int
    start_time: datetime
    end_time: datetime
    status: str
    notes: str

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int

    class Config:
        orm_mode = True 