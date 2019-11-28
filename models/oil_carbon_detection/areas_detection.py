from .carbon_detection.carbon_6ch_model import get_preds as carbon_predict
from .oil_detection.oil_6ch_model import get_preds as oil_predict
from .uv_mask import get_masks
from .simplify import carbon_simplify, oil_simplify
from .merge import merge_props
from .validate import validate_label
from skimage.measure import label

def get_areas(dl_img, uv_img):
    
    carbon_mask, oil_mask = get_masks(uv_img)
    carbon_mask = carbon_simplify(carbon_mask)    
    oil_mask = oil_simplify(oil_mask)
    
    carbon_label = label(carbon_mask, neighbors=8)
    oil_label = label(oil_mask, neighbors=8)
    minsize = (len(uv_img[0]) * 100) // 3
    carbon_label = merge_props(carbon_label, minsize)
    oil_label = merge_props(oil_label, minsize)

    carbon_area, carbon_dict = validate_label(uv_img, dl_img, carbon_label, carbon_predict)
    oil_area, oil_dict = validate_label(uv_img, dl_img, oil_label, oil_predict)
    
    return (oil_area, oil_dict), (carbon_area, carbon_dict)