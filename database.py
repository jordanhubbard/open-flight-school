import sqlite3
from datetime import datetime
import os
from contextlib import contextmanager

DATABASE_PATH = os.path.join('instance', 'flight_school.db')

def init_db():
    """Initialize the database by creating all tables."""
    os.makedirs('instance', exist_ok=True)
    with get_db() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                address TEXT,
                phone TEXT,
                credit_card TEXT,
                is_admin BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reset_token TEXT UNIQUE,
                reset_token_expires TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS aircraft (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tail_number TEXT UNIQUE NOT NULL,
                make_model TEXT NOT NULL,
                type TEXT,
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
    @staticmethod
    def get_by_id(user_id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            return cursor.fetchone()

    @staticmethod
    def get_by_email(email):
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            return cursor.fetchone()

    @staticmethod
    def create(first_name, last_name, email, password_hash, is_admin=False):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO users (first_name, last_name, email, password_hash, is_admin)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, password_hash, is_admin))
            db.commit()
            return cursor.lastrowid

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

class Aircraft:
    @staticmethod
    def get_all():
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('SELECT * FROM aircraft')
            return cursor.fetchall()

    @staticmethod
    def get_by_id(aircraft_id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('SELECT * FROM aircraft WHERE id = ?', (aircraft_id,))
            return cursor.fetchone()

    @staticmethod
    def create(tail_number, make_model, type_):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO aircraft (tail_number, make_model, type)
                VALUES (?, ?, ?)
            ''', (tail_number, make_model, type_))
            db.commit()
            return cursor.lastrowid

class Instructor:
    @staticmethod
    def get_all():
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('SELECT * FROM instructors')
            return cursor.fetchall()

    @staticmethod
    def get_by_id(instructor_id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('SELECT * FROM instructors WHERE id = ?', (instructor_id,))
            return cursor.fetchone()

    @staticmethod
    def create(name, email, phone, ratings):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO instructors (name, email, phone, ratings)
                VALUES (?, ?, ?, ?)
            ''', (name, email, phone, ratings))
            db.commit()
            return cursor.lastrowid

class Booking:
    @staticmethod
    def get_all():
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('''
                SELECT b.*, u.first_name || ' ' || u.last_name as user_name,
                       a.make_model as aircraft_name, i.name as instructor_name
                FROM bookings b
                LEFT JOIN users u ON b.user_id = u.id
                LEFT JOIN aircraft a ON b.aircraft_id = a.id
                LEFT JOIN instructors i ON b.instructor_id = i.id
            ''')
            return cursor.fetchall()

    @staticmethod
    def get_by_user(user_id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('''
                SELECT b.*, a.make_model as aircraft_name, i.name as instructor_name
                FROM bookings b
                LEFT JOIN aircraft a ON b.aircraft_id = a.id
                LEFT JOIN instructors i ON b.instructor_id = i.id
                WHERE b.user_id = ?
            ''', (user_id,))
            return cursor.fetchall()

    @staticmethod
    def get_by_id(booking_id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('''
                SELECT b.*, a.make_model as aircraft_name, i.name as instructor_name
                FROM bookings b
                LEFT JOIN aircraft a ON b.aircraft_id = a.id
                LEFT JOIN instructors i ON b.instructor_id = i.id
                WHERE b.id = ?
            ''', (booking_id,))
            return cursor.fetchone()

    @staticmethod
    def get_by_date_range(start_date, end_date):
        with get_db() as db:
            cursor = db.cursor()
            cursor.row_factory = dict_factory
            cursor.execute('''
                SELECT b.*, a.make_model as aircraft_name, i.name as instructor_name
                FROM bookings b
                LEFT JOIN aircraft a ON b.aircraft_id = a.id
                LEFT JOIN instructors i ON b.instructor_id = i.id
                WHERE b.start_time >= ? AND b.start_time <= ?
            ''', (start_date.isoformat(), end_date.isoformat()))
            return cursor.fetchall()

    @staticmethod
    def create(start_time, end_time, user_id, aircraft_id, instructor_id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO bookings (start_time, end_time, user_id, aircraft_id, instructor_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (start_time.isoformat(), end_time.isoformat(), user_id, aircraft_id, instructor_id))
            db.commit()
            return cursor.lastrowid

    @staticmethod
    def check_conflicts(start_time, end_time, aircraft_id=None, instructor_id=None):
        with get_db() as db:
            cursor = db.cursor()
            conditions = []
            params = []
            
            if aircraft_id:
                conditions.append('aircraft_id = ?')
                params.append(aircraft_id)
            if instructor_id:
                conditions.append('instructor_id = ?')
                params.append(instructor_id)
                
            where_clause = ' OR '.join(conditions)
            query = f'''
                SELECT COUNT(*) as count
                FROM bookings
                WHERE status != 'cancelled'
                AND (({where_clause})
                AND (start_time <= ? AND end_time >= ?))
            '''
            params.extend([end_time.isoformat(), start_time.isoformat()])
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result['count'] > 0 