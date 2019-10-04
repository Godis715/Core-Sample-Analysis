import requests
import os
import hashlib

url = 'http://127.0.0.1:5050/api/data_analysis/'
fileobj = open(os.path.join(os.path.dirname(__file__), 'testZip.zip'), 'rb')
print(fileobj)
r = requests.post(url, files={"archive": ("testZip.zip", fileobj)})

print(r.status_code)
print(r.text)

