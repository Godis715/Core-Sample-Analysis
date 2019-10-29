import pandas as pd
from zipfile import ZipFile
import random as rnd
import json
import os

MY_PATH_IMPORT = 'H:/Data'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def generation(path_import, path_export, count_archives):
    data = pd.read_csv(f'{path_import}/data.csv')
    if not os.path.exists(f'{path_export}/sample_archives'):
	    os.mkdir(f'{path_export}/sample_archives')
    index_archive = -1
    description = None
    for i in range(0, data.shape[0] - 1, 2):
        dl_row = dict(data.iloc[i])
        uv_row = dict(data.iloc[i + 1])
        if dl_row['PhotoTop'] == 0.00 or uv_row['PhotoTop'] == 0.00:
            if i != 0:
                with open(f'{BASE_DIR}/description.json', 'w') as description_file:
                    json.dump(description, description_file, indent=4)
                with ZipFile(f'{path_export}/sample_archives/sample_archive_{index_archive}.zip', 'a') as sample_archive:
                    sample_archive.write(f'{BASE_DIR}/description.json', 'sample/description.json')
                os.remove(f'{BASE_DIR}/description.json')
                print(f'gen: sample_archive_{index_archive}.zip')
            index_archive += 1
            if index_archive == count_archives:
            	break
            description = {
                'deposit': rnd.randint(1, 10),
                'hole': rnd.randint(1, 10),
                'fragments': []
            }
        dl_image_name = f"{dl_row['Id']}.jpeg"
        uv_image_name = f"{uv_row['Id']}.jpeg"
        with ZipFile(f'{path_export}/sample_archives/sample_archive_{index_archive}.zip', 'a') as sample_archive:
            dl_image_path = f"{path_import}/{dl_row['Folder']}/data"
            uv_image_path = f"{path_import}/{uv_row['Folder']}/data"
            sample_archive.write(f"{dl_image_path}/{dl_image_name}", f"sample/{dl_image_name}")
            sample_archive.write(f"{uv_image_path}/{uv_image_name}", f"sample/{uv_image_name}")
        description['fragments'].append({
            'dlImg': dl_image_name,
            'uvImg': uv_image_name,
            'top': int(dl_row['PhotoTop'] * 100),
            'bottom': int(uv_row['PhotoDown'] * 100)
        })


def generation_random(path_import, path_export, count_archives):
    data = pd.read_csv(f'{path_import}/data.csv')
    if not os.path.exists(f'{path_export}/sample_archives'):
	    os.mkdir(f'{path_export}/sample_archives')
    index_archive = -1
    count_gen = -1
    description = None
    is_allow_gen = False
    for i in range(0, data.shape[0] - 1, 2):
        dl_row = dict(data.iloc[i])
        uv_row = dict(data.iloc[i + 1])
        if dl_row['PhotoTop'] == 0.00 or uv_row['PhotoTop'] == 0.00:
            if i != 0 and is_allow_gen:
                with open(f'{BASE_DIR}/description.json', 'w') as description_file:
                    json.dump(description, description_file, indent=4)
                with ZipFile(f'{path_export}/sample_archives/sample_archive_{index_archive}.zip', 'a') as sample_archive:
                    sample_archive.write(f'{BASE_DIR}/description.json', 'sample/description.json')
                os.remove(f'{BASE_DIR}/description.json')
                print(f'gen: sample_archive_{index_archive}.zip')
       	    is_allow_gen = rnd.randint(0, 1)
            if is_allow_gen:
                count_gen += 1
                if count_gen == count_archives:
                    break
                description = {
                    'deposit': rnd.randint(1, 10),
                    'hole': rnd.randint(1, 10),
                    'fragments': []
                }
            index_archive += 1
        if is_allow_gen:
	        dl_image_name = f"{dl_row['Id']}.jpeg"
	        uv_image_name = f"{uv_row['Id']}.jpeg"
	        with ZipFile(f'{path_export}/sample_archives/sample_archive_{index_archive}.zip', 'a') as sample_archive:
	            dl_image_path = f"{path_import}/{dl_row['Folder']}/data"
	            uv_image_path = f"{path_import}/{uv_row['Folder']}/data"
	            sample_archive.write(f"{dl_image_path}/{dl_image_name}", f"sample/{dl_image_name}")
	            sample_archive.write(f"{uv_image_path}/{uv_image_name}", f"sample/{uv_image_name}")
	        description['fragments'].append({
	            'dlImg': dl_image_name,
	            'uvImg': uv_image_name,
	            'top': int(dl_row['PhotoTop'] * 100),
	            'bottom': int(uv_row['PhotoDown'] * 100)
	        })


def main():

    path_import = input('Path of import: ')
    path_import = path_import if path_import != '' else MY_PATH_IMPORT
    if not os.path.exists(path_import):
    	print('Path not correct!')
    	return


    path_export = input('Path of export: ')
    path_export = path_export if path_export != '' else BASE_DIR
    if not os.path.exists(path_import):
    	print('Path not correct!')
    	return

    count_archives = input('Count archives: ')
    if count_archives == '':
        print('Not correct value!')
        return

    type_gen = input('Type gen: ')
    print('------ List gen ------')
    if type_gen == '':
        generation(path_import, path_export, int(count_archives))
    elif type_gen == 'rand':
        generation_random(path_import, path_export, int(count_archives))


if __name__ == '__main__':
    main()
