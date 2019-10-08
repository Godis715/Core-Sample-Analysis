import requests
import json

data = {
    "username": "dima12101",
    "password": "Lbvf12101"
}
url = "http://localhost:8000/api/login"
response = requests.post(url, data=data)
token = json.loads(response.text).get('token')
print(token)

if token:
    token = f"Token {token}"
    headers = {"Authorization": token}
    response = requests.get("http://localhost:8000/api/testLogin", headers=headers)
    print(response.text)
else:
    print('No Key')


