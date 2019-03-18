""" Test basic user functions """
import json
from tests.base import BaseTestCase
from tests.test_auth import login_user, validate_user_login

class TestRole(BaseTestCase):
    """ Test role operations """
    def test_get_role(self):
        """ Test basic GET """
        self.assert200(self.client.get('/api/roles'))
        self.assert200(self.client.get('/api/roles/admin'))

    def test_create_role_unauthorized(self):
        """ Test role creation from unprivileged account """
        data = {
            'role_id': 'backup',
            'description': 'Backup Operators',
        }

        response = self.client.post(
            '/api/roles',
            data=json.dumps(data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)

    def test_create_role(self):
        """ Test role creation """
        response = login_user(self.client, 'admin', 'admin')
        auth_token = validate_user_login(self, response)

        data = {
            'role_id': 'backup',
            'description': 'Backup Operators',
        }

        response = self.client.post(
            '/api/roles',
            data=json.dumps(data),
            content_type='application/json',
            headers={'Authorization' : 'Bearer ' + auth_token}
        )

        self.assertEqual(response.status_code, 201)
