from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    full_name = Column(String)
    phone = Column(String)
    address = Column(String)
    medical_class = Column(String)
    medical_expiry = Column(DateTime)
    ratings = Column(String)
    endorsements = Column(String)
    flight_reviews = Column(String)
    currency = Column(String)
    notes = Column(String)

class Aircraft(Base):
    __tablename__ = "aircraft"

    id = Column(Integer, primary_key=True, index=True)
    registration = Column(String, unique=True, index=True)
    make_model = Column(String)
    year = Column(Integer)
    serial_number = Column(String)
    total_time = Column(Integer)
    last_maintenance = Column(DateTime)
    next_maintenance = Column(DateTime)
    status = Column(String)
    notes = Column(String)

class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    ratings = Column(String)
    endorsements = Column(String)
    flight_reviews = Column(String)
    currency = Column(String)
    availability = Column(String)
    notes = Column(String)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String)
    notes = Column(String)

    student = relationship("User", back_populates="bookings")
    instructor = relationship("Instructor", back_populates="bookings")
    aircraft = relationship("Aircraft", back_populates="bookings") 