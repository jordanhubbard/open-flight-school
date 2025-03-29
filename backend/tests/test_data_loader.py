import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models import User, Flight, Aircraft, Instructor, FlightType, FlightStatus

def load_test_data(db: Session):
    """Load test data from JSON file into the database."""
    # Clean up existing data
    print("Cleaning up existing data...")
    db.execute(delete(Flight))
    db.execute(delete(Aircraft))
    db.execute(delete(Instructor))
    db.execute(delete(User))
    db.commit()
    print("Existing data cleaned up")
    
    # Get the directory containing this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_file = os.path.join(current_dir, "test_data.json")
    
    with open(test_data_file, "r") as f:
        test_data = json.load(f)
    
    # Dictionary to store entity mappings
    id_mappings = {
        'users': {},      # email -> id
        'aircraft': {},   # registration -> id
        'instructors': {} # email -> id
    }
    
    # Load users
    for user_data in test_data["users"]:
        if "medical_expiry" in user_data:
            user_data["medical_expiry"] = datetime.fromisoformat(user_data["medical_expiry"].replace("Z", "+00:00"))
        
        db_user = User(**user_data)
        db.add(db_user)
    db.commit()
    
    # Store user mappings
    users = db.execute(select(User)).scalars().all()
    for user in users:
        id_mappings['users'][user.email] = user.id
    print("Users loaded successfully")
    
    # Load aircraft
    for aircraft_data in test_data["aircraft"]:
        for date_field in ["last_maintenance", "next_maintenance"]:
            if date_field in aircraft_data:
                aircraft_data[date_field] = datetime.fromisoformat(aircraft_data[date_field].replace("Z", "+00:00"))
        
        db_aircraft = Aircraft(**aircraft_data)
        db.add(db_aircraft)
    db.commit()
    
    # Store aircraft mappings
    aircraft = db.execute(select(Aircraft)).scalars().all()
    for ac in aircraft:
        id_mappings['aircraft'][ac.registration] = ac.id
    print("Aircraft loaded successfully")
    
    # Load instructors
    for instructor_data in test_data["instructors"]:
        db_instructor = Instructor(**instructor_data)
        db.add(db_instructor)
    db.commit()
    
    # Store instructor mappings
    instructors = db.execute(select(Instructor)).scalars().all()
    for instructor in instructors:
        id_mappings['instructors'][instructor.email] = instructor.id
    print("Instructors loaded successfully")
    
    # Load flights
    for flight_data in test_data["flights"]:
        # Convert string dates to datetime objects
        for date_field in ["start_time", "end_time"]:
            if date_field in flight_data:
                flight_data[date_field] = datetime.fromisoformat(flight_data[date_field].replace("Z", "+00:00"))
        
        # Convert string enums to enum objects
        if "flight_type" in flight_data:
            flight_data["flight_type"] = FlightType(flight_data["flight_type"])
        if "status" in flight_data:
            flight_data["status"] = FlightStatus(flight_data["status"])
        
        # Map the IDs
        if "student_id" in flight_data:
            student_email = next((u["email"] for u in test_data["users"] if u.get("id", 1) == flight_data["student_id"]), None)
            if student_email:
                flight_data["student_id"] = id_mappings['users'][student_email]
        
        if "instructor_id" in flight_data:
            instructor_email = next((i["email"] for i in test_data["instructors"] if i.get("id", flight_data["instructor_id"]) == flight_data["instructor_id"]), None)
            if instructor_email:
                flight_data["instructor_id"] = id_mappings['instructors'][instructor_email]
        
        if "aircraft_id" in flight_data:
            aircraft_reg = next((a["registration"] for a in test_data["aircraft"] if a.get("id", flight_data["aircraft_id"]) == flight_data["aircraft_id"]), None)
            if aircraft_reg:
                flight_data["aircraft_id"] = id_mappings['aircraft'][aircraft_reg]
        
        db_flight = Flight(**flight_data)
        db.add(db_flight)
    db.commit()
    print("Flights loaded successfully") 