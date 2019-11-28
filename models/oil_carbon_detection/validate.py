from PIL import Image
from skimage import measure
import numpy as np

def validate_label(img, dl, labeled, predict):
    bbox_dict = {}
    img = Image.fromarray(img)
    dl = Image.fromarray(dl)
    props = measure.regionprops(labeled)
    if props != []:
        crops = []
        w, h = img.size
        for prop in props:
            centr = prop.centroid
            croparea = [0, centr[0]-50 if centr[0] > 50 else 0, 
                        w, centr[0]+50 if centr[0]+50 < h else h]
            crop = img.crop(croparea)
            dl_crop = dl.crop(croparea)
            crops.append((crop, dl_crop))
        preds = predict(crops)
        for i in range(len(props)):
            lbl = props[i].label
            bbox = props[i].bbox
            if preds[i] == 'no':
                labeled = np.array([[0 if c == lbl else c
                                        for c in r] for r in labeled])
            if preds[i] == 'low':
                labeled = np.array([[-1 if c == lbl else c
                                        for c in r] for r in labeled])
                bbox_dict[str(bbox[0])+', '+str(bbox[2])] = 'low'
            if preds[i] == 'high':
                labeled = np.array([[-2 if c == lbl else c
                                        for c in r] for r in labeled])
                bbox_dict[str(bbox[0])+', '+str(bbox[2])] = 'high'
    return labeled, bbox_dict