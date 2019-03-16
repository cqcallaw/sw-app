import os

from flask import Flask, g
from flask_restful import Resource, Api
from . import db, orm
from sqlalchemy import text

class Users(Resource):
    def get(self):
        session_maker = db.get_session_maker()
        session = session_maker()
        return [{ 'id': instance.id, 'name': instance.name} for instance in session.query(orm.User)]

class User(Resource):
    def get(self, user_id):
        session_maker = db.get_session_maker()
        session = session_maker()
        result = session.query(orm.User).filter_by(id=user_id)
        result = result[0] # assume one result; IDs should be primary keys
        return {
            'id': result.id,
            'name': result.name,
            'roles': [{ 'id': role.id, 'description': role.description } for role in result.roles]
        }

class Roles(Resource):
    def get(self):
        session_maker = db.get_session_maker()
        session = session_maker()
        return [{ 'id': instance.id, 'description': instance.description} for instance in session.query(orm.Role)]

class Role(Resource):
    def get(self, role_id):
        session_maker = db.get_session_maker()
        session = session_maker()
        result = session.query(orm.Role).filter_by(id=role_id)
        result = result[0] # assume one result; IDs should be primary keys
        return {
            'id': result.id,
            'description': result.description,
            'members': [{ 'id': user.id, 'name': user.name } for user in result.users]
        }

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'sw-demo.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    api = Api(app)
    api.add_resource(Users, '/api/v1/users')
    api.add_resource(User, '/api/v1/users/<string:user_id>')
    api.add_resource(Roles, '/api/v1/roles')
    api.add_resource(Role, '/api/v1/roles/<string:role_id>')

    return app
