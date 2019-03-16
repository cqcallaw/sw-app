""" SW Demo REST API """
import os
import flask
from flask_sqlalchemy import SQLAlchemy
import flask_restless

app = flask.Flask(__name__)

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

from .controllers import role_api_blueprint, user_api_blueprint
app.register_blueprint(role_api_blueprint)
app.register_blueprint(user_api_blueprint)

sample_data_init()

def sample_data_init():
    """ populate DB with sample data """

    admin_role = Role(id='admin', description='Administrators')
    user_role = Role(id='users', description='users')

    admin_user = User(id='admin', name='The Administrator')
    admin_user.roles.append(admin_role)
    admin_user.roles.append(user_role)

    plain_user = User(id='user', name='A user')
    plain_user.roles.append(user_role)

    alice = User(id='alice', name='Alice')
    alice.roles.append(user_role)

    bob = User(id='bob', name='Bob')
    bob.roles.append(user_role)

    eve = User(id='eve', name='Eve')
    eve.roles.append(user_role)

    db.session.add(admin_role)
    db.session.add(user_role)
    db.session.add(admin_user)
    db.session.add(plain_user)
    db.session.add(alice)
    db.session.add(bob)
    db.session.add(eve)
    db.session.commit()
