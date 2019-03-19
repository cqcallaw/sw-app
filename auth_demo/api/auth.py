""" Authentication """
import datetime
import re
import jwt
from flask import current_app, request, make_response, jsonify
from auth_demo.models import User, BlacklistToken
from auth_demo.extensions import DATABASE_INSTANCE, BCRYPT_HANDLE

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
