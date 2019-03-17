""" SW Demo test fixtures """
import os
from flask_testing import TestCase
from sw_demo_api import create_app
from sw_demo_api.db import gen_sample_data

class BaseTestCase(TestCase):
    """ Base Tests """
    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.app_instance = None
        self.client = None

    def create_app(self):
        os.environ['APP_SETTINGS'] = 'sw_demo_api.config.Testing'
        self.app_instance = create_app()
        gen_sample_data(self.app_instance)
        return self.app_instance

    def setUp(self):
        self.app = self.app_instance
        self.client = self.app.test_client()

    def tearDown(self):
        db_path = self.app.config['DATABASE_NAME']
        db_file_system_path = os.path.realpath(os.path.join('sw_demo_api', db_path))
        if os.path.exists(db_file_system_path):
            os.remove(db_file_system_path)
