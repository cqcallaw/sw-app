""" Authentication """
import datetime
import jwt
from flask import current_app, request, make_response, jsonify
from sw_demo_api.models import User
from sw_demo_api.extensions import DATABASE_INSTANCE, BCRYPT_HANDLE

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

    auth_token = encode_auth_token(current_app.config['SECRET_KEY'], user.user_id)
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
    if not auth_header:
        response = {
            'status': 'fail',
            'message': 'Logout requires Authorization header.'
        }
        return make_response(jsonify(response)), 400

    auth_token = auth_header.split(" ")[1]

    if not auth_token:
        response = {
            'status': 'fail',
            'message': 'Logout requires valid auth token in Authorization header.'
        }
        return make_response(jsonify(response)), 400
    response = {
        'status': 'fail',
        'message': 'Failed to log out.'
    }
    return make_response(jsonify(response)), 500

def encode_auth_token(secret_key, user_id):
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
        secret_key,
        algorithm='HS256'
    )

def decode_auth_token(secret_key, auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, secret_key)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
