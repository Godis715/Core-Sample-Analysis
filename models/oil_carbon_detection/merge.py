import numpy as np
from skimage import measure

def merge_props(labeled, minsize):
    def dist(a, b):
        dist = ((b[0]-a[0])**2 + (b[1]-a[1])**2)**(0.5)
        return dist
    changed = [0]
    while changed != []:
        changed = []
        props = measure.regionprops(labeled)
        for prop1 in props:
            lbl1 = prop1.label
            if lbl1 not in changed:
                if prop1.area < minsize:
                    merged = False
                    centr1 = prop1.centroid
                    for prop2 in props:
                        centr2 = prop2.centroid
                        lbl2 = prop2.label
                        if lbl1 != lbl2 and lbl2 not in changed and dist(centr1, centr2) < 100:
                            merged = True
                            labeled = np.where(labeled == lbl1, lbl2, labeled)
                            break
                    if merged == False:
                        labeled = np.where(labeled == lbl1, 0, labeled)
                    changed.append(lbl1)
    
    return labeled