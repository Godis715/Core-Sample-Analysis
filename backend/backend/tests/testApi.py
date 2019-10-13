import requests
import json
import os

# from Crypto.Cipher import AES
# import chardet
# data = b'8'
#
# key = b'a))4y#r=rd&8)nyu54_vlw)vv)fzpjh4)$@j4%d@9rm)uh5f@f'[:16]
# cipher = AES.new(key, AES.MODE_EAX)
#
# nonce = cipher.nonce
# ciphertext, mac = cipher.encrypt_and_digest(data)
#
# nonce_code = chardet.detect(nonce)
# ciphertext_code = chardet.detect(ciphertext)
# mac_code = chardet.detect(mac)
#
# nonce_str = "".join(map(chr, nonce))
# ciphertext_str = "".join(map(chr, ciphertext))
# mac_str = "".join(map(chr, mac))
#
# NCM = '###'.join([nonce_str, ciphertext_str, mac_str])
#
# nonce_str, ciphertext_str, mac_str = NCM.split('###')
# nonce = nonce_str.encode('utf-8')
# ciphertext = ciphertext_str.encode('utf-8')
# mac = mac_str.encode('utf-8')
#
# cipher = AES.new(key, AES.MODE_EAX, nonce)
# data = cipher.decrypt_and_verify(ciphertext, mac)


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
    response = requests.post(f"{url}core_sample/upload",
                             files={"archive": ("sample.zip", file_obj)},
                             data={'csName': 'Тест'},
                             headers=headers)
    print(response.status_code)
    print(response.text)
else:
    print('No Key')


