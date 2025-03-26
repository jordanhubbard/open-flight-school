from app import app, db
from models import User, Aircraft, Instructor, Booking
from datetime import datetime, timedelta

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@eyesoutside.com').first()
        if not admin:
            admin = User(
                first_name='Admin',
                last_name='User',
                email='admin@eyesoutside.com',
                address='123 Admin St',
                phone='555-0123',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Create test aircraft if they don't exist
        aircraft_data = [
            {'tail_number': 'N12345', 'make_model': 'Cessna 172', 'type': 'Single Engine'},
            {'tail_number': 'N67890', 'make_model': 'Piper Arrow', 'type': 'Complex'},
            {'tail_number': 'N24680', 'make_model': 'Diamond DA40', 'type': 'Glass Cockpit'}
        ]
        
        for aircraft_info in aircraft_data:
            aircraft = Aircraft.query.filter_by(tail_number=aircraft_info['tail_number']).first()
            if not aircraft:
                aircraft = Aircraft(**aircraft_info)
                db.session.add(aircraft)
        
        # Create test instructors if they don't exist
        instructor_data = [
            {
                'name': 'John Smith',
                'email': 'john@eyesoutside.com',
                'phone': '555-0124',
                'ratings': 'CFI, CFII, MEI'
            },
            {
                'name': 'Sarah Johnson',
                'email': 'sarah@eyesoutside.com',
                'phone': '555-0125',
                'ratings': 'CFI, CFII, AGI'
            }
        ]
        
        for instructor_info in instructor_data:
            instructor = Instructor.query.filter_by(email=instructor_info['email']).first()
            if not instructor:
                instructor = Instructor(**instructor_info)
                db.session.add(instructor)
        
        # Create test bookings if they don't exist
        if not Booking.query.first():
            now = datetime.utcnow()
            booking_data = [
                {
                    'start_time': now + timedelta(days=1, hours=9),
                    'end_time': now + timedelta(days=1, hours=11),
                    'user_id': 1,
                    'aircraft_id': 1,
                    'instructor_id': 1,
                    'status': 'confirmed'
                },
                {
                    'start_time': now + timedelta(days=2, hours=14),
                    'end_time': now + timedelta(days=2, hours=16),
                    'user_id': 1,
                    'aircraft_id': 2,
                    'instructor_id': 2,
                    'status': 'pending'
                }
            ]
            
            for booking_info in booking_data:
                booking = Booking(**booking_info)
                db.session.add(booking)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 