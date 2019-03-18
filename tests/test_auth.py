""" Authentication tests """
import unittest
import json
import time
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

def validate_user_login(test, response):
    """ Validate user login and return auth token """
    test.assertEqual(response.status_code, 200)
    response_data = response.json
    test.assertIn('auth_token', response_data)
    auth_token = response_data['auth_token']
    test.assertIsNotNone(auth_token)

    return auth_token


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
        self.assertEqual(data['message'], 'Operation requires Authorization header.')


    def test_invalid_auth_header(self):
        """ Test logout with malformed Authentication header """
        response = self.client.post(
            '/api/auth/logout',
            headers={'Authorization' : 'Blah'}
        )

        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertEqual(
            data['message'],
            'Operation requires valid auth token in Authorization header.'
        )

    def test_invalid_auth_token(self):
        """ Test logout for invalid token """
        response = self.client.post(
            '/api/auth/logout',
            headers={'Authorization' : 'Bearer gobllegook'}
        )

        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertEqual(
            data['message'],
            'Invalid token. Please log in again.'
        )

    def test_valid_logout(self):
        """ Test for valid logout"""
        login_response = login_user(self.client, 'user', 'user')
        auth_token = validate_user_login(self, login_response)

        response = self.client.post(
            '/api/auth/logout',
            headers={'Authorization' : 'Bearer ' + auth_token}
        )
        data = response.json
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Log out successful.')
        self.assertEqual(response.status_code, 200)

    def test_timed_out_token(self):
        """ Test logout after timeout """
        login_response = login_user(self.client, 'user', 'user')
        auth_token = validate_user_login(self, login_response)

        # wait for token to expire
        time.sleep(6)

        response = self.client.post(
            '/api/auth/logout',
            headers={'Authorization' : 'Bearer ' + auth_token}
        )
        data = response.json
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Signature expired. Please log in again.')
        self.assertEqual(response.status_code, 400)

    def test_blacklisted_token(self):
        """ Test logout for blacklisted token """
        login_response = login_user(self.client, 'user', 'user')
        auth_token = validate_user_login(self, login_response)

        response = self.client.post(
            '/api/auth/logout',
            headers={'Authorization' : 'Bearer ' + auth_token}
        )
        data = response.json
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Log out successful.')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/api/auth/logout',
            headers={'Authorization' : 'Bearer ' + auth_token}
        )
        data = response.json
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Token blacklisted. Please log in again.')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
