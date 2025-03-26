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

        # Create regular user
        user = User(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            is_admin=False
        )
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

        # Create some bookings
        now = datetime.utcnow()
        booking1 = Booking(
            start_time=now + timedelta(days=1, hours=9),
            end_time=now + timedelta(days=1, hours=11),
            user_id=2,  # John Doe
            aircraft_id=1,  # First aircraft
            instructor_id=1,  # First instructor
            status='confirmed'
        )
        booking2 = Booking(
            start_time=now + timedelta(days=2, hours=13),
            end_time=now + timedelta(days=2, hours=15),
            user_id=2,  # John Doe
            aircraft_id=2,  # Second aircraft
            instructor_id=2,  # Second instructor
            status='pending'
        )
        db.session.add(booking1)
        db.session.add(booking2)

        try:
            db.session.commit()
            print("Test data loaded successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error loading test data: {str(e)}")

if __name__ == '__main__':
    load_test_data() 