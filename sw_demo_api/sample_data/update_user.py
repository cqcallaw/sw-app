import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)

url = 'http://127.0.0.1:5000/api/users/alice'
headers = {'Content-Type': 'application/json'}

user = {
    'name': 'New Alice',
}

response = requests.patch(url, json=user, headers=headers)
assert response.ok
print(response.json())