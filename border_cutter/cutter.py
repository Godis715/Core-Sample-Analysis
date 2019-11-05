from PIL import Image, ImageStat

def cut(image):
    w, h = image.size
    
    i = 5
    max_reas = 0
    pos = 0
    while i <= w/4:
        area = [i, 0, i+1, h]
        leftcrop = image.crop(area)
        area = [i+1, 0, i+2, h]
        rightcrop = image.crop(area)
        lr, lg, lb = ImageStat.Stat(leftcrop).mean
        rr, rg, rb = ImageStat.Stat(rightcrop).mean
        reas = abs(rr-lr + rg-lg + rb-lb)
        if reas > 3:
            max_reas = reas
            pos = i
        i += 1

    i = w-5
    max_reas = 0
    pos2 = w
    while i >= w*3/4:
        area = [i, 0, i+1, h]
        leftcrop = image.crop(area)
        area = [i, 0, i+2, h]
        rightcrop = image.crop(area)
        lr, lg, lb = ImageStat.Stat(leftcrop).mean
        rr, rg, rb = ImageStat.Stat(rightcrop).mean
        reas = abs(rr-lr + rg-lg + rb-lb)
        if reas > 3:
            max_reas = reas
            pos2 = i
        i -= 1

    croparea = [pos, 0, pos2, h]
    image = image.crop(croparea)
    return image
