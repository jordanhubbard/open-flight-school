import json
from database import init_db, User, Aircraft, Instructor, Booking
from datetime import datetime, timedelta

def load_test_data():
    # Initialize database
    init_db()
    
    # Load test data from JSON file
    with open('test-data.json', 'r') as f:
        data = json.load(f)
    
    # Create users
    for user_data in data['users']:
        User.create(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role=user_data['role']
        )
    
    # Create aircraft
    for aircraft_data in data['aircraft']:
        Aircraft.create(
            make_model=aircraft_data['make_model'],
            tail_number=aircraft_data['tail_number'],
            type_=aircraft_data['aircraft_type']
        )
    
    # Create instructors
    for instructor_data in data['instructors']:
        Instructor.create(
            name=instructor_data['name'],
            email=instructor_data['email'],
            phone=instructor_data['phone'],
            ratings=instructor_data['ratings']
        )
    
    # Create bookings
    for booking_data in data['bookings']:
        start_time = datetime.fromisoformat(booking_data['start_time'])
        end_time = datetime.fromisoformat(booking_data['end_time'])
        
        Booking.create(
            user_id=booking_data['user_id'],
            aircraft_id=booking_data['aircraft_id'],
            instructor_id=booking_data['instructor_id'],
            start_time=start_time,
            end_time=end_time,
            status=booking_data['status']
        )

if __name__ == '__main__':
    load_test_data()
    print("Test data loaded successfully!") 