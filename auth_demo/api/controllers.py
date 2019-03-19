""" REST API Controllers """
import datetime
import re
import jwt
from flask import current_app, request, make_response, jsonify
import flask_restless
from auth_demo.models import Role, User, BlacklistToken
from auth_demo.extensions import DATABASE_INSTANCE, BCRYPT_HANDLE

def init(app):
    """ Initialize controllers """
    with app.app_context():
        manager = flask_restless.APIManager(app, flask_sqlalchemy_db=DATABASE_INSTANCE)

        role_api_blueprint = manager.create_api_blueprint(
            Role,
            methods=['GET', 'PATCH', 'POST'],
            include_columns=['role_id', 'description'],
            preprocessors={
                'POST': [
                    lambda data, **kw: check_role_mod(app)
                ],
                'PATCH_SINGLE': [
                    lambda instance_id, data, **kw: check_role_mod(app)
                ],
                'PATCH_MANY': [
                    lambda params, data, **kw: check_role_mod(app)
                ]
            },
        )
        user_api_blueprint = manager.create_api_blueprint(
            User,
            methods=['GET', 'PATCH', 'POST'],
            include_columns=['user_id', 'name', 'roles'],
            preprocessors={
                'PATCH_SINGLE': [
                    lambda instance_id, data, **kw: check_user_mod(
                        app,
                        instance_id,
                        data,
                        **kw
                    )
                ],
                'PATCH_MANY': [
                    lambda params, data, **kw: check_user_mod_many(
                        app,
                        params,
                        data,
                        **kw
                    )
                ]
            },
            postprocessors={
                'POST': [
                    lambda result, **kw: create_user_auth_token(
                        app,
                        result,
                        **kw
                    )
                ],
            }

        )

        app.register_blueprint(role_api_blueprint)
        app.register_blueprint(user_api_blueprint)

        app.add_url_rule('/api/auth/login', view_func=login_handler, methods=['POST'])
        app.add_url_rule('/api/auth/logout', view_func=logout_handler, methods=['POST'])

def login_handler():  # pylint: disable=too-many-return-statements
    """ Handle Login POST """
    if 'Content-Type' not in request.headers:
        response = {
            'status': 'fail',
            'message': 'Content type must be specified.'
        }
        return make_response(jsonify(response)), 400

    content_type = request.headers['Content-Type']

    if not content_type:
        response = {
            'status': 'fail',
            'message': 'Login submission does not specific content type (must be application/json).'
        }
        return make_response(jsonify(response)), 400

    if content_type != 'application/json':
        response = {
            'status': 'fail',
            'message': 'Content type %s unsupported; must be application/json.' % content_type
        }
        return make_response(jsonify(response)), 400

    post_data = request.get_json()

    if not post_data:
        response = {
            'status': 'fail',
            'message': 'Empty request.'
        }
        return make_response(jsonify(response)), 400

    if not 'user_id' in post_data:
        response = {
            'status': 'fail',
            'message': 'Malformed request: missing user ID.'
        }
        return make_response(jsonify(response)), 400

    if not 'password' in post_data:
        response = {
            'status': 'fail',
            'message': 'Malformed request: missing password.'
        }
        return make_response(jsonify(response)), 400

    user = User.query.filter_by(user_id=post_data.get('user_id')).first()
    if not user:
        response = {
            'status': 'fail',
            'message': 'User does not exist.'
        }
        return make_response(jsonify(response)), 400

    if not BCRYPT_HANDLE.check_password_hash(user.password, post_data.get('password')):
        response = {
            'status': 'fail',
            'message': 'Invalid password.'
        }
        return make_response(jsonify(response)), 400

    auth_token = encode_auth_token(
        current_app.config['SECRET_KEY'],
        current_app.config['AUTH_TOKEN_TIMEOUT'],
        user.user_id
    )
    if not auth_token:
        response = {
            'status': 'fail',
            'message': 'Failed to generate auth token.'
        }
        return make_response(jsonify(response)), 500

    decoded_token = auth_token.decode()
    user.auth_token = decoded_token
    DATABASE_INSTANCE.session.commit()
    response = {
        'status': 'success',
        'message': 'Successfully logged in.',
        'auth_token': decoded_token
    }
    return make_response(jsonify(response)), 200

def logout_handler():
    """ Handle logout """
    auth_header = request.headers.get('Authorization')
    encoded_token, _, error, error_code = process_auth_header(
        current_app.config['SECRET_KEY'],
        auth_header
    )

    if error:
        return make_response(jsonify({'status': 'fail', 'message': error})), error_code

    blacklist_token = BlacklistToken(token=encoded_token)
    DATABASE_INSTANCE.session.add(blacklist_token)
    DATABASE_INSTANCE.session.commit()
    response = {
        'status': 'success',
        'message': 'Log out successful.'
    }
    return make_response(jsonify(response)), 200

