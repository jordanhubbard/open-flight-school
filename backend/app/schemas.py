from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class AircraftBase(BaseModel):
    registration: str
    type: str
    model: str
    year: int

class AircraftCreate(AircraftBase):
    pass

class AircraftUpdate(AircraftBase):
    registration: Optional[str] = None
    type: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None

class Aircraft(AircraftBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class InstructorBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str
    rating: str

class InstructorCreate(InstructorBase):
    password: str

class InstructorUpdate(InstructorBase):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    rating: Optional[str] = None
    password: Optional[str] = None

class Instructor(InstructorBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class FlightBase(BaseModel):
    student_id: int
    instructor_id: int
    aircraft_id: int
    start_time: datetime
    end_time: datetime
    duration: float
    notes: Optional[str] = None

class FlightCreate(FlightBase):
    pass

class FlightUpdate(FlightBase):
    student_id: Optional[int] = None
    instructor_id: Optional[int] = None
    aircraft_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    notes: Optional[str] = None

class Flight(FlightBase):
    id: int

    class Config:
        from_attributes = True 