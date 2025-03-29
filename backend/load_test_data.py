import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Flight, Aircraft, Instructor, FlightType, FlightStatus

def load_test_data():
    """Load test data from JSON file into the database."""
    # Get the directory containing this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_file = os.path.join(current_dir, "tests", "test_data.json")
    
    db = SessionLocal()
    try:
        with open(test_data_file, "r") as f:
            test_data = json.load(f)
        
        # Load users
        for user_data in test_data["users"]:
            # Convert string dates to datetime objects
            if "medical_expiry" in user_data:
                user_data["medical_expiry"] = datetime.fromisoformat(user_data["medical_expiry"].replace("Z", "+00:00"))
            
            db_user = User(**user_data)
            db.add(db_user)
        
        # Load aircraft
        for aircraft_data in test_data["aircraft"]:
            # Convert string dates to datetime objects
            for date_field in ["last_maintenance", "next_maintenance"]:
                if date_field in aircraft_data:
                    aircraft_data[date_field] = datetime.fromisoformat(aircraft_data[date_field].replace("Z", "+00:00"))
            
            db_aircraft = Aircraft(**aircraft_data)
            db.add(db_aircraft)
        
        # Load instructors
        for instructor_data in test_data["instructors"]:
            db_instructor = Instructor(**instructor_data)
            db.add(db_instructor)
        
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
            
            db_flight = Flight(**flight_data)
            db.add(db_flight)
        
        db.commit()
        print("Test data loaded successfully!")
    
    except Exception as e:
        print(f"Error loading test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_test_data() 