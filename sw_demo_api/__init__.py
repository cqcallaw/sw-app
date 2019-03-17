""" SW Demo REST API """
import os
import flask
import sw_demo_api.extensions
import sw_demo_api.db
import sw_demo_api.controllers
import sw_demo_api.config

def create_app(test_config=None):
    """ Create the Flask app for the SW demo REST API """
    app = flask.Flask(__name__)

    if test_config is None:
        # source config based on environment variable or default
        app_settings = os.getenv(
            'APP_SETTINGS',
            'sw_demo_api.config.Development'
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

    sw_demo_api.extensions.register_extensions(app)

    if app.config['DB_PURGE']:
        db_path = app.config['DATABASE_NAME']
        db_file_system_path = os.path.realpath(os.path.join('sw_demo_api', db_path))
        if os.path.exists(db_file_system_path):
            os.remove(db_file_system_path)

    sw_demo_api.db.init(app)
    sw_demo_api.controllers.init(app)

    return app
