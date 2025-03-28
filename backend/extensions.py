from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id)) 