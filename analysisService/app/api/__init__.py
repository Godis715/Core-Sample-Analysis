from flask import jsonify, abort, make_response, request
from flask import Blueprint

from app.analysisModels.analysis import analyse

import json
import io
from PIL import Image


bp = Blueprint('api', __name__)


@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@bp.route("/")
def hello():
    return "Main page of api Service analysis!"

@bp.route('/analyse/', methods=['POST'])
def data_analysis():
    data = json.loads(request.form['data'])

    fragments = data.pop('fragments')
    data['fragments'] = []
    for fragment in fragments:
        data['fragments'].append({
            'top': fragment['top'],
            'bottom': fragment['bottom'],
            'dl_resolution': fragment['dl_resolution'],
            'uv_resolution': fragment['uv_resolution'],
            'dlImg': Image.open(io.BytesIO(request.files[fragment['dlImg']].read())),
            'uvImg': Image.open(io.BytesIO(request.files[fragment['uvImg']].read()))
        })

    return make_response(jsonify({'markup': analyse(data)}), 200)

