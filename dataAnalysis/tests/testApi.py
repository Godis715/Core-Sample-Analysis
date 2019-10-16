import requests
import os
import hashlib

url = 'http://127.0.0.1:5050/api/data_analysis/'
#sample-testError.zip
fileobj = open(os.path.join(os.path.dirname(__file__), 'sample.zip'), 'rb')
#fileobj = open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'rb') # <-- Error
r = requests.post(url, files={"archive": ("sample.zip", fileobj)})

print(r.status_code)
print(r.text)

