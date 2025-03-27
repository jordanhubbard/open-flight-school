from app import app, db
from models import User, Aircraft, Instructor, Booking
from datetime import datetime
import json

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Load test data from JSON file
        with open('test-data.json', 'r') as f:
            test_data = json.load(f)
        
        # Create users
        for user_data in test_data['users']:
            user = User.query.filter_by(email=user_data['email']).first()
            if not user:
                user = User(
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    address=user_data.get('address'),
                    phone=user_data.get('phone'),
                    is_admin=user_data['is_admin']
                )
                user.set_password(user_data['password'])
                db.session.add(user)
        
        # Create aircraft
        for aircraft_data in test_data['aircraft']:
            aircraft = Aircraft.query.filter_by(tail_number=aircraft_data['tail_number']).first()
            if not aircraft:
                aircraft = Aircraft(**aircraft_data)
                db.session.add(aircraft)
        
        # Create instructors
        for instructor_data in test_data['instructors']:
            instructor = Instructor.query.filter_by(email=instructor_data['email']).first()
            if not instructor:
                instructor = Instructor(**instructor_data)
                db.session.add(instructor)
        
        # Create bookings
        if not Booking.query.first():  # Only create bookings if none exist
            for booking_data in test_data['bookings']:
                booking = Booking(
                    start_time=datetime.fromisoformat(booking_data['start_time']),
                    end_time=datetime.fromisoformat(booking_data['end_time']),
                    user_id=booking_data['user_id'],
                    aircraft_id=booking_data['aircraft_id'],
                    instructor_id=booking_data['instructor_id'],
                    status=booking_data['status']
                )
                db.session.add(booking)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 