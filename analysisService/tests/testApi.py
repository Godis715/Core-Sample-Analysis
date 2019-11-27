import json
import os
import requests
import time


url = 'http://127.0.0.1:5050/api/data_analysis/'

TESTDIR = f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/tests'

data = {
    'deposit': 1,
    'hole': 2,
    'fragments': [
        {
            'top': 0,
            'bottom': 1300,
            'dl_resolution': 100.0,
            'uv_resolution': 100.0,
            'dlImg': f'{TESTDIR}/fragments/fragment1_DL.jpg',
            'uvImg': f'{TESTDIR}/fragments/fragment1_UV.jpg',
        },
        {
            'top': 1300,
            'bottom': 2100,
            'dl_resolution': 100.0,
            'uv_resolution': 100.0,
            'dlImg': f'{TESTDIR}/fragments/fragment2_DL.jpg',
            'uvImg': f'{TESTDIR}/fragments/fragment2_UV.jpg',
        },
        {
            'top': 2100,
            'bottom': 4000,
            'dl_resolution': 100.0,
            'uv_resolution': 100.0,
            'dlImg': f'{TESTDIR}/fragments/fragment3_DL.jpg',
            'uvImg': f'{TESTDIR}/fragments/fragment3_UV.jpg',
        },
        {
            'top': 4000,
            'bottom': 4500,
            'dl_resolution': 100.0,
            'uv_resolution': 100.0,
            'dlImg': f'{TESTDIR}/fragments/fragment4_DL.jpg',
            'uvImg': f'{TESTDIR}/fragments/fragment4_UV.jpg',
        }

    ]
}

files = {
    f"{data['fragments'][0]['dlImg']}": open(f"{data['fragments'][0]['dlImg']}", 'rb'),
    f"{data['fragments'][0]['uvImg']}": open(f"{data['fragments'][0]['uvImg']}", 'rb'),
    f"{data['fragments'][1]['dlImg']}": open(f"{data['fragments'][1]['dlImg']}", 'rb'),
    f"{data['fragments'][1]['uvImg']}": open(f"{data['fragments'][1]['uvImg']}", 'rb'),
    f"{data['fragments'][2]['dlImg']}": open(f"{data['fragments'][2]['dlImg']}", 'rb'),
    f"{data['fragments'][2]['uvImg']}": open(f"{data['fragments'][2]['uvImg']}", 'rb'),
    f"{data['fragments'][3]['dlImg']}": open(f"{data['fragments'][3]['dlImg']}", 'rb'),
    f"{data['fragments'][3]['uvImg']}": open(f"{data['fragments'][3]['uvImg']}", 'rb'),
}
start = time.time()
response_markup = requests.post(url, data={'data': json.dumps(data)}, files=files)
end = time.time()
print(end - start)

print(response_markup.status_code)
print(response_markup.text)
