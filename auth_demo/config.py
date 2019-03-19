""" Configuration data """
# pylint: disable=too-few-public-methods
import os

BASE_DATABASE_NAME = 'auth_demo.sqlite'

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'very_secret_key')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_PURGE = False
    SAMPLE_DATA = False
    DATABASE_NAME = BASE_DATABASE_NAME
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_NAME
    AUTH_TOKEN_TIMEOUT = 2592000 # default to 30 day timeout

class Development(BaseConfig):
    """Development configuration."""
    BCRYPT_LOG_ROUNDS = 4
    DEBUG = True
    DB_PURGE = True
    SAMPLE_DATA = True
    AUTH_TOKEN_TIMEOUT = 86400 # 24 hours

class Testing(Development):
    """Testing configuration."""
    TESTING = True
    SAMPLE_DATA = True
    DATABASE_NAME = 'testing_' + BASE_DATABASE_NAME
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_NAME
    PRESERVE_CONTEXT_ON_EXCEPTION = False # ref: https://stackoverflow.com/a/28139033/577298
    AUTH_TOKEN_TIMEOUT = 5
