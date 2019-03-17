""" Initialization tests """
from tests.base import BaseTestCase

class TestConfig(BaseTestCase):
    """ Test basic app configuration """
    def test_app_is_testing(self):
        """ Test testing config info """
        app = self.app
        self.assertFalse(app is None)
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///testing_sw_demo_api.sqlite'
        )
