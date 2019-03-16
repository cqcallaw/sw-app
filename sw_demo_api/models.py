from sw_demo_api import db
from sqlalchemy import ForeignKey, Column, Integer, Unicode
from sqlalchemy.orm import relationship

class Role(db.Model):
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
    __tablename__ = 'users'

    id = Column(Unicode, primary_key=True)
    name = Column(Unicode)
    roles = relationship(
        'Role',
        secondary='user_roles'
    )

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'

    role_id = Column(Unicode, ForeignKey('roles.id'), primary_key=True)
    user_id = Column(Unicode, ForeignKey('users.id'), primary_key=True)

    def __repr__(self):
        return "<UserRole(role_id='%s', user_id='%s')>" % (self.role_id, self.user_id)
