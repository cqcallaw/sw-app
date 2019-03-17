""" Test basic user functions """
import json
from tests.base import BaseTestCase

class TestUser(BaseTestCase):
    """ Test basic app configuration """
    def test_get_user(self):
        """ Test basic user GET """
        client = self.client
        self.assert200(client.get('/api/users'))
        self.assert200(client.get('/api/users/alice'))

    def test_create_user(self):
        """ Test basic user POST """
        data = {
            'user_id': 'newkid',
            'name': 'The New Guy',
            'password': 'n',
            'roles': [
                {"role_id": "users"}
            ]
        }

        response = self.client.post(
            '/api/users',
            data=json.dumps(data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        response_data = response.json
        self.assertIn('auth_token', response_data)
        self.assertIsNotNone(response_data['auth_token'])

    def test_create_user_duplicate(self):
        """ Test basic user POST """
        data = {
            'user_id': 'user',
            'name': 'The New Guy',
            'password': 'n',
            'roles': [
                {"role_id": "users"}
            ]
        }

        response = self.client.post(
            '/api/users',
            data=json.dumps(data),
            content_type='application/json',
        )

        self.assert400(response)

    def test_modify_user_no_login(self):
        """ Test basic user PATCH, no auth"""
        data = {'name': 'New Alice'}

        response = self.client.patch(
            '/api/users/alice',
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)
