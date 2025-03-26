from app import app, db
from models import User, Aircraft, Instructor, Booking
from datetime import datetime, timedelta
import json

def load_test_data():
    with app.app_context():
        # Create admin user
        admin = User(
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Create regular users
        users = [
            User(
                first_name='John',
                last_name='Doe',
                email='john@example.com',
                is_admin=False
            ),
            User(
                first_name='Jane',
                last_name='Smith',
                email='jane@example.com',
                is_admin=False
            ),
            User(
                first_name='Bob',
                last_name='Johnson',
                email='bob@example.com',
                is_admin=False
            )
        ]
        for user in users:
            user.set_password('password123')
            db.session.add(user)

        # Load test data from JSON file
        with open('test-data.json', 'r') as f:
            test_data = json.load(f)

        # Create aircraft
        for aircraft_data in test_data['aircraft']:
            aircraft = Aircraft(
                tail_number=aircraft_data['tail_number'],
                make_model=aircraft_data['make_model'],
                type=aircraft_data['type']
            )
            db.session.add(aircraft)

        # Create instructors
        for instructor_data in test_data['instructors']:
            instructor = Instructor(
                name=instructor_data['name'],
                email=instructor_data['email'],
                phone=instructor_data['phone'],
                ratings=','.join(instructor_data['ratings'])
            )
            db.session.add(instructor)

        # Create bookings
        for booking_data in test_data['bookings']:
            booking = Booking(
                user_id=booking_data['user_id'],
                aircraft_id=booking_data['aircraft_id'],
                instructor_id=booking_data['instructor_id'],
                start_time=datetime.fromisoformat(booking_data['start_time']),
                end_time=datetime.fromisoformat(booking_data['end_time']),
                status=booking_data['status']
            )
            db.session.add(booking)

        try:
            db.session.commit()
            print("Test data loaded successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error loading test data: {str(e)}")

if __name__ == '__main__':
    load_test_data() 