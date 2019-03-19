""" Extension instances """
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

DATABASE_INSTANCE = SQLAlchemy()
BCRYPT_HANDLE = Bcrypt()

def register_extensions(app):
    """ Register extensions with the Flask app """
    DATABASE_INSTANCE.init_app(app)
    BCRYPT_HANDLE.init_app(app)
