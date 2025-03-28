import sqlite3
from datetime import datetime, timedelta
import os
from contextlib import contextmanager

def get_database_path():
    """Get the database path based on the environment."""
    if os.environ.get('TESTING'):
        return 'test.db'
    return os.path.join('instance', 'flight_school.db')

DATABASE_PATH = get_database_path()

def init_db():
    """Initialize the database by creating all tables."""
    if os.environ.get('TESTING'):
        # For testing, we want to start with a fresh database
        try:
            os.remove(DATABASE_PATH)
        except FileNotFoundError:
            pass
    else:
        os.makedirs('instance', exist_ok=True)
    
    with get_db() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'student',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reset_token TEXT UNIQUE,
                reset_token_expires TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS aircraft (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tail_number TEXT UNIQUE NOT NULL,
                make_model TEXT NOT NULL,
                type_ TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS instructors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                ratings TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                user_id INTEGER NOT NULL,
                aircraft_id INTEGER,
                instructor_id INTEGER,
                status TEXT DEFAULT 'confirmed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (aircraft_id) REFERENCES aircraft (id),
                FOREIGN KEY (instructor_id) REFERENCES instructors (id)
            );
        ''')

@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    try:
        yield conn
    finally:
        conn.close()

def dict_factory(cursor, row):
    """Convert database rows to dictionaries."""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password_hash = data['password_hash']
        self.role = data['role']
        self.created_at = data['created_at']
        self.reset_token = data.get('reset_token')
        self.reset_token_expires = data.get('reset_token_expires')
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        return self.password_hash == password  # TODO: Use proper password hashing

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at
        }

    @staticmethod
    def get_by_id(user_id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            data = cursor.fetchone()
            return User(data) if data else None

    @staticmethod
    def get_by_email(email):
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            data = cursor.fetchone()
            return User(data) if data else None

    @staticmethod
    def create(username, email, password, role='student'):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password, role))
            db.commit()
            return User.get_by_id(cursor.lastrowid)

    @staticmethod
    def update(user_id, **kwargs):
        if not kwargs:
            return False
        
        set_clause = ', '.join(f'{key} = ?' for key in kwargs.keys())
        query = f'UPDATE users SET {set_clause} WHERE id = ?'
        values = list(kwargs.values()) + [user_id]
        
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(query, values)
            db.commit()
            return cursor.rowcount > 0

    @staticmethod
    def generate_reset_token(user_id):
        token = os.urandom(32).hex()
        expires = datetime.utcnow() + timedelta(hours=1)
        User.update(user_id, reset_token=token, reset_token_expires=expires)
        return token

    @staticmethod
    def verify_reset_token(token):
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('''
                SELECT id FROM users 
                WHERE reset_token = ? AND reset_token_expires > ?
            ''', (token, datetime.utcnow().isoformat()))
            user = cursor.fetchone()
            return User.get_by_id(user['id']) if user else None

    @staticmethod
    def update_password(user_id, password):
        return User.update(user_id, password_hash=password)

class Aircraft:
    def __init__(self, data):
        self.id = data['id']
        self.make_model = data['make_model']
        self.registration = data['registration']
        self.hourly_rate = data['hourly_rate']
        self.type_ = data.get('type_', 'Single Engine')
    
    def to_dict(self):
        return {
            'id': self.id,
            'make_model': self.make_model,
            'registration': self.registration,
            'hourly_rate': self.hourly_rate,
            'type_': self.type_
        }
    
    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM aircraft')
        aircraft = cursor.fetchall()
        return [Aircraft(dict(a)) for a in aircraft]
    
    @staticmethod
    def get_by_id(aircraft_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM aircraft WHERE id = ?', (aircraft_id,))
        data = cursor.fetchone()
        return Aircraft(dict(data)) if data else None

    @staticmethod
    def create(tail_number, make_model, type_='Single Engine', hourly_rate=150.0):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO aircraft (registration, make_model, type_, hourly_rate)
            VALUES (?, ?, ?, ?)
        ''', (tail_number, make_model, type_, hourly_rate))
        aircraft_id = cursor.lastrowid
        db.commit()
        
        cursor.execute('SELECT * FROM aircraft WHERE id = ?', (aircraft_id,))
        data = cursor.fetchone()
        return Aircraft(dict(data))

class Instructor:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.hourly_rate = data['hourly_rate']
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'hourly_rate': self.hourly_rate
        }
    
    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM instructors')
        instructors = cursor.fetchall()
        return [Instructor(dict(i)) for i in instructors]
    
    @staticmethod
    def get_by_id(instructor_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM instructors WHERE id = ?', (instructor_id,))
        data = cursor.fetchone()
        return Instructor(dict(data)) if data else None

    @staticmethod
    def create(name, email, hourly_rate=75.0):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO instructors (name, email, hourly_rate)
            VALUES (?, ?, ?)
        ''', (name, email, hourly_rate))
        instructor_id = cursor.lastrowid
        db.commit()
        
        cursor.execute('SELECT * FROM instructors WHERE id = ?', (instructor_id,))
        data = cursor.fetchone()
        return Instructor(dict(data))

class Booking:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.aircraft_id = data['aircraft_id']
        self.instructor_id = data['instructor_id']
        self.start_time = datetime.fromisoformat(data['start_time'])
        self.end_time = datetime.fromisoformat(data['end_time'])
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'aircraft_id': self.aircraft_id,
            'instructor_id': self.instructor_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat()
        }
    
    @staticmethod
    def get_by_user(user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT * FROM bookings WHERE user_id = ?',
            (user_id,)
        )
        bookings = cursor.fetchall()
        return [Booking(dict(booking)) for booking in bookings]
    
    @staticmethod
    def check_conflicts(start_time, end_time, aircraft_id, instructor_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM bookings 
            WHERE (aircraft_id = ? OR instructor_id = ?)
            AND (
                (start_time <= ? AND end_time > ?) OR
                (start_time < ? AND end_time >= ?) OR
                (start_time >= ? AND end_time <= ?)
            )
        ''', (
            aircraft_id, instructor_id,
            start_time, start_time,
            end_time, end_time,
            start_time, end_time
        ))
        count = cursor.fetchone()[0]
        return count > 0
    
    @staticmethod
    def create(user_id, aircraft_id, instructor_id, start_time, end_time):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO bookings (user_id, aircraft_id, instructor_id, start_time, end_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, aircraft_id, instructor_id, start_time.isoformat(), end_time.isoformat()))
        booking_id = cursor.lastrowid
        db.commit()
        
        cursor.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,))
        booking_data = cursor.fetchone()
        return Booking(dict(booking_data)) 