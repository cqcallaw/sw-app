""" App controllers """
from flask import render_template

def init(app):
    """ Init app controllers """
    with app.app_context():
        app.add_url_rule('/', view_func=base_handler, methods=['GET'])
        app.add_url_rule('/users', view_func=users_handler, methods=['GET'])
        app.add_url_rule('/users<string:user_id>', view_func=user_handler, methods=['GET'])
        app.add_url_rule('/register', view_func=register_handler, methods=['GET'])

def base_handler():
    """ Base URL handler """
    return render_template('index.html')

def users_handler():
    """ Users view handler """

def user_handler():
    """ User view handler """

def register_handler():
    """ Register view handler """
