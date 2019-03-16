import os

from flask import Flask, g
from flask_restful import Resource, Api
from . import db, orm
from sqlalchemy.orm import sessionmaker

class Users(Resource):
    def get(self):
        session_maker = db.get_session_maker()
        session = session_maker()
        return [{ 'id': instance.id, 'name': instance.name} for instance in session.query(orm.User).order_by(orm.User.id)]

class User(Resource):
    def get(self, user_id):
        # must sanitize input
        return []

class UserRoles(Resource):
    def get(self, user_id):
        # must sanitize input
        return []

class Roles(Resource):
    def get(self):
        return []
        # conn = db_connect.connect()
        # query = conn.execute("select * from roles")
        # return [{ 'id': i[0], 'description': i[1]} for i in query.cursor.fetchall()]

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
    api.add_resource(UserRoles, '/api/v1/users/<string:user_id>/roles')
    api.add_resource(Roles, '/api/v1/roles')

    return app
