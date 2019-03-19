""" SW Demo test fixtures """
import os
from flask_testing import TestCase
from auth_demo import create_app

class BaseTestCase(TestCase):
    """ Base Tests """
    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.app_instance = None
        self.client = None

    def create_app(self):
        os.environ['APP_SETTINGS'] = 'auth_demo.config.Testing'
        self.app_instance = create_app()
        return self.app_instance

    def setUp(self):
        self.app = self.app_instance
        self.client = self.app.test_client()

    def tearDown(self):
        db_path = self.app.config['DATABASE_NAME']
        db_file_system_path = os.path.realpath(os.path.join('auth_demo', db_path))
        if os.path.exists(db_file_system_path):
            os.remove(db_file_system_path)
