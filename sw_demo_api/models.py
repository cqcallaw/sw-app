from sw_demo_api import db

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Unicode, primary_key=True)
    description = db.Column(db.Unicode)
    users = db.relationship(
        'User',
        secondary='user_roles'
    )

    def __repr__(self):
        return "<Role(id='%s', description='%s')>" % (self.id, self.description)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Unicode, primary_key=True)
    name = db.Column(db.Unicode)
    roles = db.relationship(
        'Role',
        secondary='user_roles'
    )

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'

    role_id = db.Column(db.String, db.ForeignKey('roles.id'), primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), primary_key=True)

    def __repr__(self):
        return "<UserRole(role_id='%s', user_id='%s')>" % (self.role_id, self.user_id)
