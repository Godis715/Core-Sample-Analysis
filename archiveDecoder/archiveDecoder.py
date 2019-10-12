import os
import io

import xlrd
import json

from zipfile import ZipFile
from PIL import Image


ALLOWED_PARAMS_SAMPLE = {'deposit', 'hole', 'parts'}
ALLOWED_PARAMS_PART = {'nameImg_DL', 'nameImg_UV', 'begin_part', 'end_part'}

ERROR_FORMAT = 'Error format file (Expected {})'
NOT_EXIST_FILE = '{} file not exist!'
NOT_FOUND_FILE_BY_LINK = 'Not found {} by link!'
NOT_CORRECT_SAMPLE_PARAMS = 'Description params of sample is not correct!'
NOT_CORRECT_PART_PARAMS = 'Description params of part is not correct!'


def _description_sample_params_isCorrect(params):
    return len(ALLOWED_PARAMS_SAMPLE - set(params)) == 0 and len(ALLOWED_PARAMS_SAMPLE) == len(params)


def _description_part_params_isCorrect(params):
    return len(ALLOWED_PARAMS_PART - set(params)) == 0 and len(ALLOWED_PARAMS_PART) == len(params)


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
    {'Type': 'Success', 'Data': sample_data}
    """

    """sample_data = 
    {   
        sample params ...
        parts:
        [
            {
                'image_DL': PIL_image,
                'image_UV': PIL_image,
                other params...
            },
            ...
        ]
    }
    """
    root_folder = archive.namelist()[0]
    path_file_description = f'{root_folder}description'
    if f'{path_file_description}.json' in archive.namelist():
        with archive.open(f'{path_file_description}.json') as file_description_json:
            file_bytes = file_description_json.read()
            sample_data = json.loads(file_bytes.decode("utf-8"))
            if not _description_sample_params_isCorrect(data.keys()):
                return {'Type': 'Error', 'Message': NOT_CORRECT_SAMPLE_PARAMS}  # <--- Error
            parts = []
            for description_part in sample_data.pop('parts'):
                if not _description_part_params_isCorrect(description_part.keys()):
                    return {'Type': 'Error', 'Message': NOT_CORRECT_PART_PARAMS}  # <--- Error
                part = {}
                for param, value in description_part.items():
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
                parts.append(part)
            sample_data['parts'] = parts
        return {'Type': 'Success', 'Data': sample_data}  # <--- result
    elif f'{path_file_description}.xlsx' in archive.namelist():
        sample_data = {}
        with archive.open(f'{path_file_description}.xlsx') as file_description_xlsx:
            file_bytes = file_description_xlsx.read()
            workbook = xlrd.open_workbook(file_contents=file_bytes)
            sheet = workbook.sheet_by_index(0)

            sample_header = set(sheet.row_values(0))
            sample_header.remove('')
            sample_header = list(sample_header)
            if not _description_sample_params_isCorrect(sample_header):
                return {'Type': 'Error', 'Message': NOT_CORRECT_SAMPLE_PARAMS}  # <--- Error
            for col_num in range(len(sample_header)):
                if sample_header[col_num] != 'parts':
                    sample_data[sample_header[col_num]] = sheet.cell(1, col_num).value
                else:
                    sample_data['parts'] = []
            col_num_parts = len(sample_header) - 1

            parts_header = sheet.row_values(rowx=1, start_colx=col_num_parts)
            if not _description_part_params_isCorrect(parts_header):
                return {'Type': 'Error', 'Message': NOT_CORRECT_PART_PARAMS}  # <--- Error

            for row_num in range(2, sheet.nrows):
                part = {}
                for col_num in range(col_num_parts, sheet.ncols):
                    if parts_header[col_num - col_num_parts] == 'nameImg_DL' or parts_header[col_num - col_num_parts] == 'nameImg_UV':
                        if f'{root_folder}{sheet.cell(row_num, col_num).value}' not in archive.namelist():
                            return {'Type': 'Error',
                                    'Message': NOT_FOUND_FILE_BY_LINK.format('image')}  # <--- Error
                        type_image = parts_header[col_num - col_num_parts].split('_')[1]  # DL or UV
                        with archive.open(f'{root_folder}{sheet.cell(row_num, col_num).value}') as image:
                            stream = io.BytesIO(image.read())
                            part[f'image_{type_image}'] = Image.open(stream)
                    else:
                        part[parts_header[col_num - col_num_parts]] = sheet.cell(row_num, col_num).value
                sample_data['parts'].append(part)

        return {'Type': 'Success', 'Data': sample_data}  # <--- result
    else:
        return {'Type': 'Error', 'Message': NOT_EXIST_FILE.format('description.(json/xlsx)')}  # <--- Error


if __name__ == "__main__":
    zip_archive = ZipFile(os.path.join(os.path.dirname(__file__), 'sample.zip'))
    data = decode_archive(zip_archive)
    zip_archive.close()
    print(data)
