from joblib import load
from PIL import Image, ImageStat
import numpy as np
import cv2
import os
path = os.path.dirname(os.path.abspath(__file__))
model = load(path+'/oil_rfc.joblib')

def get_preds(crops):
    X = []

    for crop in crops:
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

        features = [
            area / size,
            intensity,
            mean_hue,
            mean_sat,
            mean_val
        ]
        X.append(features)

    preds = model.predict(X)
    return preds

def predict(pil_img, step):
    w, h = pil_img.size
    area = [30, 0, w-30, step]
    crops = {}
    while h >= area[3]:
        crops[str(area[1])+', '+str(area[3])] = pil_img.crop(area)
        area[1] += step
        area[3] += step
    preds = get_preds(crops.values())
    result = {list(crops.keys())[i]: preds[i] for i in range(len(preds))}

    return result
