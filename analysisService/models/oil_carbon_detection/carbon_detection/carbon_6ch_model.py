from joblib import load
from PIL import Image, ImageStat
import numpy as np
import cv2
import os
path = os.path.dirname(os.path.abspath(__file__))
model = load(path+'/carbon_6ch.joblib')

def get_preds(crops):
    X = []

    for crop, dl_crop in crops:
        img = np.array(crop)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        pil_img = Image.fromarray(img_hsv)
        mean_hue, mean_sat, mean_val = ImageStat.Stat(pil_img).mean
        img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

        dark = (0,0,5)
        light = (20,255,200)
        mask_orange = cv2.inRange(img_hsv, dark, light)
        img_orange = cv2.bitwise_and(img_gray, img_gray, mask=mask_orange)

        dark = (120,0,5)
        light = (180,255,60)
        mask_red = cv2.inRange(img_hsv, dark, light)
        img_red = cv2.bitwise_and(img_gray, img_gray, mask=mask_red)

        img_carbon = cv2.bitwise_or(img_orange, img_red)
        mask_intensity = sum([sum(row) for row in img_carbon])
        size = len(img) * len(img[0])
        area = sum([sum([0 if pxl == 0 else 1 for pxl in row])for row in img_carbon])
        intensity = (mask_intensity) / (mean_val*area) if area != 0 else 0
        
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