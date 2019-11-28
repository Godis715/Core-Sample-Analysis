import numpy as np
import torch
from PIL import Image
from torchvision import models, transforms
import torch.nn as nn
import os
path = os.path.dirname(os.path.abspath(__file__))

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

labels_dict = {0:'siltstone', 1:'mudstone', 2:'sandstone', 3:'other'}

def init_model(path):
    model = models.resnet18()
    num_ftrs = model.fc.in_features
    model.fc = nn.Sequential(nn.Linear(num_ftrs, 256),
                             nn.BatchNorm1d(256),
                             nn.ReLU(),
                             nn.Linear(256, 128),
                             nn.BatchNorm1d(128),
                             nn.ReLU(),
                             nn.Linear(128, 3))
    model.to(device)
    model.load_state_dict(torch.load(path, map_location='cpu'))
    model.eval()
    return model


def img_preprocessing(image):
    img = Image.fromarray(image)
    img = transforms.Resize((224, 224))(img)
    tensor = transforms.ToTensor()(img)
    tensor = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])(tensor)
    tensor = torch.unsqueeze(tensor, 0)
    tensor = tensor.to(device)
    return tensor

def image_pass(image, wsize):
    heigth, width = np.shape(image)[0], np.shape(image)[1]
    k = heigth // wsize
    model = init_model(path+'/resnet18_ft_v6.pt') #insert path here
    np_img = np.asarray(image)
    result = []
    for i in range(0, k):
        bottom = i * wsize
        top = (i + 1) * wsize
        frame = np_img[bottom : top, :, :]
        prepr_frame = img_preprocessing(frame)
        with torch.no_grad():
            temp = torch.log(model(prepr_frame))
            temp[temp != temp] = 0
            if torch.sum(temp).item() > 0.3:
                pred = labels_dict[torch.argmax(model(prepr_frame)).item()]
            else:
                pred = labels_dict[3]
        result.append((bottom, top, pred))

    last_frame = np_img[k * wsize : heigth, :, :]
    prepr_frame = img_preprocessing(last_frame)
    with torch.no_grad():
        temp = torch.log(model(prepr_frame))
        temp[temp != temp] = 0
        if torch.sum(temp).item() > 0.3:
            pred = labels_dict[torch.argmax(model(prepr_frame)).item()]
        else:
            pred = labels_dict[3]
    result.append((k * wsize, heigth, pred))
    return result



