""" Extension instances """
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

DATABASE_INSTANCE = SQLAlchemy()
BCRYPT_HANDLE = Bcrypt()
LOGIN_MANAGER = LoginManager()

def register_extensions(app):
    """ Register extensions with the Flask app """
    DATABASE_INSTANCE.init_app(app)
    BCRYPT_HANDLE.init_app(app)
    LOGIN_MANAGER.init_app(app)
