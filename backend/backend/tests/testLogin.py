import requests
import json

data = {
    "username": "dima12101",
    "password": "Lbvf1201"
}
url = "http://localhost:8000/api/login"
response = requests.post(url, data=data)
if response.status_code == '200':
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
    response = requests.get("http://localhost:8000/api/testLogin", headers=headers)
    print(response.status_code)
    print(response.text)
else:
    print('No Key')


