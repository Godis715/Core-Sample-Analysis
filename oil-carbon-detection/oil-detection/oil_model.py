from joblib import load
from PIL import Image, ImageStat
import numpy as np
import cv2
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load(os.path.join(BASE_DIR, 'oil_rfc.joblib'))


def predict(pil_img, ruin):
    img = np.array(pil_img)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    pil_img = Image.fromarray(img_hsv)
    mean_hue, mean_sat, mean_val = ImageStat.Stat(pil_img).mean
    dark = (0, 0, 85+mean_val/3)
    light = (255, 255, 255)
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    mask_yel = cv2.inRange(img_hsv, dark, light)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_yel = cv2.bitwise_and(img_gray, img_gray, mask=mask_yel)
    size = len(img) * len(img[0])
    area = sum([sum([0 if pxl == 0 else 1 for pxl in row])for row in img_yel])
    feature = [
        area / size,
        sum([sum(row) for row in img_yel]) / (area*mean_val),
        mean_hue,
        mean_sat,
        mean_val,
        ruin
    ]
    pred = 'high' if model.predict([feature])[0] == 1 else 'notDefined'
    return pred
