from analysisModels import mock
import oil_model
import ruin_model_cpu


STEP_ROCK = 20
STEP_OIL = 10
STEP_CARBON = 10
STEP_RUIN = 5

CLASSES = {
    'rock': ['mudstone', 'siltstone', 'sandstone'],
    'oil': ['notDefined', 'low', 'high'],
    'carbon': ['notDefined', 'low', 'high'],
    'ruin': ['none', 'low', 'high']
}


def _oil_model(fragments):
    markup_fragments = []
    for fragment in fragments:
        # markup_fragment = [{
        #     'class': oil_model.predict(fragment['uvImg'], False),
        #     'top': 0,
        #     'bottom': fragment['uvImg'].size[1]
        # }]
        markup_fragment = []
        size_step_fragment = STEP_OIL * fragment['uv_resolution']
        current_height = size_step_fragment
        while current_height < fragment['uvImg'].size[1]:
            windowImg = fragment['uvImg'].crop((0, current_height - size_step_fragment,
                                                fragment['uvImg'].size[0], current_height))
            markup_fragment.append({
                'class': oil_model.predict(windowImg, False),
                'top': current_height - size_step_fragment,
                'bottom': current_height
            })
            current_height += size_step_fragment
        if current_height > fragment['uvImg'].size[1]:
            windowImg = fragment['uvImg'].crop((0, current_height - size_step_fragment,
                                                fragment['uvImg'].size[0], fragment['uvImg'].size[1]))
            markup_fragment.append({
                'class': oil_model.predict(windowImg, False),
                'top': current_height - size_step_fragment,
                'bottom': fragment['uvImg'].size[1]
            })
        markup_fragments.append(markup_fragment)

    return markup_fragments


def _ruin_model(fragments):
    markup_fragments = []
    for fragment in fragments:
        # markup_fragment = [{
        #     'class': oil_model.predict(fragment['uvImg'], False),
        #     'top': 0,
        #     'bottom': fragment['uvImg'].size[1]
        # }]
        markup_fragment = []
        size_step_fragment = STEP_RUIN * fragment['dl_resolution']
        current_height = size_step_fragment
        while current_height < fragment['dlImg'].size[1]:
            windowImg = fragment['dlImg'].crop((0, current_height - size_step_fragment,
                                                fragment['dlImg'].size[0], current_height))
            markup_fragment.append({
                'class': ruin_model_cpu.predict(windowImg),
                'top': current_height - size_step_fragment,
                'bottom': current_height
            })
            current_height += size_step_fragment
        if current_height > fragment['dlImg'].size[1]:
            windowImg = fragment['dlImg'].crop((0, current_height - size_step_fragment,
                                                fragment['dlImg'].size[0], fragment['dlImg'].size[1]))
            markup_fragment.append({
                'class': ruin_model_cpu.predict(windowImg),
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
    markup_fragments_oil = _oil_model(data['fragments'])
    markup_fragments_carbon = mock.analyse_param(data['fragments'], STEP_CARBON, 'carbon')
    markup_fragments_ruin = _ruin_model(data['fragments'])

    markup_rock = _merge_markups(markup_fragments_rock, data['fragments'])
    markup_oil = _merge_markups(markup_fragments_oil, data['fragments'])
    markup_carbon = _merge_markups(markup_fragments_carbon, data['fragments'])
    markup_ruin = _merge_markups(markup_fragments_ruin, data['fragments'])

    return {
        'rock': _merge_windows(markup_rock),
        'oil': _merge_windows(markup_oil),
        'carbon': _merge_windows(markup_carbon),
        'ruin': _merge_windows(markup_ruin)
    }
