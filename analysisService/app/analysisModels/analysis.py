from analysisModels import mock
import carbon_6ch_model
import oil_6ch_model
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

OIL_CHANNEL = 'uv'
RUIN_CHANNEL = 'dl'
ROCK_CHANNEL = 'dl'
CARBON_CHANNEL = 'uv'


def _oil_model_old_version(fragments):
    markup_fragments = []
    for fragment in fragments:
        # markup_fragment = [{
        #     'class': oil_model.predict(fragment['uvImg'], False),
        #     'top': 0,
        #     'bottom': fragment['uvImg'].size[1]
        # }]
        markup_fragment = []
        size_step_fragment = STEP_OIL * fragment[f'{OIL_CHANNEL}_resolution']
        current_height = size_step_fragment
        while current_height < fragment[f'{OIL_CHANNEL}Img'].size[1]:
            windowImg = fragment[f'{OIL_CHANNEL}Img'].crop((0, current_height - size_step_fragment,
                                                fragment[f'{OIL_CHANNEL}Img'].size[0], current_height))
            # markup_fragment.append({
            #     'class': oil_model.predict(windowImg, False),
            #     'top': current_height - size_step_fragment,
            #     'bottom': current_height
            # })
            current_height += size_step_fragment
        if current_height >= fragment[f'{OIL_CHANNEL}Img'].size[1]:
            windowImg = fragment[f'{OIL_CHANNEL}Img'].crop((0, current_height - size_step_fragment,
                                    fragment[f'{OIL_CHANNEL}Img'].size[0], fragment[f'{OIL_CHANNEL}Img'].size[1]))
            # markup_fragment.append({
            #     'class': oil_model.predict(windowImg, False),
            #     'top': current_height - size_step_fragment,
            #     'bottom': fragment[f'{OIL_CHANNEL}Img'].size[1]
            # })
        markup_fragments.append(markup_fragment)
    return markup_fragments


def _oil_model(fragments):
    markup_fragments = []
    for fragment in fragments:
        markup_fragment = []

        size_step_fragment = STEP_OIL
        current_height = size_step_fragment
        fragment_windows = []
        while fragment['top'] + current_height < fragment['bottom']:
            uv_window = fragment[f'uvImg'].crop(
                        (0, (current_height - size_step_fragment) * fragment[f'uv_resolution'],
                         fragment[f'uvImg'].size[0], current_height * fragment[f'uv_resolution']))
            uv_window = uv_window.resize((int(uv_window.size[0] * (100 / uv_window.size[1])), 100))
            dl_window = fragment[f'dlImg'].crop(
                        (0, (current_height - size_step_fragment) * fragment[f'dl_resolution'],
                         fragment[f'dlImg'].size[0], current_height * fragment[f'dl_resolution']))
            dl_window = dl_window.resize((int(dl_window.size[0] * (100 / dl_window.size[1])), 100))
            fragment_windows.append((uv_window, dl_window))
            markup_fragment.append({
                'class': None,
                'top': (current_height - size_step_fragment) * fragment[f'{OIL_CHANNEL}_resolution'],
                'bottom': current_height * fragment[f'{OIL_CHANNEL}_resolution']
            })
            current_height += size_step_fragment
        if current_height * fragment[f'{OIL_CHANNEL}_resolution'] >= fragment[f'{OIL_CHANNEL}Img'].size[1]:
            uv_window = fragment[f'uvImg'].crop(
                        (0, (current_height - size_step_fragment) * fragment[f'uv_resolution'],
                         fragment[f'uvImg'].size[0], fragment[f'uvImg'].size[1]))
            uv_window = uv_window.resize((int(uv_window.size[0] * (100 / uv_window.size[1])), 100))
            dl_window = fragment[f'dlImg'].crop(
                        (0, (current_height - size_step_fragment) * fragment[f'dl_resolution'],
                         fragment[f'dlImg'].size[0], fragment[f'dlImg'].size[1]))
            dl_window = dl_window.resize((int(dl_window.size[0] * (100 / dl_window.size[1])), 100))
            fragment_windows.append((uv_window, dl_window))
            markup_fragment.append({
                'class': None,
                'top': (current_height - size_step_fragment) * fragment[f'{OIL_CHANNEL}_resolution'],
                'bottom': fragment[f'{OIL_CHANNEL}Img'].size[1]
            })

        markup_windows_class = list(map(lambda pred: 'notDefined' if pred == 'no' else pred,
                                   oil_6ch_model.get_preds(fragment_windows)))
        for i, markup_window in enumerate(markup_fragment):
            markup_window['class'] = markup_windows_class[i]

        markup_fragments.append(markup_fragment)
    return markup_fragments


