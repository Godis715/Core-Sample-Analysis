import requests

url = 'http://127.0.0.1:5050/api/data_analysis/'

r = requests.post(url, data={'test': 'test'})

print(r.status_code)
print(r.text)

