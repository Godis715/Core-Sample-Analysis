from analysisModels import mock
from oil_model import predict


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

MODELS = {
    'oil': oil_model.predict
}


def _analyse_param(fragments, size_step, name_param):
    markup_fragments = []
    for fragment in fragments:
        markup_fragment = []
        size_step_fragment = size_step * fragment['dl_resolution']
        current_height = size_step_fragment
        while current_height < fragment['dlImg'].size[1]:
            markup_fragment.append({
                'class':'',
                'top': current_height - size_step_fragment,
                'bottom': current_height
            })
            current_height += size_step_fragment
        if current_height > fragment['dlImg'].size[1]:
            markup_fragment.append({
                'class': '',
                'top': current_height - size_step_fragment,
                'bottom': fragment['dlImg'].size[1]
            })
        markup_fragments.append(markup_fragment)

    return markup_fragments


def _merge_markups(markup_fragments, fragments):
    general_markup = []
    current_height = 0
    for i, markup_fragment in enumerate(markup_fragments):
        for window in markup_fragment:
            size_step_fragment = (window['bottom'] - window['top']) / fragments[i]['dl_resolution']
            current_height += size_step_fragment
            general_markup.append({
                'class': window['class'],
                'top': current_height - size_step_fragment,
                'bottom': current_height
            })

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
                    'top': round(temp_top_class),
                    'bottom': round(temp_bottom_class)
                })
            temp_class = window['class']
            temp_top_class = window['top']
            temp_bottom_class = window['bottom']
        else:
            temp_bottom_class = window['bottom']
    if temp_class is not None:
        merge_markup.append({
            'class': temp_class,
            'top': round(temp_top_class),
            'bottom': round(temp_bottom_class)
        })
    return merge_markup


def analyse(data):
    markup_fragments_rock = mock.analyse_param(data['fragments'], STEP_ROCK, 'rock')
    markup_fragments_oil = _analyse_param(data['fragments'], STEP_OIL, 'oil')
    markup_fragments_carbon = mock.analyse_param(data['fragments'], STEP_CARBON, 'carbon')
    markup_fragments_disruption = _analyse_param(data['fragments'], STEP_DISRUPTION, 'ruin')

    markup_rock = _merge_markups(markup_fragments_rock, data['fragments'])
    markup_oil = _merge_markups(markup_fragments_oil, data['fragments'])
    markup_carbon = _merge_markups(markup_fragments_carbon, data['fragments'])
    markup_disruption = _merge_markups(markup_fragments_disruption, data['fragments'])

    return {
        'rock': _merge_windows(markup_rock),
        'oil': _merge_windows(markup_oil),
        'carbon': _merge_windows(markup_carbon),
        'ruin': _merge_windows(markup_disruption)
    }
