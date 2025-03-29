from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .base import Base

class FlightType(str, enum.Enum):
    training = "training"
    solo = "solo"
    cross_country = "cross_country"
    night = "night"
    instrument = "instrument"

class FlightStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"
    in_progress = "in_progress"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    address = Column(String)
    medical_class = Column(String)
    medical_expiry = Column(DateTime)
    ratings = Column(String)
    endorsements = Column(String)
    flight_reviews = Column(String)
    currency = Column(String)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    flights = relationship("Flight", back_populates="student")

class Aircraft(Base):
    __tablename__ = "aircraft"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    registration = Column(String, unique=True, index=True)
    type = Column(String)
    model = Column(String)
    year = Column(Integer)
    serial_number = Column(String)
    total_time = Column(Float)
    last_maintenance = Column(DateTime)
    next_maintenance = Column(DateTime)
    status = Column(String)
    category = Column(String)
    class_type = Column(String)
    is_active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    flights = relationship("Flight", back_populates="aircraft")

class Instructor(Base):
    __tablename__ = "instructors"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    rating = Column(String)
    is_active = Column(Boolean, default=True)
    availability = Column(String)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    flights = relationship("Flight", back_populates="instructor")

class Flight(Base):
    __tablename__ = "flights"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"))
    flight_type = Column(Enum(FlightType))
    status = Column(Enum(FlightStatus))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Float)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("User", back_populates="flights")
    instructor = relationship("Instructor", back_populates="flights")
    aircraft = relationship("Aircraft", back_populates="flights") 