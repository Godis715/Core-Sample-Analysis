import os
import io

import xlrd
import json

from zipfile import ZipFile
from PIL import Image

# Types of parameters
ALLOWED_PARAMS_SAMPLE = {'deposit', 'hole', 'fragments'}
ALLOWED_PARAMS_PART = {'dlImg', 'uvImg', 'top', 'bottom'}

# Errors and warnings
ERROR_FORMAT = "File format error (Expected {})"
ERROR_NOT_EXIST_FILE = "file '{}' doesn't exist!"
ERROR_NOT_FOUND_FILE_BY_LINK = "Link points to a non-existent file '{}'!"
ERROR_NOT_CORRECT_SAMPLE_PARAMS = "Description of core sample is not valid!"
ERROR_NOT_CORRECT_PART_PARAMS = "Description of fragment is not valid!"

WARN_NOT_CORRECT_SIZE_IMAGES = "Sizes of images dl('{}'), uv('{}') don't match"
WARN_NOT_USE_ALL_IMAGES = "The archive contains unreferenced images"


def _description_sample_params_isCorrect(params):
    return len(ALLOWED_PARAMS_SAMPLE - set(params)) == 0 and len(ALLOWED_PARAMS_SAMPLE) == len(params)


def _description_part_params_isCorrect(params):
    return len(ALLOWED_PARAMS_PART - set(params)) == 0 and len(ALLOWED_PARAMS_PART) == len(params)


def _use_all_images(list_all_paths_img,  list_use_path_img):
    return len(set(list_all_paths_img) - set(list_use_path_img)) == 0 and len(list_all_paths_img) == len(list_use_path_img)


