""" SW Demo REST API """
import os
import flask
import sw_demo_api.extensions
import sw_demo_api.db
import sw_demo_api.controllers
import sw_demo_api.config

def create_app():
    """ Create the Flask app for the SW demo REST API """
    app = flask.Flask(__name__)

    app_settings = os.getenv(
        'APP_SETTINGS',
        'sw_demo_api.config.Development'
    )
    app.config.from_object(app_settings)

    sw_demo_api.extensions.register_extensions(app)

    # purge existing DB to avoid schema mismatch
    db_path = sw_demo_api.config.DATABASE_NAME + '.sqlite'
    db_file_system_path = os.path.realpath(os.path.join('sw_demo_api', db_path))
    if os.path.exists(db_file_system_path):
        os.remove(db_file_system_path)

    sw_demo_api.db.init(app)
    sw_demo_api.controllers.init(app)

    return app
