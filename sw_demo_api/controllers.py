""" REST API Controllers """
import flask_restless
from sw_demo_api.models import Role, User
from sw_demo_api.extensions import DATABASE_INSTANCE

def init(app):
    """ Initialize controllers """
    with app.app_context():
        manager = flask_restless.APIManager(app, flask_sqlalchemy_db=DATABASE_INSTANCE)

        role_api_blueprint = manager.create_api_blueprint(Role, methods=['GET', 'PATCH', 'POST'])
        user_api_blueprint = manager.create_api_blueprint(
            User,
            methods=['GET', 'PATCH', 'POST'],
            include_columns=['user_id', 'name', 'roles']
        )

        app.register_blueprint(role_api_blueprint)
        app.register_blueprint(user_api_blueprint)
