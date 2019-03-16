from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'

    id = Column(String, primary_key=True)
    description = Column(String)
    users = relationship(
        'User',
        secondary='user_roles'
    )

    def __repr__(self):
        return "<Role(id='%s', description='%s')>" % (self.id, self.description)

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    name = Column(String)
    roles = relationship(
        'Role',
        secondary='user_roles'
    )

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)

class UserRoles(Base):
    __tablename__ = 'user_roles'

    role_id = Column(String, ForeignKey('roles.id'), primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), primary_key=True)

    def __repr__(self):
        return "<UserRole(role_id='%s', user_id='%s')>" % (self.role_id, self.user_id)

def init_db(db_path, engine, session_maker):
    Base.metadata.create_all(engine)

    s = session_maker()
    s.add(Role(id='admin', description='Administrators'))
    s.add(Role(id='users', description='users'))
    s.add(User(id='admin', name='The Administrator'))
    s.add(User(id='user', name='A user'))
    s.commit()

