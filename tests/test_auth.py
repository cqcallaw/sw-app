""" Authentication tests """
import unittest
import json
# from sw_demo_api.models import User
from tests.base import BaseTestCase

def login_user(client, user_id, password):
    """ Helper function for user login """
    return client.post(
        '/api/auth/login',
        content_type='application/json',
        data=json.dumps(
            {
                'user_id': user_id,
                'password': password
            }
        )
    )

class TestLogin(BaseTestCase):
    """ Test authentication """
    def test_wrong_content_type(self):
        """ Test for wrong content type """
        response = self.client.post(
            '/api/auth/login',
            data=''
        )

        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertEqual(
            data['message'],
            'Login submission does not specific content type (must be application/json).'
        )

    def test_malformed_login(self):
        """ Test for malformed submission """
        response = self.client.post(
            '/api/auth/login',
            content_type='application/json',
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
        response = login_user(self.client, 'nemo', 'fake')

        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertEqual(data['message'], 'User does not exist.')

    def test_invalid_login_password(self):
        """ Test for invalid password """
        response = login_user(self.client, 'user', 'fake')

        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertEqual(data['message'], 'Invalid password.')

    def test_valid_login(self):
        """ Test for valid login user """
        response = login_user(self.client, 'user', 'user')

        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn('auth_token', response_data)
        self.assertIsNotNone(response_data['auth_token'])

class TestLogout(BaseTestCase):
    """ Test logout functions """

    def test_no_auth_header(self):
        """ Test logout without Authentication header """
        response = self.client.post(
            '/api/auth/logout'
        )

        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertEqual(data['message'], 'Logout requires Authorization header.')


    """ Test logout with malformed Authentication header """
    """ Test logout for invalid user """
    """ Test logout after timeout """
    """ Test double logout """
    """ Test for valid logout"""

    # def test_valid_logout(self):
    #     """ Test for valid logout"""
    #     response = login_user(self.client, 'user', 'user')

    #     self.assertEqual(response.status_code, 200)
    #     response_data = response.json
    #     self.assertIn('auth_token', response_data)
    #     self.assertIsNotNone(response_data['auth_token'])

if __name__ == '__main__':
    unittest.main()