def archiveDecode(archive):
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
    {'Type': 'Success', 'Data': sample_data, 'Warnings': warnings}
    """

    """sample_data = 
    {   
        sample params ...
        fragments:
        [
            {
                'image_DL': PIL_image,
                'image_UV': PIL_image,
                fragment params...
            },
            ...
        ]
    }
    """
    warnings = []
    use_path_images = []

    root_folder = archive.namelist()[0].split('/')[0] + '/'
    path_file_description = f'{root_folder}description'
    # Checking: [exist] - [file of description (.json or .xlsx format)]
    if f'{path_file_description}.json' in archive.namelist():
        """ Expected struct of description:
        {   
        sample params ...
        fragments:
        [
            {
                'image_DL': src,
                'image_UV': src,
                fragment params...
            },
            ...
        ]
        }
        """
        with archive.open(f'{path_file_description}.json') as file_description_json:

            # Loading: file of description in python dictionary
            file_bytes = file_description_json.read()
            sample_data = json.loads(file_bytes.decode("utf-8"))

            # Checking: [correct] - [name of parameters of core sample]
            if not _description_sample_params_isCorrect(sample_data.keys()):
                return {'Type': 'Error', 'Message': ERROR_NOT_CORRECT_SAMPLE_PARAMS}  # <--- Error

            parts = []
            for description_part in sample_data.pop('fragments'):

                # Checking: [correct] - [name of parameters of fragment]
                if not _description_part_params_isCorrect(description_part.keys()):
                    return {'Type': 'Error', 'Message': ERROR_NOT_CORRECT_PART_PARAMS}  # <--- Error

                # Loading: images from archive by links
                part = {}
                for param, value in description_part.items():
                    if param == 'dlImg' or param == 'uvImg':
                        # Checking: [exist] - [image in archive by link]
                        if f'{root_folder}{value}' not in archive.namelist():
                            return {'Type': 'Error',
                                    'Message': ERROR_NOT_FOUND_FILE_BY_LINK.format('image')}  # <--- Error
                        type_image = param[:2]  # DL or UV
                        use_path_images.append(f'{root_folder}{value}')
                        with archive.open(f'{root_folder}{value}') as image:
                            stream = io.BytesIO(image.read())
                            nameField = f'{type_image}Img'
                            part[nameField] = Image.open(stream)
                            part[nameField].filename = value
                    else:
                        part[param] = value

                # Checking: [correct] - [sizes of images: DL and UV]
                if part['dlImg'].size[0] != part['uvImg'].size[0] or part['dlImg'].size[1] != part['uvImg'].size[1]:
                    warnings.append(WARN_NOT_CORRECT_SIZE_IMAGES.format(part['dlImg'].filename, part['uvImg'].filename))

                parts.append(part)
            sample_data['fragments'] = parts
    elif f'{path_file_description}.xlsx' in archive.namelist():
        """ Expected struct of description:
            
        """
        sample_data = {}
        with archive.open(f'{path_file_description}.xlsx') as file_description_xlsx:

            # Loading: file of description in xlrd object
            file_bytes = file_description_xlsx.read()
            workbook = xlrd.open_workbook(file_contents=file_bytes)
            sheet = workbook.sheet_by_index(0)

            # Get name of parameters of core sample
            sample_header = set(sheet.row_values(0))
            sample_header.remove('')
            sample_header = list(sample_header)
            # Checking: [correct] - [name of parameters of core sample]
            if not _description_sample_params_isCorrect(sample_header):
                return {'Type': 'Error', 'Message': ERROR_NOT_CORRECT_SAMPLE_PARAMS}  # <--- Error

            # Loading: parameters of core sample in python dictionary
            for col_num in range(len(sample_header)):
                if sample_header[col_num] != 'fragments':
                    sample_data[sample_header[col_num]] = sheet.cell(1, col_num).value
                else:
                    sample_data['fragments'] = []
            col_num_parts = len(sample_header) - 1

            # Get name of parameters of fragment
            parts_header = sheet.row_values(rowx=1, start_colx=col_num_parts)
            # Checking: [correct] - [name of parameters of fragment]
            if not _description_part_params_isCorrect(parts_header):
                return {'Type': 'Error', 'Message': ERROR_NOT_CORRECT_PART_PARAMS}  # <--- Error

            # Loading: parameters of fragment in python dictionary
            for row_num in range(2, sheet.nrows):
                part = {}
                for col_num in range(col_num_parts, sheet.ncols):
                    if parts_header[col_num - col_num_parts] == 'dlImg' or parts_header[col_num - col_num_parts] == 'uvImg':
                        # Checking: [exist] - [image in archive by link]
                        if f'{root_folder}{sheet.cell(row_num, col_num).value}' not in archive.namelist():
                            return {'Type': 'Error',
                                    'Message': ERROR_NOT_FOUND_FILE_BY_LINK.format('image')}  # <--- Error
                        type_image = parts_header[col_num - col_num_parts][:2]  # DL or UV
                        use_path_images.append(f'{root_folder}{sheet.cell(row_num, col_num).value}')
                        with archive.open(f'{root_folder}{sheet.cell(row_num, col_num).value}') as image:
                            stream = io.BytesIO(image.read())
                            nameField = f'{type_image}Img'
                            part[nameField] = Image.open(stream)
                            part[nameField].filename = sheet.cell(row_num, col_num).value
                    else:
                        part[parts_header[col_num - col_num_parts]] = sheet.cell(row_num, col_num).value

                if part['dlImg'].size[0] != part['uvImg'].size[0] or part['dlImg'].size[1] != part['uvImg'].size[1]:
                    warnings.append(WARN_NOT_CORRECT_SIZE_IMAGES.format(part['dlImg'].filename, part['uvImg'].filename))

                sample_data['fragments'].append(part)
    else:
        return {'Type': 'Error', 'Message': ERROR_NOT_EXIST_FILE.format('description.(json/xlsx)')}  # <--- Error

    all_path_images = archive.namelist()
    if root_folder in archive.namelist():
        all_path_images.remove(root_folder)

    if f'{root_folder}description.json' in archive.namelist():
        all_path_images.remove(f'{root_folder}description.json')
    if f'{root_folder}description.xlsx' in archive.namelist():
        all_path_images.remove(f'{root_folder}description.xlsx')
    # Checking: [exist] - [unnecessary files]
    if not _use_all_images(all_path_images, use_path_images):
        warnings.append(WARN_NOT_USE_ALL_IMAGES)

    return {'Type': 'Success', 'Data': sample_data, 'Warnings': warnings}  # <--- result


if __name__ == "__main__":
    zip_archive = ZipFile(os.path.join(os.path.dirname(__file__), 'tests/sample_archive_40.zip'))
    data = archiveDecode(zip_archive)
    zip_archive.close()
    print(data)
    for warn in data['Warnings']:
        print(warn)
