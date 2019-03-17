""" Configuration data """

import os

DATABASE_NAME = 'sw_demo_api'

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'very_secret_key')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_NAME + '.sqlite'
