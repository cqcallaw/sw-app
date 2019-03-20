""" SW auth app forms """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class LoginForm(FlaskForm):
    """ Login Form """
    user_id = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    """ Registration Form """
    user_id = StringField('Username')
    name = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')
