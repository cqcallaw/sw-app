""" Configuration data """

import os

BASE_DATABASE_NAME = 'sw_demo_api.sqlite'

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'very_secret_key')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_PURGE = False
    DATABASE_NAME = BASE_DATABASE_NAME
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_NAME

class Development(BaseConfig):
    """Development configuration."""
    BCRYPT_LOG_ROUNDS = 4
    DEBUG = True
    DB_PURGE = True

class Testing(Development):
    """Testing configuration."""
    TESTING = True
    DATABASE_NAME = 'testing_' + BASE_DATABASE_NAME
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_NAME
