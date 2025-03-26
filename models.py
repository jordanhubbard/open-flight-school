from flask_login import UserMixin
from datetime import datetime, timedelta
from extensions import db
import bcrypt
import secrets

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    credit_card = db.Column(db.String(16))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expires = db.Column(db.DateTime)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def generate_reset_token(self, expires_in=3600):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(seconds=expires_in)
        db.session.commit()
        return self.reset_token

    def is_reset_token_valid(self):
        return self.reset_token_expires and self.reset_token_expires > datetime.utcnow()

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'address': self.address,
            'phone': self.phone,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }

class Aircraft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tail_number = db.Column(db.String(10), unique=True, nullable=False)
    make_model = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='aircraft', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'tail_number': self.tail_number,
            'make_model': self.make_model,
            'type': self.type,
            'created_at': self.created_at.isoformat()
        }

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    ratings = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='instructor', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'ratings': self.ratings.split(',') if self.ratings else [],
            'created_at': self.created_at.isoformat()
        }

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'user_id': self.user_id,
            'aircraft_id': self.aircraft_id,
            'instructor_id': self.instructor_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def check_conflicts(cls, start_time, end_time, aircraft_id=None, instructor_id=None):
        query = cls.query.filter(
            ((cls.aircraft_id == aircraft_id) | (cls.instructor_id == instructor_id)) &
            ((cls.start_time <= end_time) & (cls.end_time >= start_time))
        )
        return query.first() is not None 