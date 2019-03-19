""" App controllers """
from flask import render_template

def init(app):
    """ Init app controllers """
    with app.app_context():
        app.add_url_rule('/', view_func=base_handler, methods=['GET'])

def base_handler():
    """ Base URL handler """
    return render_template('index.html')
