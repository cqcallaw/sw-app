""" REST API Controllers """
from flask import request, make_response, jsonify
from flask_login import current_user, login_user, logout_user
import flask_restless
from auth_demo.models import Role, User
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
                    lambda data, **kw: check_role_mod()
                ],
                'PATCH_SINGLE': [
                    lambda instance_id, data, **kw: check_role_mod()
                ],
                'PATCH_MANY': [
                    lambda params, data, **kw: check_role_mod()
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
            }
        )

        app.register_blueprint(role_api_blueprint)
        app.register_blueprint(user_api_blueprint)

        app.add_url_rule('/api/auth/login', view_func=api_login, methods=['POST'])
        app.add_url_rule('/api/auth/logout', view_func=api_logout, methods=['POST'])

def api_login():  # pylint: disable=too-many-return-statements
    """ Handle Login POST """
    content_type = request.headers['Content-Type']

    if not content_type:
        response = {
            'status': 'fail',
            'message': 'Login submission does not specific content type.'
        }
        return make_response(jsonify(response)), 400

    user_id = 'UNKNOWN_USER'
    password = 'INVALID_PASSWORD'

    if 'application/json' in content_type:
        post_data = request.get_json()

        user_id = post_data.get('user_id')
        password = post_data.get('password')
    # elif content_type == 'application/x-www-form-urlencoded':
    #     user_id = request.form['username']
    #     password = request.form['password']
    else:
        response = {
            'status': 'fail',
            'message': 'Content type %s unsupported.' % content_type
        }
        return make_response(jsonify(response)), 400

    if not user_id:
        response = {
            'status': 'fail',
            'message': 'Malformed request: missing user ID.'
        }
        return make_response(jsonify(response)), 400

    user = User.query.get(user_id)

    if not user:
        response = {
            'status': 'fail',
            'message': 'User does not exist.'
        }
        return make_response(jsonify(response)), 400

    if not BCRYPT_HANDLE.check_password_hash(user.password, password):
        response = {
            'status': 'fail',
            'message': 'Invalid password.'
        }
        return make_response(jsonify(response)), 400

    login_result = login_user(user)
    if not login_result:
        response = {
            'status': 'fail',
            'message': 'Login failed.'
        }
        return make_response(jsonify(response)), 500

    assert user.is_authenticated
    response = {
        'status': 'success',
        'message': 'Login successful.'
    }
    return make_response(jsonify(response)), 200

def api_logout():
    """ Handle logout """
    logout_user()
    response = {
        'status': 'success',
        'message': 'Log out successful.'
    }
    return make_response(jsonify(response)), 200

def check_role_mod():
    """ Check that current user can modify roles """
    if current_user.is_anonymous or not current_user.is_admin:
        raise flask_restless.ProcessingException(description='Not Authorized', code=401)

def check_user_mod_many(app, search_params=None, data=None, **kwargs):  # pylint: disable=unused-argument
    """ Check authentication status """
    if current_user.is_anonymous or not current_user.is_admin:
        raise flask_restless.ProcessingException(description='Not Authorized', code=401)

def check_user_mod(app, instance_id=None, data=None, **kw): # pylint: disable=unused-argument
    """ Check authentication status """
    if not instance_id:
        raise flask_restless.ProcessingException(description='No instance ID specified', code=400)

    mod_subject = User.query.get(instance_id)
    if not mod_subject:
        raise flask_restless.ProcessingException(description='Unknown subject', code=404)

    if current_user.is_anonymous:
        raise flask_restless.ProcessingException(description='Operation requires login.', code=401)

    if 'roles' in data:
        if not current_user.is_admin:
            raise flask_restless.ProcessingException(
                description='Only admins may edit roles',
                code=401
            )
    else:
        # check general modification constraints
        if not current_user.can_modify(mod_subject):
            raise flask_restless.ProcessingException(description='Operation not allowed', code=401)
