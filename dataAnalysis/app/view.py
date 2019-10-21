from app import app
from flask import jsonify, abort, make_response, request

import json
import io

from PIL import Image
from time import sleep

from analysisModels.mock import analyse


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/data_analysis/', methods=['POST'])
def data_analysis():
    data = json.loads(request.form['data'])

    fragments = data.pop('fragments')
    data['fragments'] = []
    for fragment in fragments:
        data['fragments'].append({
            'top': fragment['top'],
            'bottom': fragment['bottom'],
            'dlImg': Image.open(io.BytesIO(request.files[fragment['dlImg']].read())),
            'uvImg': Image.open(io.BytesIO(request.files[fragment['uvImg']].read()))
        })

    return make_response(jsonify({'markup': analyse(data)}), 200)

