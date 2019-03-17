""" SW Demo REST API """
import os
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import flask_restless

app = flask.Flask(__name__)

BCRYPT_HANDLE = Bcrypt(app)

# Create our SQLAlchemy DB engine
db_path = 'sw_demo_api.sqlite'

# purge existing data, for demo purposes
db_file_system_path = os.path.realpath(os.path.join('sw_demo_api', db_path))
if os.path.exists(db_file_system_path):
    os.remove(db_file_system_path)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file_system_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from .models import User, Role, UserRoles

db.create_all()

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

from .controllers import ROLE_API_BLUEPRINT, USER_API_BLUEPRINT
app.register_blueprint(ROLE_API_BLUEPRINT)
app.register_blueprint(USER_API_BLUEPRINT)

def sample_data_init():
    """ populate DB with sample data """

    admin_role = Role(role_id='admin', description='Administrators')
    user_role = Role(role_id='users', description='users')

    admin_user = User(
        user_id='admin',
        name='The Administrator',
        password='admin',
        roles=[admin_role, user_role]
    )

    plain_user = User(user_id='user', name='A user', password='user', roles=[user_role])
    alice = User(user_id='alice', name='Alice', password='a', roles=[user_role])
    bob = User(user_id='bob', name='Bob', password='b', roles=[user_role])
    eve = User(user_id='eve', name='Eve', password='e', roles=[user_role])

    db.session.add(admin_role)
    db.session.add(user_role)
    db.session.add(admin_user)
    db.session.add(plain_user)
    db.session.add(alice)
    db.session.add(bob)
    db.session.add(eve)
    db.session.commit()

sample_data_init()