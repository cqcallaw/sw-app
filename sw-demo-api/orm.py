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

    s.add(admin_role)
    s.add(user_role)
    s.add(admin_user)
    s.add(plain_user)
    s.add(alice)
    s.add(bob)
    s.add(eve)
    s.commit()

