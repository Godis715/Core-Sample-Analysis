import os
import io

import xlrd
import json

from zipfile import ZipFile
from PIL import Image


ALLOWED_PARAMS = {'nameImg_DL', 'nameImg_UV', 'deposits', 'hole'}


def _description_params_isCorrect(params):
    return len(ALLOWED_PARAMS - set(params)) == 0 and len(ALLOWED_PARAMS) == len(params)


def decode_archive(path_archive):
    """Decoding zip file with images of sample and file of description (.json or .xlsx format)"""

    """Expected struct:
    -RootFolder
    --image1_DL
    --image1_UV
    ...
    --description
    """

    """Result: 
    {'Type': 'Error', 'Message': '...'}
    or
    {'Type': 'Success', 'Data': samples}
    """

    """samples = 
    [
        {
            'image_DL': PIL_image,
            'image_UV': PIL_image,
            other params...
        },
        ...
    ]
    """

    format_archive = path_archive.rsplit('.', 1)[1]
    if format_archive == 'zip':
        samples = []
        with ZipFile(path_archive) as zip_archive:
            root_folder = zip_archive.namelist()[0]

            path_file_description = f'{root_folder}description'
            if f'{path_file_description}.xlsx' in zip_archive.namelist():
                with zip_archive.open(f'{path_file_description}.xlsx') as file_description_xlsx:
                    file_bytes = file_description_xlsx.read()
                    workbook = xlrd.open_workbook(file_contents=file_bytes)
                    sheet = workbook.sheet_by_index(0)
                    header = sheet.row_values(0)
                    if not _description_params_isCorrect(header):
                        return {'Type': 'Error', 'Message': 'Description params is not correct!'}
                    for row_num in range(1, sheet.nrows):
                        sample = {}
                        for col_num in range(sheet.ncols):
                            if header[col_num] == 'nameImg_DL' or header[col_num] == 'nameImg_UV':
                                if f'{root_folder}{sheet.cell(row_num, col_num).value}' not in zip_archive.namelist():
                                    return {'Type': 'Error', 'Message': 'Not found image by link!'}
                                type_image = header[col_num].split('_')[1] # DL or UV
                                with zip_archive.open(f'{root_folder}{sheet.cell(row_num, col_num).value}') as image:
                                    stream = io.BytesIO(image.read())
                                    sample[f'image_{type_image}'] = Image.open(stream)
                            else:
                                sample[header[col_num]] = sheet.cell(row_num, col_num).value
                        samples.append(sample)
                return {'Type': 'Success', 'Data': samples}
            elif f'{path_file_description}.json' in zip_archive.namelist():
                with zip_archive.open(f'{path_file_description}.json') as file_description_json:
                    file_bytes = file_description_json.read()
                    description_data = json.loads(file_bytes.decode("utf-8"))
                    for description_sample in description_data:
                        if not _description_params_isCorrect(description_sample.keys()):
                            return {'Type': 'Error', 'Message': 'Description params is not correct!'}
                        sample = {}
                        for param, value in description_sample.items():
                            if param == 'nameImg_DL' or param == 'nameImg_UV':
                                if f'{root_folder}{value}' not in zip_archive.namelist():
                                    return {'Type': 'Error', 'Message': 'Not found image by link!'}
                                type_image = param.split('_')[1] # DL or UV
                                with zip_archive.open(f'{root_folder}{value}') as image:
                                    stream = io.BytesIO(image.read())
                                    sample[f'image_{type_image}'] = Image.open(stream)
                            else:
                                sample[param] = value
                        samples.append(sample)
                return {'Type': 'Success', 'Data': samples}
            else:
                return {'Type': 'Error', 'Message': 'Description file not exist!'}
    else:
        return {'Type': 'Error', 'Message': 'Error format file (Expected .zip)'}


if __name__ == "__main__":
    data = decode_archive(os.path.join(os.path.dirname(__file__), 'samples.zip'))
    print(data)