def check_role_mod(app):
    """ Check that current user can modify roles """
    current_user = validate_current_user(
        app.config['SECRET_KEY'],
        request.headers.get('Authorization')
    )
    if not is_admin(current_user):
        raise flask_restless.ProcessingException(description='Not Authorized', code=401)

def check_user_mod_many(app, search_params=None, data=None, **kwargs):  # pylint: disable=unused-argument
    """ Check authentication status """
    current_user = validate_current_user(
        app.config['SECRET_KEY'],
        request.headers.get('Authorization')
    )
    if not is_admin(current_user):
        raise flask_restless.ProcessingException(description='Not Authorized', code=401)

def check_user_mod(app, instance_id=None, data=None, **kw): # pylint: disable=unused-argument
    """ Check authentication status """
    if not instance_id:
        raise flask_restless.ProcessingException(description='No instance ID specified', code=400)

    mod_subject = User.query.filter_by(user_id=instance_id).first()
    if not mod_subject:
        raise flask_restless.ProcessingException(description='Unknown subject', code=404)

    current_user = validate_current_user(
        app.config['SECRET_KEY'],
        request.headers.get('Authorization')
    )

    if 'roles' in data:
        if not is_admin(current_user):
            raise flask_restless.ProcessingException(
                description='Only admins may edit roles',
                code=401
            )
    else:
        # check general modification constraints
        if not can_modify(current_user, mod_subject):
            raise flask_restless.ProcessingException(description='Operation not allowed', code=401)

def validate_current_user(secret_key, auth_header):
    """ Validate current user """
    _, decoded_token, error, error_code = process_auth_header(
        secret_key,
        auth_header
    )
    if error:
        raise flask_restless.ProcessingException(description=error, code=error_code)

    authorization_subject = decoded_token['sub']
    current_user = User.query.filter_by(user_id=authorization_subject).first()

    if not current_user:
        raise flask_restless.ProcessingException(
            description='Unrecognized authorization subject',
            code=400
        )

    return current_user

def is_admin(user: User):
    """ Check if user is admin """
    for role in user.roles:
        if role.role_id == 'admin':
            return True

    return False

def can_modify(current_user: User, subject: User):
    """
    Check if the current user can modify the given subject
    Flask-restless complains if we put this on the User model
    """
    if current_user.user_id == subject.user_id:
        return True # users can modify their own accounts

    if is_admin(current_user):
        return True # admins can always mod

    return False

def create_user_auth_token(app, result=None, **kw): # pylint: disable=unused-argument
    """
    Add user auth token to response

    We do this as post-processing so it will be included in the response
    even though auth tokens shouldn't ordinarily be part of user views
    """
    auth_token = encode_auth_token(
        app.config['SECRET_KEY'],
        app.config['AUTH_TOKEN_TIMEOUT'],
        result['user_id']
    )
    if auth_token:
        user = User.query.filter(User.user_id == result['user_id']).first()
        user.auth_token = auth_token.decode()
        DATABASE_INSTANCE.session.commit()
        result['auth_token'] = auth_token.decode()
    else:
        app.logger.error('Failed to create user auth token!')
        raise flask_restless.ProcessingException(
            description='Failed to create auth token!',
            code=500
        )

def process_auth_header(secret_key: str, auth_header):
    """ Decode an Authorization header into a JWT token data, or return an error """
    if not auth_header:
        return None, None, 'Operation requires Authorization header.', 400

    auth_token_match = re.match('Bearer (.*)', auth_header)
    if not auth_token_match:
        return None, None, 'Operation requires valid auth token in Authorization header.', 400

    auth_token = auth_token_match.group(1)
    decoded_token, decode_token_error = decode_auth_token(
        secret_key,
        auth_token
    )
    if decode_token_error:
        return None, None, decode_token_error, 400

    existing_blacklist_entry = BlacklistToken.query.filter_by(token=auth_token).first()
    if existing_blacklist_entry:
        return None, None, 'Token blacklisted. Please log in again.', 401

    return auth_token, decoded_token, None, 200

def encode_auth_token(secret_key: str, timeout: int, user_id: str):
    """
    Generate an auth token
    :return: string
    """
    return jwt.encode(
        {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=timeout),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        },
        secret_key,
        algorithm='HS256'
    )

def decode_auth_token(secret_key: str, auth_token):
    """
    Decode an auth token
    :param auth_token:
    :return: Dict?, string?
    """
    try:
        payload = jwt.decode(auth_token, secret_key)
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return None, 'Invalid token. Please log in again.'
