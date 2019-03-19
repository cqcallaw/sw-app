""" REST API Controllers """
from flask import request
import flask_restless
from auth_demo.models import Role, User
from auth_demo.extensions import DATABASE_INSTANCE
from auth_demo.auth import login_handler, logout_handler, encode_auth_token, process_auth_header

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