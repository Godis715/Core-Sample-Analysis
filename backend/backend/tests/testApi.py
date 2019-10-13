import requests
import json
import os

url = 'http://127.0.0.1:8000/api/'

data = {
    "username": "dima12101",
    "password": "Lbvf12101"
}
response = requests.post(f'{url}login', data=data)
if response.status_code == 200:
    token = json.loads(response.text).get('token')
    print(token)
else:
    print(response.status_code)
    error = json.loads(response.text).get('error')
    print(error)
    token = None


if token:
    token = f"Token {token}"
    headers = {"Authorization": token}

    file_obj = open(os.path.join(os.path.dirname(__file__), 'sample.zip'), 'rb')
    response = requests.post(f"{url}core_sample/upload", files={"archive": ("sample.zip", file_obj)}, headers=headers)

    print(response.status_code)
    print(response.text)
else:
    print('No Key')


