from flask_login import LoginManager
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


login_manager = LoginManager()
login_manager.login_view = 'app.web.routes.login'
login_manager.session_protection = "strong"
bcrypt = Bcrypt()
db = SQLAlchemy()


