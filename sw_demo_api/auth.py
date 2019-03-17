""" Auth Blueprint """
# import functools
# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, session, url_for
# )
# from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import jwt
from flask import current_app, request, make_response, jsonify
from sw_demo_api.models import User
from sw_demo_api.extensions import DATABASE_INSTANCE, BCRYPT_HANDLE

def login_handler():
    """ Handle Login POST """
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

    auth_token = encode_auth_token(current_app, user.id)
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
