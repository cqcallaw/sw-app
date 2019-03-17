""" Sample new user addition """
import logging
import requests

logging.basicConfig(level=logging.DEBUG)

response = requests.post(
    'http://127.0.0.1:5000/api/users',
    headers={'Content-Type': 'application/json'},
    json={
        'user_id': 'newkid',
        'name': 'The New Guy',
        'password': 'n',
        'roles': [
            {"role_id": "users"}
        ]
    }
)
assert response.ok
print(response.json())
