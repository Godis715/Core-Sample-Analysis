from PIL import Image

import random

STEP_ROCK = 0.4
STEP_OIL = 0.2
STEP_CARBON = 0.1
STEP_DISRUPTION = 0.1

CLASSES = {
    'rock': ['mudstone', 'siltstone', 'sandstone'],
    'oil': ['notDefined', 'low', 'high'],
    'carbon': ['notDefined', 'low', 'high'],
    'disruption': ['none', 'low', 'high']
}


def _analyse_param(fragments, size_step, name_param):
    markup_fragments = []
    for fragment in fragments:
        markup_fragment = []
        size_step_fragment = size_step * fragment['dl_density']
        current_height = size_step_fragment
        while current_height < fragment['dlImg'].size[1]:
            markup_fragment.append({
                'class': CLASSES[name_param][random.randint(0, len(CLASSES[name_param]) - 1)],
                'top': current_height - size_step_fragment,
                'bottom': current_height
            })
            current_height += size_step_fragment
        markup_fragments.append(markup_fragment)

    return markup_fragments


def _merge_markups(markup_fragments, size_step):
    general_markup = []
    current_height = size_step
    for i, markup_fragment in enumerate(markup_fragments):
        for window in markup_fragment:
            general_markup.append({
                'class': window['class'],
                'top': current_height - size_step,
                'bottom': current_height
            })
            current_height += size_step
    return general_markup


def _merge_windows(markup):
    merge_markup = []
    temp_class = None
    temp_top_class = None
    temp_bottom_class = None
    for window in markup:
        if temp_class != window['class']:
            if temp_class is not None:
                merge_markup.append({
                    'class': temp_class,
                    'top': temp_top_class,
                    'bottom': temp_bottom_class
                })
            temp_class = window['class']
            temp_top_class = window['top']
            temp_bottom_class = window['bottom']
        else:
            temp_bottom_class = window['bottom']
    return merge_markup


def analyse(data):
    markup_fragments_rock = _analyse_param(data['fragments'], STEP_ROCK, 'rock')
    markup_fragments_oil = _analyse_param(data['fragments'], STEP_OIL, 'oil')
    markup_fragments_carbon = _analyse_param(data['fragments'], STEP_CARBON, 'carbon')
    markup_fragments_disruption = _analyse_param(data['fragments'], STEP_DISRUPTION, 'disruption')

    markup_rock = _merge_markups(markup_fragments_rock, STEP_ROCK)
    markup_oil = _merge_markups(markup_fragments_oil, STEP_OIL)
    markup_carbon = _merge_markups(markup_fragments_carbon, STEP_CARBON)
    markup_disruption = _merge_markups(markup_fragments_disruption, STEP_DISRUPTION)

    return {
        'rock': _merge_windows(markup_rock),
        'oil': _merge_windows(markup_oil),
        'carbon': _merge_windows(markup_carbon),
        'disruption': _merge_windows(markup_disruption)
    }
