from joblib import load
from PIL import Image, ImageStat
import numpy as np
import cv2
import os
path = os.path.dirname(os.path.abspath(__file__))
model = load(path+'/oil_6ch.joblib')

def get_preds(crops):
    X = []

    for crop, dl_crop in crops:
        crop_arr = np.array(crop)
        img_hsv = cv2.cvtColor(crop_arr, cv2.COLOR_RGB2HSV)
        img_gray = cv2.cvtColor(crop_arr, cv2.COLOR_RGB2GRAY)
        mean_hue, mean_sat, mean_val = ImageStat.Stat(crop).mean

        dark = (0, 0, mean_val/2)
        light = (179, 255, 255)
        mask_yel = cv2.inRange(img_hsv, dark, light)
        img_yel = cv2.bitwise_and(img_gray, img_gray, mask=mask_yel)
        mask_intensity = sum([sum(row) for row in img_yel])

        size = len(crop_arr) * len(crop_arr[0])
        area = sum([sum([0 if pxl == 0 else 1 for pxl in row])for row in img_yel])
        intensity = mask_intensity / (mean_val*area) if area != 0 else 0
        
        dl = np.array(dl_crop)
        dl_hsv = cv2.cvtColor(dl, cv2.COLOR_RGB2HSV)
        pil_dl = Image.fromarray(dl_hsv)
        dl_hue, dl_sat, dl_val = ImageStat.Stat(pil_dl).mean
        
        features = [
            area / size,
            intensity,
            mean_hue,
            mean_sat,
            mean_val,
            dl_hue,
            dl_sat,
            dl_val
        ]
        X.append(features)
    
    preds = model.predict(X)
    return preds