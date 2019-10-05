from app import app
from flask import jsonify, abort, make_response, request

from zipfile import ZipFile


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'zip'


@app.route('/api/data_analysis/', methods=['POST'])
def data_analysis():
    file = request.files['archive']
    if allowed_file(file.filename):
        zip_file = ZipFile(file, 'r')
        # result_decode = decode_archive(zip_file)
        # if (result_decode['Type'] == 'Success'):
        #     result_analysis = analysis(result_decode['Data'])
        #     if (result_analysis['Type'] == 'Success'):
        #         return jsonify({'Type': 'Success', 'Data:': result_analysis['Data']})
        #     else:
        #         return jsonify({'Type': 'Error', 'Message:': result_analysis['Message']})
        # else:
        #     return jsonify({'Type': 'Error', 'Message:': result_decode['Message']})
        return 'File load!' #Temp
    return jsonify({'Type': 'Error', 'Message:': 'Error format file (Expected .zip)'})

