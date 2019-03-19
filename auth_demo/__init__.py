""" SW Demo REST API """
import os
import flask
import auth_demo.extensions
import auth_demo.db
import auth_demo.controllers
import auth_demo.config

def create_app(test_config=None):
    """ Create the Flask app for the SW demo REST API """
    app = flask.Flask(__name__)

    if test_config is None:
        # source config based on environment variable or default
        app_settings = os.getenv(
            'APP_SETTINGS',
            'auth_demo.config.Development'
        )
        app.config.from_object(app_settings)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    auth_demo.extensions.register_extensions(app)

    auth_demo.db.init(app)

    auth_demo.controllers.init(app)

    return app
