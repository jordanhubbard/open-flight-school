import json
from datetime import datetime
from app import create_app
from models import db, User, Aircraft, Instructor, Booking
from werkzeug.security import generate_password_hash

def load_test_data():
    """Load test data into the database using SQLAlchemy models."""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Load test data from JSON file
        with open('test-data.json', 'r') as f:
            data = json.load(f)
        
        # Create users
        users = {}  # Keep track of created users for bookings
        for user_data in data['users']:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password=generate_password_hash(user_data['password']),
                role=user_data['role']
            )
            db.session.add(user)
            db.session.flush()  # Get the ID before commit
            users[user.email] = user
        
        # Create aircraft
        aircraft = {}  # Keep track of created aircraft for bookings
        for aircraft_data in data['aircraft']:
            aircraft_obj = Aircraft(
                tail_number=aircraft_data['tail_number'],
                make_model=aircraft_data['make_model'],
                aircraft_type=aircraft_data['aircraft_type'],
                status=aircraft_data['status']
            )
            db.session.add(aircraft_obj)
            db.session.flush()
            aircraft[aircraft_obj.tail_number] = aircraft_obj
        
        # Create instructors
        instructors = {}  # Keep track of created instructors for bookings
        for instructor_data in data['instructors']:
            instructor = Instructor(
                name=instructor_data['name'],
                email=instructor_data['email'],
                phone=instructor_data['phone'],
                ratings=instructor_data['ratings']
            )
            db.session.add(instructor)
            db.session.flush()
            instructors[instructor.email] = instructor
        
        # Create bookings
        for booking_data in data['bookings']:
            # Map user_id to actual user
            user = list(users.values())[booking_data['user_id'] - 2]  # Adjust for 0-based index
            # Map aircraft_id to actual aircraft
            aircraft_obj = list(aircraft.values())[booking_data['aircraft_id'] - 1]
            # Map instructor_id to actual instructor
            instructor = list(instructors.values())[booking_data['instructor_id'] - 1]
            
            booking = Booking(
                user_id=user.id,
                aircraft_id=aircraft_obj.id,
                instructor_id=instructor.id,
                start_time=datetime.fromisoformat(booking_data['start_time']),
                end_time=datetime.fromisoformat(booking_data['end_time']),
                status=booking_data['status']
            )
            db.session.add(booking)
        
        # Commit all changes
        db.session.commit()
        print("Test data loaded successfully!")

if __name__ == '__main__':
    load_test_data() 