""" SW Demo REST API database models """
from sqlalchemy import ForeignKey, Column, Unicode
from sqlalchemy.orm import relationship
from sw_demo_api import db, BCRYPT_HANDLE

class Role(db.Model):
    """ DB model for user role """
    __tablename__ = 'roles'

    id = Column(Unicode, primary_key=True)
    description = Column(Unicode)
    users = relationship(
        'User',
        secondary='user_roles'
    )

    def __repr__(self):
        return "<Role(id='%s', description='%s')>" % (self.id, self.description)

class User(db.Model):
    """ DB model for user """
    __tablename__ = 'users'

    id = Column(Unicode, primary_key=True)
    name = Column(Unicode)
    password = Column(Unicode, nullable=False)
    roles = relationship(
        'Role',
        secondary='user_roles'
    )

    def __init__(self, id, name, password, roles):
        self.id = id
        self.name = name
        self.password = BCRYPT_HANDLE.generate_password_hash(password).decode()
        self.roles = roles

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)

class UserRoles(db.Model):
    """ DB model for M:N relationship between users and roles """
    __tablename__ = 'user_roles'

    role_id = Column(Unicode, ForeignKey('roles.id'), primary_key=True)
    user_id = Column(Unicode, ForeignKey('users.id'), primary_key=True)

    def __repr__(self):
        return "<UserRole(role_id='%s', user_id='%s')>" % (self.role_id, self.user_id)
