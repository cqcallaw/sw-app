import requests
import logging

logging.basicConfig(level=logging.DEBUG)

url = 'http://127.0.0.1:5000/api/users'
headers = {'Content-Type': 'application/json'}

user = {
    'user_id': 'newkid',
    'name': 'The New Guy',
    'password': 'n',
    'roles': [
        {"role_id": "users"}
    ]
}

response = requests.post(url, json=user, headers=headers)
assert response.ok
print(response.json())