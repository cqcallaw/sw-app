""" Database helpers """
import os
from auth_demo.models import User, Role
from auth_demo.extensions import DATABASE_INSTANCE

def init(app):
    """ Init DB """
    if app.config['DB_PURGE']:
        db_path = app.config['DATABASE_NAME']
        db_file_system_path = os.path.realpath(os.path.join('auth_demo', db_path))
        if os.path.exists(db_file_system_path):
            os.remove(db_file_system_path)

    with app.app_context():
        DATABASE_INSTANCE.create_all()

    if app.config['SAMPLE_DATA']:
        gen_sample_data(app)

def gen_sample_data(app):
    """ Populate database with sample data """
    with app.app_context():
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

        DATABASE_INSTANCE.session.add(admin_role)
        DATABASE_INSTANCE.session.add(user_role)
        DATABASE_INSTANCE.session.add(admin_user)
        DATABASE_INSTANCE.session.add(plain_user)
        DATABASE_INSTANCE.session.add(alice)
        DATABASE_INSTANCE.session.add(bob)
        DATABASE_INSTANCE.session.add(eve)
        DATABASE_INSTANCE.session.commit()
