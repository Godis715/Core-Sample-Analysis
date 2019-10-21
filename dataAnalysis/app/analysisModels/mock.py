from PIL import Image

import random

STEP_ROCK = 20
STEP_OIL = 30
STEP_CARBON = 10
STEP_DISRUPTION = 40

CLASSES = {
    'rock': ['clay', 'siltstone', 'sandstone'],
    'oil': ['not_define', 'low', 'high'],
    'carbon': ['not_define', 'low', 'high'],
    'disruption': ['none', 'low', 'high']
}


def _merge_fragments(fragments):
    general_width = 0
    for fragment in fragments:
        general_width = max(general_width, fragment['dlImg'].size[0])
        general_width = max(general_width, fragment['uvImg'].size[0])

    general_height_dl = 0
    general_height_uv = 0
    for fragment in fragments:
        general_height_dl += fragment['dlImg'].size[1] * (general_width / fragment['dlImg'].size[0])
        general_height_uv += fragment['uvImg'].size[1] * (general_width / fragment['uvImg'].size[0])

    return general_width, max(general_height_dl, general_height_uv)


def _analyse_param(height, size_step, name_param):
    markup = []
    current_height = size_step
    while current_height < height:
        markup.append({
            'class': CLASSES[name_param][random.randint(0, len(CLASSES[name_param]) - 1)],
            'begin': current_height - size_step,
            'end': current_height
        })
        current_height += size_step
    return markup


def _merge_markup(markup):
    merge_markup = []
    temp_class = None
    temp_begin_class = None
    temp_end_class = None
    for window in markup:
        if temp_class != window['class']:
            if temp_class is not None:
                merge_markup.append({
                    'class': temp_class,
                    'begin': temp_begin_class,
                    'end': temp_end_class
                })
            temp_class = window['class']
            temp_begin_class = window['begin']
            temp_end_class = window['end']
        else:
            temp_end_class = window['end']
    return merge_markup


def analyse(data):
    _, general_height = _merge_fragments(data['fragments'])
    markup_rock = _analyse_param(general_height, STEP_ROCK, 'rock')
    markup_oil = _analyse_param(general_height, STEP_ROCK, 'oil')
    markup_carbon = _analyse_param(general_height, STEP_ROCK, 'carbon')
    markup_disruption = _analyse_param(general_height, STEP_ROCK, 'disruption')

    return {
        'rock': _merge_markup(markup_rock),
        'oil': _merge_markup(markup_oil),
        'carbon': _merge_markup(markup_carbon),
        'disruption': _merge_markup(markup_disruption)
    }
