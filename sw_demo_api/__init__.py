""" SW Demo REST API """
import os
import flask
import flask_restless
import sw_demo_api.extensions
import sw_demo_api.db
import sw_demo_api.controllers

def create_app():
    """ Create the Flask app for the SW demo REST API """
    app = flask.Flask(__name__)

    db_path = 'sw_demo_api.sqlite'
    db_file_system_path = os.path.realpath(os.path.join('sw_demo_api', db_path))

    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file_system_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    sw_demo_api.extensions.register_extensions(app)

    # purge existing DB to avoid schema mismatch
    if os.path.exists(db_file_system_path):
        os.remove(db_file_system_path)

    sw_demo_api.db.init(app)
    sw_demo_api.controllers.init(app)

    return app
