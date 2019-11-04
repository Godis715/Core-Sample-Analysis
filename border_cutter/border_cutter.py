import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BEGIN_CUT = 30
STEP = 1


def _get_luminance(img, left__border_area, right__border_area):
    img = img.convert('RGB')
    luminance = 0
    for x in range(left__border_area, right__border_area + 1):
        for y in range(img.size[1]):
            r, g, b = img.getpixel((x, y))
            luminance += (0.299 * r + 0.587 * g + 0.114 * b)
    luminance /= (img.size[0] * img.size[1])
    return luminance


def draw_border(img, left_border, right_border):
    img = img.convert('RGBA')
    draw = ImageDraw.Draw(img)
    draw.line((left_border, 0, left_border, img.size[1] - 1), fill="red")
    draw.line((img.size[0] - right_border, 0, img.size[0] - right_border, img.size[1] - 1), fill="red")
    img.show()


def cut(img):
    left_cut = BEGIN_CUT
    right_cut = BEGIN_CUT
    luminance_left_border_prev = _get_luminance(img, 1, 1)
    luminance_right_border_prev = _get_luminance(img, img.size[0] - 1, img.size[0] - 1)
    luminance_left_dif = 0
    luminance_right_dif = 0
    is_move_left = True
    is_move_right = True
    while left_cut + right_cut < img.size[0] and (is_move_left or is_move_right):

        if is_move_left:
            luminance_left_border_cur = _get_luminance(img, 0, left_cut)
            if luminance_left_border_cur - luminance_left_border_prev > luminance_left_dif:
                luminance_left_dif = luminance_left_border_cur - luminance_left_border_prev
                luminance_left_border_prev = luminance_left_border_cur
                left_cut += STEP
            else:
                is_move_left = False

        if is_move_right:
            luminance_right_border_cur = _get_luminance(img, img.size[0] - right_cut, img.size[0] - 1)
            if luminance_right_border_cur - luminance_right_border_prev > luminance_right_dif:
                luminance_right_dif = luminance_right_border_cur - luminance_right_border_prev
                luminance_right_border_prev = luminance_right_border_cur
                right_cut += STEP
            else:
                is_move_right = False

    draw_border(img, left_cut, right_cut)
    if not left_cut + right_cut >= img.size[0]:
        return img.crop((left_cut + 1, 0, img.size[0] - right_cut, img.size[1]))
    else:
        return img


if __name__ == '__main__':
    image = Image.open(f'{BASE_DIR}/tests/test6.jpeg')
    image = cut(image)
    image.show()
