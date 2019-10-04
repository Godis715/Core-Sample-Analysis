import os

from app import app
from flask import jsonify, abort, make_response, request
from werkzeug.utils import secure_filename


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] == 'zip'


def generate_filename(filename):
    app.config['FILE_ID'] += 1
    id = app.config['FILE_ID']
    filename_parts = filename.split('.', 1)
    return f'{filename_parts[0]}-{id}.{filename_parts[1]}'


@app.route('/api/data_analysis/', methods=['POST'])
def data_analysis():
    file = request.files['archive']
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path_file_load = os.path.join(app.config['UPLOAD_FOLDER'], generate_filename(filename))
        file.save(path_file_load)
        #decoder_zip(path_file_load)
        return 'File load!'
    return 'Error load!'

