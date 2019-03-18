""" REST API Controllers """
import flask_restless
from sw_demo_api.models import Role, User
from sw_demo_api.extensions import DATABASE_INSTANCE
from sw_demo_api.auth import login_handler, logout_handler, encode_auth_token

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
                'PATCH_SINGLE': [
                    lambda instance_id, data, **kw: check_auth(
                        app,
                        instance_id,
                        data,
                        **kw
                    )
                ],
                'PATCH_MANY': [
                    lambda params, data, **kw: check_auth_many(
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

def check_auth_many(app, search_params=None, data=None, **kwargs):
    """ Check authentication status """
    raise flask_restless.ProcessingException(description='Not Authorized', code=401)

def check_auth(app, instance_id=None, data=None, **kw):
    """ Check authentication status """
    raise flask_restless.ProcessingException(description='Not Authorized', code=401)

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
