""" Authentication tests """
import unittest
import json
# from sw_demo_api.models import User
from tests.base import BaseTestCase

class TestAuth(BaseTestCase):
    """ Test authentication """
    def test_malformed_login(self):
        """ Test for malformed """
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(
                {
                    'whatever': 'nemo',
                    'not_password': 'fake'
                }
            )
        )

        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertEqual(data['message'], 'Malformed request: missing user ID.')

    def test_invalid_login_id(self):
        """ Test for invalid user """
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(
                {
                    'user_id': 'nemo',
                    'password': 'fake'
                }
            )
        )

        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertEqual(data['message'], 'User does not exist.')

    def test_invalid_login_password(self):
        """ Test for invalid password """
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(
                {
                    'user_id': 'user',
                    'password': 'fake'
                }
            )
        )

        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertEqual(data['message'], 'Invalid password.')

    def test_valid_login(self):
        """ Test for valid login user """
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(
                {
                    'user_id': 'user',
                    'password': 'user'
                }
            )
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn('auth_token', response_data)
        self.assertIsNotNone(response_data['auth_token'])

if __name__ == '__main__':
    unittest.main()
