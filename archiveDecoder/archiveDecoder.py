import os
import io

import xlrd
import json

from zipfile import ZipFile
from PIL import Image


ALLOWED_PARAMS = {'nameImg_DL', 'nameImg_UV', 'begin_part', 'end_part'}

ERROR_FORMAT = 'Error format file (Expected {})'
NOT_EXIST_FILE = '{} file not exist!'
NOT_FOUND_FILE_BY_LINK = 'Not found {} by link!'
NOT_CORRECT_PARAMS = 'Description params is not correct!'


def _description_params_isCorrect(params):
    return len(ALLOWED_PARAMS - set(params)) == 0 and len(ALLOWED_PARAMS) == len(params)


def decode_archive(archive):
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
    {'Type': 'Success', 'Data': sample_parts}
    """

    """sample_parts = 
    [
        {
            'image_DL': PIL_image,
            'image_UV': PIL_image,
            other params...
        },
        ...
    ]
    """

    sample_parts = []

    root_folder = archive.namelist()[0]
    path_file_description = f'{root_folder}description'
    if f'{path_file_description}.xlsx' in archive.namelist():
        with archive.open(f'{path_file_description}.xlsx') as file_description_xlsx:
            file_bytes = file_description_xlsx.read()
            workbook = xlrd.open_workbook(file_contents=file_bytes)
            sheet = workbook.sheet_by_index(0)
            header = sheet.row_values(0)
            if not _description_params_isCorrect(header):
                return {'Type': 'Error', 'Message': NOT_CORRECT_PARAMS}  # <--- Error
            for row_num in range(1, sheet.nrows):
                part = {}
                for col_num in range(sheet.ncols):
                    if header[col_num] == 'nameImg_DL' or header[col_num] == 'nameImg_UV':
                        if f'{root_folder}{sheet.cell(row_num, col_num).value}' not in archive.namelist():
                            return {'Type': 'Error',
                                    'Message': NOT_FOUND_FILE_BY_LINK.format('image')}  # <--- Error
                        type_image = header[col_num].split('_')[1]  # DL or UV
                        with archive.open(f'{root_folder}{sheet.cell(row_num, col_num).value}') as image:
                            stream = io.BytesIO(image.read())
                            part[f'image_{type_image}'] = Image.open(stream)
                    else:
                        part[header[col_num]] = sheet.cell(row_num, col_num).value
                sample_parts.append(part)
        return {'Type': 'Success', 'Data': sample_parts}  # <--- result
    elif f'{path_file_description}.json' in archive.namelist():
        with archive.open(f'{path_file_description}.json') as file_description_json:
            file_bytes = file_description_json.read()
            description_data = json.loads(file_bytes.decode("utf-8"))
            for description_sample in description_data:
                if not _description_params_isCorrect(description_sample.keys()):
                    return {'Type': 'Error', 'Message': NOT_CORRECT_PARAMS}  # <--- Error
                part = {}
                for param, value in description_sample.items():
                    if param == 'nameImg_DL' or param == 'nameImg_UV':
                        if f'{root_folder}{value}' not in archive.namelist():
                            return {'Type': 'Error',
                                    'Message': NOT_FOUND_FILE_BY_LINK.format('image')}  # <--- Error
                        type_image = param.split('_')[1]  # DL or UV
                        with archive.open(f'{root_folder}{value}') as image:
                            stream = io.BytesIO(image.read())
                            part[f'image_{type_image}'] = Image.open(stream)
                    else:
                        part[param] = value
                sample_parts.append(part)
        return {'Type': 'Success', 'Data': sample_parts}  # <--- result
    else:
        return {'Type': 'Error', 'Message': NOT_EXIST_FILE.format('Description.(xlsx/json)')}  # <--- Error


if __name__ == "__main__":
    zip_archive = ZipFile(os.path.join(os.path.dirname(__file__), 'tests/sample.zip'))
    data = decode_archive(zip_archive)
    zip_archive.close()
    print(data)
