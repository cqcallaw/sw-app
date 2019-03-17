""" REST API Controllers """
import datetime
import jwt
import flask_restless
from sw_demo_api.models import Role, User
from sw_demo_api.extensions import DATABASE_INSTANCE

def init(app):
    """ Initialize controllers """
    with app.app_context():
        manager = flask_restless.APIManager(app, flask_sqlalchemy_db=DATABASE_INSTANCE)

        role_api_blueprint = manager.create_api_blueprint(
            Role,
            methods=['GET', 'PATCH', 'POST'],
            include_columns=['role_id', 'description']
        )
        user_api_blueprint = manager.create_api_blueprint(
            User,
            methods=['GET', 'PATCH', 'POST'],
            include_columns=['user_id', 'name', 'roles'],
            preprocessors={
                'PATCH_SINGLE': [lambda instance_id, data, **kwargs: check_auth(app, instance_id, data, **kwargs)],
                'PATCH_MANY': [lambda search_params, data, **kwargs: check_auth_many(app, search_params, data, **kwargs)]
            }
        )

        app.register_blueprint(role_api_blueprint)
        app.register_blueprint(user_api_blueprint)

def check_auth_many(app, search_params=None, data=None, **kwargs):
    """ Check authentication status """
    raise flask_restless.ProcessingException(description='Not Authorized', code=401)

def check_auth(app, instance_id=None, data=None, **kw):
    """ Check authentication status """
    raise flask_restless.ProcessingException(description='Not Authorized', code=401)

def encode_auth_token(app, user_id):
    """
    Generates the Auth Token
    :return: string
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

def decode_auth_token(app, auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config['SECRET_KEY'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
