import json
import os
import sys
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Aircraft, Instructor

def load_test_data():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Read test data
        with open('test-data.json', 'r') as f:
            data = json.load(f)
        
        # Load aircraft
        for aircraft_data in data['aircraft']:
            aircraft = Aircraft(
                make_model=aircraft_data['make_model'],
                tail_number=aircraft_data['tail_number'],
                type=aircraft_data['type']
            )
            db.session.add(aircraft)
        
        # Load instructors
        for instructor_data in data['instructors']:
            instructor = Instructor(
                name=instructor_data['name'],
                email=instructor_data['email'],
                phone=instructor_data['phone'],
                ratings=instructor_data['ratings']
            )
            db.session.add(instructor)
        
        # Commit all changes
        db.session.commit()
        print("Test data loaded successfully!")

if __name__ == '__main__':
    load_test_data() 