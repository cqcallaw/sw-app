""" Sample user update addition """
import logging
import requests

logging.basicConfig(level=logging.DEBUG)

response = requests.patch(
    'http://127.0.0.1:5000/api/users/alice',
    headers={'Content-Type': 'application/json'},
    json={
        'name': 'New Alice',
    }
)
assert response.ok
print(response.json())
