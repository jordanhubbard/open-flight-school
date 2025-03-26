from app import app, db
from models import User, Aircraft, Instructor, Booking
from datetime import datetime, timedelta

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

        # Create aircraft
        aircraft1 = Aircraft(
            tail_number='N12345',
            make_model='Cessna 172',
            type='Single Engine'
        )
        aircraft2 = Aircraft(
            tail_number='N67890',
            make_model='Piper PA-28',
            type='Single Engine'
        )
        db.session.add(aircraft1)
        db.session.add(aircraft2)

        # Create instructors
        instructor1 = Instructor(
            name='Jane Smith',
            email='jane@example.com',
            phone='555-0101',
            ratings='CFI,CFII,MEI'
        )
        instructor2 = Instructor(
            name='Bob Johnson',
            email='bob@example.com',
            phone='555-0102',
            ratings='CFI,CFII'
        )
        db.session.add(instructor1)
        db.session.add(instructor2)

        # Create some bookings
        now = datetime.utcnow()
        booking1 = Booking(
            start_time=now + timedelta(days=1, hours=9),
            end_time=now + timedelta(days=1, hours=11),
            user_id=2,  # John Doe
            aircraft_id=1,  # Cessna 172
            instructor_id=1,  # Jane Smith
            status='confirmed'
        )
        booking2 = Booking(
            start_time=now + timedelta(days=2, hours=13),
            end_time=now + timedelta(days=2, hours=15),
            user_id=2,  # John Doe
            aircraft_id=2,  # Piper PA-28
            instructor_id=2,  # Bob Johnson
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