""" Test basic user functions """
import json
from tests.base import BaseTestCase
from tests.test_auth import login_user, validate_user_login
from auth_demo.models import User

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
        validate_user_login(self, response)

        data = {'name': 'New User'}

        with self.client.session_transaction() as session:
            session['user_id'] = 'user'
            session['_fresh'] = True

            response = self.client.patch(
                '/api/users/alice',
                data=json.dumps(data),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 401)

    def test_modify_user(self):
        """ Test basic user PATCH """
        response = login_user(self.client, 'user', 'user')
        validate_user_login(self, response)

        data = {'name': 'New User Name'}

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

        user = User.query.get('user')
        self.assertEqual(user.name, 'New User Name')

    def test_modify_user_no_privilege_escalation(self):
        """ Test user can't make themself admin """
        response = login_user(self.client, 'user', 'user')
        validate_user_login(self, response)

        data = {
            'roles': {
                'add': [{'role_id': 'admin'}]
            }
        }

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

        user = User.query.get('user')
        self.assertEqual(len(user.roles), 1)
        self.assertEqual(user.roles[0].role_id, 'users')

    def test_modify_user_admin_assign(self):
        """ Test that admins can raise other admins """
        response = login_user(self.client, 'admin', 'admin')
        validate_user_login(self, response)

        data = {
            'roles': {
                'add': [{'role_id': 'admin'}]
            }
        }

        with self.client.session_transaction() as session:
            session['user_id'] = 'user'
            session['_fresh'] = True

            response = self.client.patch(
                '/api/users/user',
                data=json.dumps(data),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)

            user = User.query.get('user')
            self.assertEqual(len(user.roles), 2)
            self.assertEqual(user.roles[0].role_id, 'users')
            self.assertEqual(user.roles[1].role_id, 'admin')
