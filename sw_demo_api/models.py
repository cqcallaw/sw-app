""" SW Demo REST API database models """
from sqlalchemy import ForeignKey, Column, Unicode
from sqlalchemy.orm import relationship
from sw_demo_api.extensions import DATABASE_INSTANCE, BCRYPT_HANDLE

class Role(DATABASE_INSTANCE.Model):
    """ DB model for user role """
    __tablename__ = 'roles'

    role_id = Column(Unicode, primary_key=True)
    description = Column(Unicode)
    users = relationship(
        'User',
        secondary='user_roles'
    )

    def __repr__(self):
        return "<Role(id='%s', description='%s')>" % (self.id, self.description)

class User(DATABASE_INSTANCE.Model):
    """ DB model for user """
    __tablename__ = 'users'

    user_id = Column(Unicode, primary_key=True)
    name = Column(Unicode)
    password = Column(Unicode, nullable=False)
    auth_token = Column(Unicode)
    roles = relationship(
        'Role',
        secondary='user_roles'
    )

    def __init__(self, user_id, name, password, **kwargs):
        self.user_id = user_id
        self.name = name
        self.password = BCRYPT_HANDLE.generate_password_hash(password).decode()
        if 'roles' in kwargs:
            self.roles = kwargs['roles']

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.user_id, self.name)

class UserRoles(DATABASE_INSTANCE.Model):
    """ DB model for M:N relationship between users and roles """
    __tablename__ = 'user_roles'

    role_id = Column(Unicode, ForeignKey('roles.role_id'), primary_key=True)
    user_id = Column(Unicode, ForeignKey('users.user_id'), primary_key=True)

    def __repr__(self):
        return "<UserRole(role_id='%s', user_id='%s')>" % (self.role_id, self.user_id)
