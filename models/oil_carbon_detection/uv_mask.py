from PIL import Image, ImageStat
import cv2
from scipy import ndimage

def get_masks(img):
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
    img_carbon = ndimage.median_filter(input=img_carbon, size=20, cval=0.0, mode='reflect') 

    dark = (0,0,50+mean_val/3)
    light = (179,255,255)
    mask_yel = cv2.inRange(img_hsv, dark, light)
    img_yel = cv2.bitwise_and(img_gray, img_gray, mask=mask_yel)
    img_yel = ndimage.median_filter(input=img_yel, size=20, cval=0.0, mode='reflect') 

    return img_carbon, img_yel