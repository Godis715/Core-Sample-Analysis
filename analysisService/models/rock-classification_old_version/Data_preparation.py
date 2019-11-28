import os
import pandas as pd
import numpy as np
import shutil
from torchvision import transforms
import torchvision.transforms.functional as tf
from matplotlib import pyplot as plt
from PIL import Image
from pathlib import Path

ALLOW_COPY = False

root = '/home/iref/Datasets/Kern_project'
raw = os.path.join(root, 'raw')

train_dir = os.path.join(root, 'train')
val_dir = os.path.join(root, 'val')
test_dir = os.path.join(root, 'test')

A_train = os.path.join(train_dir, 'A')
P_train = os.path.join(train_dir, 'P')

A_val = os.path.join(val_dir, 'A')
P_val = os.path.join(val_dir, 'P')

A_test = os.path.join(test_dir, 'A')
P_test = os.path.join(test_dir, 'P')


large = os.path.join(root, 'large')

input_size = 100

#os.mkdir(train_dir)
#os.mkdir(val_dir)
#os.mkdir(test_dir)

'''table_frame = pd.read_excel(os.path.join(raw, 'table.xlsx'), usecols='O')
sl = table_frame[3:55]
sl = sl.reindex(np.arange(55))
sl = sl.drop([0, 1, 2])
sl = sl.reset_index(drop=True)
sl = sl.rename(columns={'Unnamed: 14': 'Class'})
print(sl)
print()
print(len(sl))
print()'''


'''if ALLOW_COPY:
    for i in range(52):
        src_root = os.path.join(raw, '{}'.format(i + 1))
        for file in os.listdir(src_root):
            src = os.path.join(src_root, file)
            if 'алевролит' in sl['Class'][i]:
                dst = os.path.join(A_train, file)
                shutil.copyfile(src, dst)
            if 'песчаник' in sl['Class'][i]:
                dst = os.path.join(P_train, file)
                shutil.copyfile(src, dst)'''


'''data_transforms = transforms.RandomResizedCrop(input_size)
for imgname in os.listdir(large):
    if 'алевролит' in imgname:
        path = A_train
        amount = 100
    if 'песчаник'  in imgname:
        path = P_train
        amount = 50
    img = Image.open(os.path.join(large, imgname))
    for i in range(amount):
        tr_img = data_transforms(img)
        tr_img.save(os.path.join(path, 'resized_{1}_{0}'.format(imgname,i)), 'png')
    #ax = plt.subplot(1, 8, i + 1)
    #plt.tight_layout()
    #ax.set_title('#{}'.format(i + 1))
    #plt.imshow(tr_img)'''

#plt.show()

def move_file(file, dst_dir):
    shutil.copyfile(file, dst_dir / file.name)
    file.unlink()


def split_dataset(dataset_dir, validation_fraction, test_fraction, class_id):
    files = [f for f in dataset_dir.iterdir() if f.is_file()]

    validation_files = []
    test_files = []

    for i in range(np.ceil(validation_fraction * len(files)).astype(int)):
        file = np.random.choice(files)
        files.remove(file)
        validation_files.append(file)

    for i in range(np.ceil(test_fraction * len(files)).astype(int)):
        file = np.random.choice(files)
        files.remove(file)
        test_files.append(file)

    validation_dir, t_dir = '', ''
    if class_id == 'A':
        validation_dir = A_val
        t_dir = A_test
    elif class_id == 'P':
        validation_dir = P_val
        t_dir = P_test

    for file in validation_files:
        move_file(file, Path(validation_dir))
    for file in test_files:
        move_file(file, Path(t_dir))


split_dataset(Path(A_train), 0.1, 0.1, 'A')
split_dataset(Path(P_train), 0.1, 0.1, 'P')