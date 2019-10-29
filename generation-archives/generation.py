import pandas as pd
from zipfile import ZipFile
import random as rnd
import re
import json
import os

MY_PATH_IMPORT = 'H:/Data'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def generation(path_import, path_export, count_archives, isRand=False, step=1):
    # Import data
    data = pd.read_csv(f'{path_import}/data.csv')
    # Create folder of export
    if not os.path.exists(f'{path_export}/sample_archives'):
        os.mkdir(f'{path_export}/sample_archives')

    # For random
    is_allow_gen_archive = True

    index_archive = -1
    count_gen_archives = 0
    description = None
    for i in range(0, data.shape[0] - 1, 2):
        dl_row = dict(data.iloc[i])
        uv_row = dict(data.iloc[i + 1])
        # New sample
        if dl_row['PhotoTop'] == 0.00 or uv_row['PhotoTop'] == 0.00:
            # Finish generate
            if is_allow_gen_archive and index_archive % step == 0 and i != 0:
                # Export description to .json file (temporarily)
                with open(f'{BASE_DIR}/description.json', 'w') as description_file:
                    json.dump(description, description_file, indent=4)
                # Upload .json file to archive
                with ZipFile(f'{path_export}/sample_archives/sample_archive_{index_archive}.zip',
                             'a') as sample_archive:
                    sample_archive.write(f'{BASE_DIR}/description.json', 'sample/description.json')
                # Delete .json file
                os.remove(f'{BASE_DIR}/description.json')
                count_gen_archives += 1
                print(f'gen: sample_archive_{index_archive}.zip')

            if isRand:
                is_allow_gen_archive = rnd.randint(0, 1)
            index_archive += 1
            # Begin generate
            if is_allow_gen_archive and index_archive % step == 0:
                if count_gen_archives == count_archives:
                    break
                description = {
                    'deposit': int(re.search(r'\d+', dl_row['Field']).group(0)),
                    'hole': int(re.search(r'\d+', dl_row['Well']).group(0)),
                    'fragments': []
                }
        # Generate fragment
        if is_allow_gen_archive and index_archive % step == 0:
            dl_image_name = f"{dl_row['Id']}.jpeg"
            uv_image_name = f"{uv_row['Id']}.jpeg"
            # Upload images of fragment to archive
            with ZipFile(f'{path_export}/sample_archives/sample_archive_{index_archive}.zip', 'a') as sample_archive:
                dl_image_path = f"{path_import}/{dl_row['Folder']}/data"
                uv_image_path = f"{path_import}/{uv_row['Folder']}/data"
                sample_archive.write(f"{dl_image_path}/{dl_image_name}", f"sample/{dl_image_name}")
                sample_archive.write(f"{uv_image_path}/{uv_image_name}", f"sample/{uv_image_name}")
            # Add info about fragment to description
            description['fragments'].append({
                'dlImg': dl_image_name,
                'uvImg': uv_image_name,
                'top': int(dl_row['PhotoTop'] * 100),
                'bottom': int(uv_row['PhotoDown'] * 100)
            })


def main():
    print('''
__________________________________________________
    > Path of import: absolute path of folder with data.csv and images
        *Skip (Press enter) --> path of author this script ('H:/Data')
    > Path of export: absolute path of folder where folder ('sample_archives') with archives will be created
        *Skip (Press enter) --> path of this script
    > Count archives: max count of archives
        * Not to be skipped
    > With random: y/n (ability to skip some archives)
        *Skip (Press enter) --> default value (No)
    > Step: integer (viewing step)
        *Skip (Press enter) --> default value (1)
    
If turn on the random or/and raise the step then the time of generating will increase! 
__________________________________________________
    ''')

    path_import = input('*Path of import: ')
    path_import = path_import if path_import != '' else MY_PATH_IMPORT
    if not os.path.exists(path_import):
        print('Path not correct!')
        return

    path_export = input('Path of export: ')
    path_export = path_export if path_export != '' else BASE_DIR
    if not os.path.exists(path_import):
        print('Path not correct!')
        return

    count_archives = input('*Count archives: ')
    if count_archives == '' or not count_archives.isdigit():
        print('Not correct value!')
        return

    isRand = input('With random: ')
    if isRand not in ['y', 'n', '']:
        print('Not correct value!')
        return
    isRand = True if isRand == 'y' else False

    step = input('Step: ')
    if not (step == '' or step.isdigit()):
        print('Not correct value!')
        return
    step = int(step) if step != '' else 1

    print('------ List gen ------')
    generation(path_import, path_export, int(count_archives), isRand=isRand, step=step)


if __name__ == '__main__':
    main()
