from app import app, db
from models import User

with app.app_context():
    user = User.query.filter_by(email='joan@smith.com').first()
    if user:
        print(f'User found: {user.first_name} {user.last_name} (Email: {user.email})')
    else:
        print('User not found') 