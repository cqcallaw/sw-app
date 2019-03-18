""" Test basic user functions """
import json
from tests.base import BaseTestCase
from tests.test_auth import login_user
from sw_demo_api.models import User

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
        self.assertEqual(response.status_code, 400)

    def test_modify_invalid_user(self):
        """ Test basic user PATCH, invalid user"""
        data = {'name': 'New Alice'}

        response = self.client.patch(
            '/api/users/nemo',
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)

    def test_modify_user_wrong_user(self):
        """ Test basic wrong user PATCH """
        response = login_user(self.client, 'user', 'user')

        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn('auth_token', response_data)
        auth_token = response_data['auth_token']
        self.assertIsNotNone(auth_token)

        data = {'name': 'New User'}

        response = self.client.patch(
            '/api/users/alice',
            data=json.dumps(data),
            content_type='application/json',
            headers={'Authorization' : 'Bearer ' + auth_token}
        )
        self.assertEqual(response.status_code, 401)

    def test_modify_user(self):
        """ Test basic user PATCH """
        response = login_user(self.client, 'user', 'user')

        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn('auth_token', response_data)
        auth_token = response_data['auth_token']
        self.assertIsNotNone(auth_token)

        data = {'name': 'New User Name'}

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps(data),
            content_type='application/json',
            headers={'Authorization' : 'Bearer ' + auth_token}
        )
        self.assertEqual(response.status_code, 200)

        user = User.query.filter(User.user_id == 'user').first()
        self.assertEqual(user.name, 'New User Name')
