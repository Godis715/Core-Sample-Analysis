import random

STEP_ROCK = 40
STEP_OIL = 20
STEP_CARBON = 10
STEP_DISRUPTION = 10

CLASSES = {
    'rock': ['mudstone', 'siltstone', 'sandstone'],
    'oil': ['notDefined', 'low', 'high'],
    'carbon': ['notDefined', 'low', 'high'],
    'ruin': ['none', 'low', 'high']
}


def analyse_param(fragments, size_step, name_param):
    markup_fragments = []
    for fragment in fragments:
        markup_fragment = []
        size_step_fragment = size_step * fragment['dl_resolution']
        current_height = size_step_fragment
        while current_height < fragment['dlImg'].size[1]:
            markup_fragment.append({
                'class': CLASSES[name_param][random.randint(0, len(CLASSES[name_param]) - 1)],
                'top': current_height - size_step_fragment,
                'bottom': current_height
            })
            current_height += size_step_fragment
        if current_height > fragment['dlImg'].size[1]:
            markup_fragment.append({
                'class': CLASSES[name_param][random.randint(0, len(CLASSES[name_param]) - 1)],
                'top': current_height - size_step_fragment,
                'bottom': fragment['dlImg'].size[1]
            })
        markup_fragments.append(markup_fragment)

    return markup_fragments