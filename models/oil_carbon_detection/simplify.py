import numpy as np

def carbon_simplify(img):   
    simplified = np.array([[np.clip((((pxl*3)//80)+1)*60,0,255)  if pxl != 0 else 0 
                            for pxl in row] for row in img])
    return simplified

def oil_simplify(img):
    simplified = np.array([[(pxl//80)*80 for pxl in row] for row in img])
    return simplified