def _carbon_model(fragments):
    markup_fragments = []
    for fragment in fragments:
        markup_fragment = []

        size_step_fragment = STEP_CARBON
        current_height = size_step_fragment
        fragment_windows = []
        while fragment['top'] + current_height < fragment['bottom']:
            uv_window = fragment[f'uvImg'].crop(
                        (0, (current_height - size_step_fragment) * fragment[f'uv_resolution'],
                         fragment[f'uvImg'].size[0], current_height * fragment[f'uv_resolution']))
            uv_window = uv_window.resize((int(uv_window.size[0] * (100 / uv_window.size[1])), 100))
            dl_window = fragment[f'dlImg'].crop(
                        (0, (current_height - size_step_fragment) * fragment[f'dl_resolution'],
                         fragment[f'dlImg'].size[0], current_height * fragment[f'dl_resolution']))
            dl_window = dl_window.resize((int(dl_window.size[0] * (100 / dl_window.size[1])), 100))
            fragment_windows.append((uv_window, dl_window))
            markup_fragment.append({
                'class': None,
                'top': (current_height - size_step_fragment) * fragment[f'{CARBON_CHANNEL}_resolution'],
                'bottom': current_height * fragment[f'{CARBON_CHANNEL}_resolution']
            })
            current_height += size_step_fragment
        if current_height * fragment[f'{CARBON_CHANNEL}_resolution'] >= fragment[f'{CARBON_CHANNEL}Img'].size[1]:
            uv_window = fragment[f'uvImg'].crop(
                        (0, (current_height - size_step_fragment) * fragment[f'uv_resolution'],
                         fragment[f'uvImg'].size[0], fragment[f'uvImg'].size[1]))
            uv_window = uv_window.resize((int(uv_window.size[0] * (100 / uv_window.size[1])), 100))
            dl_window = fragment[f'dlImg'].crop(
                        (0, (current_height - size_step_fragment) * fragment[f'dl_resolution'],
                         fragment[f'dlImg'].size[0], fragment[f'dlImg'].size[1]))
            dl_window = dl_window.resize((int(dl_window.size[0] * (100 / dl_window.size[1])), 100))
            fragment_windows.append((uv_window, dl_window))
            markup_fragment.append({
                'class': None,
                'top': (current_height - size_step_fragment) * fragment[f'{CARBON_CHANNEL}_resolution'],
                'bottom': fragment[f'{CARBON_CHANNEL}Img'].size[1]
            })

        markup_windows_class = list(map(lambda pred: 'notDefined' if pred == 'no' else pred,
                                   carbon_6ch_model.get_preds(fragment_windows)))
        for i, markup_window in enumerate(markup_fragment):
            markup_window['class'] = markup_windows_class[i]

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
        size_step_fragment = STEP_RUIN * fragment[f'{RUIN_CHANNEL}_resolution']
        current_height = size_step_fragment
        while current_height < fragment[f'{RUIN_CHANNEL}Img'].size[1]:
            windowImg = fragment[f'{RUIN_CHANNEL}Img'].crop((0, current_height - size_step_fragment,
                                                fragment[f'{RUIN_CHANNEL}Img'].size[0], current_height))
            markup_fragment.append({
                'class': ruin_model_cpu.predict(windowImg),
                'top': current_height - size_step_fragment,
                'bottom': current_height
            })
            current_height += size_step_fragment
        if current_height >= fragment[f'{RUIN_CHANNEL}Img'].size[1]:
            windowImg = fragment[f'{RUIN_CHANNEL}Img'].crop((0, current_height - size_step_fragment,
                                                fragment[f'{RUIN_CHANNEL}Img'].size[0], fragment[f'{RUIN_CHANNEL}Img'].size[1]))
            markup_fragment.append({
                'class': ruin_model_cpu.predict(windowImg),
                'top': current_height - size_step_fragment,
                'bottom': fragment[f'{RUIN_CHANNEL}Img'].size[1]
            })
        markup_fragments.append(markup_fragment)

    return markup_fragments


def _merge_markups(markup_fragments, fragments, channel):
    general_markup = []
    current_height = 0
    for i, markup_fragment in enumerate(markup_fragments):
        for window in markup_fragment:
            size_step_fragment = (window['bottom'] - window['top']) / fragments[i][f'{channel}_resolution']
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
    markup_fragments_rock = mock.analyse_param(data['fragments'], STEP_ROCK, 'rock', ROCK_CHANNEL)
    markup_fragments_oil = _oil_model(data['fragments'])
    #markup_fragments_oil = mock.analyse_param(data['fragments'], STEP_OIL, 'oil', OIL_CHANNEL)
    markup_fragments_carbon = _carbon_model(data['fragments'])
    #markup_fragments_ruin = _ruin_model(data['fragments'])
    markup_fragments_ruin = mock.analyse_param(data['fragments'], STEP_RUIN, 'ruin', RUIN_CHANNEL)

    markup_rock = _merge_markups(markup_fragments_rock, data['fragments'], ROCK_CHANNEL)
    markup_oil = _merge_markups(markup_fragments_oil, data['fragments'], OIL_CHANNEL)
    markup_carbon = _merge_markups(markup_fragments_carbon, data['fragments'], CARBON_CHANNEL)
    markup_ruin = _merge_markups(markup_fragments_ruin, data['fragments'], RUIN_CHANNEL)

    return {
        'rock': _merge_windows(markup_rock),
        'oil': _merge_windows(markup_oil),
        'carbon': _merge_windows(markup_carbon),
        'ruin': _merge_windows(markup_ruin)
    }
