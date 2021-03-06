"""   Import   """
# Django packages
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
# Rest_framework packages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_409_CONFLICT,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)

from rest_framework.response import Response

from zipfile import ZipFile
from archiveDecoder import archiveDecode

from django.conf import settings
from . import models
# Third party packages
from zipfile import ZipFile
import os
import shutil
import hashlib
import threading
import requests
import json

# Path of fo;der with the static files
ROOT_STATIC_APP = f'{settings.PROJECT_ROOT}\\static\\core_sample'

# Response's messages
ERROR_IS_NOT_ATTACHED = "{} is not attached!"
ERROR_FORMAT_FILE = "File format error (Expected .zip)!"
ERROR_INVALID_ID = "Invalid id: {} not found!"
ERROR_NOT_AUTHOR = "The user is not author of this {}!"
ERROR_NOT_FOUND_FOLDER = "Not found {} folder!"
ERROR_NOT_ANALYSED = "This core sample hasn't be!"

ERROR_STRUCT_NOT_INCLUDED = "'{}' is not included in '{}'!"
ERROR_VALUES_ORDER = "Values of {} and {} have the wrong order!"
ERROR_VALUES_SUM = "Sum of {} is not correct!"
ERROR_VALUE = "{} have the wrong value!"

CONFLICT_FILE_UPLOADED_BEFORE = "This file has been uploaded before"
CONFLICT_CORE_SAMPLE_ANALYSED_BEFORE = "This core sample has been analysed before"
CONFLICT_CORE_SAMPLE_IN_PROCESS_ANALYSE = "This core sample is analysing now"

OK_ANALYSIS_RUN = "The analysis is run"


def _cs_count_top_bottom(fragments):
    """Counting: top and bottom of the entire core sample"""
    cs_top, cs_bottom = 1e10, 0
    for fragment in fragments:
        cs_top = min(cs_top, float(fragment['top']))
        cs_bottom = max(cs_bottom, float(fragment['bottom']))
    return cs_top, cs_bottom


def _upload_on_server(csName, data, control_sum, user):

    cs_top, cs_bottom = _cs_count_top_bottom(data['fragments'])

    # Loading: the core_sample in database
    core_sample_db = models.Core_sample(
        name=csName,
        user=user,
        control_sum=control_sum,
        deposit=data['deposit'],
        hole=data['hole'],
        top=cs_top,
        bottom=cs_bottom
    )
    core_sample_db.save()

    src_rel = f'user_{user.username}\\cs_{core_sample_db.global_id}'
    src_abs = f'{ROOT_STATIC_APP}\\{src_rel}'
    os.makedirs(src_abs)
    for fragment in data['fragments']:
        # Loading: the fragment of core_sample in the local storage
        dlImg_name = fragment['dlImg'].filename
        fragment['dlImg'].save(f'{src_abs}\\{dlImg_name}')
        uvImg_name = fragment['uvImg'].filename
        fragment['uvImg'].save(f'{src_abs}\\{uvImg_name}')
        # Loading: the fragment of core_sample in database
        fragment_db = models.Fragment(
            cs=core_sample_db,
            dl_src=f'{src_rel}\\{dlImg_name}',
            uv_src=f'{src_rel}\\{uvImg_name}',
            dl_resolution=fragment['dlImg'].size[1] / (fragment['bottom'] - fragment['top']),
            uv_resolution=fragment['uvImg'].size[1] / (fragment['bottom'] - fragment['top']),
            top=fragment['top'],
            bottom=fragment['bottom'],
            dl_height=fragment['dlImg'].size[1],
            dl_width=fragment['dlImg'].size[0],
            uv_height=fragment['uvImg'].size[1],
            uv_width=fragment['uvImg'].size[0],
        )
        fragment_db.save()

    return core_sample_db.global_id


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'zip'


@csrf_exempt
@api_view(["POST"])
def cs_upload(request):
    """Steps: 1) Decoding archive -> 2) load data -> 3) response(json)"""

    # Checking: [exist] - [data of request]
    try:
        file = request.FILES['archive']
    except:
        return Response({'message': ERROR_IS_NOT_ATTACHED.format('File')}, status=HTTP_400_BAD_REQUEST)

    # Checking: [exist] - [the same core sample]
    control_sum = hashlib.md5(file.read()).hexdigest()
    try:
        core_sample = models.Core_sample.objects.filter(control_sum=control_sum)[0]
        return Response({'csId': core_sample.global_id, 'message': CONFLICT_FILE_UPLOADED_BEFORE},
                        status=HTTP_409_CONFLICT)
    except:
        ...

    # Checking: [correct] - [format of the load archive]
    if _allowed_file(file.name):
        zip_file = ZipFile(file, 'r')
        # Step: 1)
        result_decode = archiveDecode(zip_file)
        # Checking: [correct] - [decoding of the load archive]
        if result_decode['Type'] == 'Success':
            # Step: 2)
            csId = _upload_on_server(request.POST['csName'], result_decode['Data'], control_sum, request.user)
            # Step: 3)
            return Response({'csId': csId, 'warnings': result_decode['Warnings']}, status=HTTP_200_OK)
        elif result_decode['Type'] == 'Error':
            return Response({'message': result_decode['Message']}, status=HTTP_400_BAD_REQUEST)
        else:
            raise Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message': ERROR_FORMAT_FILE}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["DELETE"])
def cs_delete(request, csId):
    # Checking: [exist] - [the core sample]
    try:
        core_sample = models.Core_sample.objects.get(global_id=csId)
    except:
        return Response({'message': ERROR_INVALID_ID.format('core sample')},
                        status=HTTP_404_NOT_FOUND)

    # Checking: [access] - [request's user == author of core sample]
    if request.user != core_sample.user:
        return Response({'message': ERROR_NOT_AUTHOR.format('core sample')},
                        status=HTTP_403_FORBIDDEN)

    # Checking (server error): [exist] - [folders and files in the local storage]
    if f'user_{request.user.username}' in os.listdir(ROOT_STATIC_APP):
        if f'cs_{csId}' in os.listdir(f'{ROOT_STATIC_APP}\\user_{request.user.username}'):
            # Deleting: in the local storage
            shutil.rmtree(f'{ROOT_STATIC_APP}\\user_{request.user.username}\\cs_{csId}')
            # Deleting: in database
            core_sample.delete()
            return Response(status=HTTP_200_OK)
        else:
            return Response({'message': ERROR_NOT_FOUND_FOLDER.format('core sample')},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message': ERROR_NOT_FOUND_FOLDER.format('user')},
                        status=HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["GET"])
def cs_get(request, csId):
    # Checking: [exist] - [the core sample]
    try:
        core_sample = models.Core_sample.objects.get(global_id=csId)
    except:
        return Response({'message': ERROR_INVALID_ID.format('core sample')},
                        status=HTTP_404_NOT_FOUND)

    # Checking: [access] - [request's user == author of core sample]
    if request.user != core_sample.user:
        return Response({'message': ERROR_NOT_AUTHOR.format('core sample')},
                        status=HTTP_403_FORBIDDEN)

    return Response({
        'csName': core_sample.name,
        'date': core_sample.date,
        'status': models.Core_sample.STATUS_TYPES_NAME[core_sample.status]
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def cs_getAll(request):
    core_sample_all = models.Core_sample.objects.filter(user=request.user)
    data = []
    for core_sample in core_sample_all:
        data.append({
            'csId': core_sample.global_id,
            'csName': core_sample.name,
            'date': core_sample.date,
            'status': models.Core_sample.STATUS_TYPES_NAME[core_sample.status]
        })
    return Response(data, status=HTTP_200_OK)


def _load_markup_on_server(markup_db, markup_data):
    for oil_layer in markup_data['oil']:
        oil_layer_db = models.Oil_layer(
            markup=markup_db,
            top=int(oil_layer['top']),
            bottom=int(oil_layer['bottom']),
            class_label=models.Oil_layer.CLASS_LABELS_NUMBER[oil_layer['class']]
        )
        oil_layer_db.save()

    for carbon_layer in markup_data['carbon']:
        carbon_layer_db = models.Carbon_layer(
            markup=markup_db,
            top=int(carbon_layer['top']),
            bottom=int(carbon_layer['bottom']),
            class_label=models.Carbon_layer.CLASS_LABELS_NUMBER[carbon_layer['class']]
        )
        carbon_layer_db.save()

    for rock_layer in markup_data['rock']:
        rock_layer_db = models.Rock_layer(
            markup=markup_db,
            top=int(rock_layer['top']),
            bottom=int(rock_layer['bottom']),
            class_label=models.Rock_layer.CLASS_LABELS_NUMBER[rock_layer['class']]
        )
        rock_layer_db.save()

    for disruption_layer in markup_data['ruin']:
        disruption_layer_db = models.Ruin_layer(
            markup=markup_db,
            top=int(disruption_layer['top']),
            bottom=int(disruption_layer['bottom']),
            class_label=models.Ruin_layer.CLASS_LABELS_NUMBER[disruption_layer['class']]
        )
        disruption_layer_db.save()


def _analyse(core_sample, user):
    # Preparing: data for request on analyse
    files = {}
    data = {
        'deposit': core_sample.deposit,
        'hole': core_sample.hole,
        'fragments': []
    }

    fragments = models.Fragment.objects.filter(cs_id=core_sample)
    for fragment in fragments:
        dlImg = open(f'{ROOT_STATIC_APP}\\{fragment.dl_src}', 'rb')
        uvImg = open(f'{ROOT_STATIC_APP}\\{fragment.uv_src}', 'rb')
        data['fragments'].append({
            'top': fragment.top,
            'bottom': fragment.bottom,
            'dl_resolution': fragment.dl_resolution,
            'uv_resolution': fragment.uv_resolution,
            'dlImg': os.path.basename(dlImg.name),
            'uvImg': os.path.basename(uvImg.name),
        })
        files[os.path.basename(dlImg.name)] = dlImg
        files[os.path.basename(uvImg.name)] = uvImg

    # Request on the server for analyse
    url = 'http://127.0.0.1:5050/api/analyse/'
    try:
        response_markup = requests.post(url, data={'data': json.dumps(data)}, files=files)
    except:
        # Error
        core_sample.status = models.Core_sample.ERROR
        core_sample.save()
    else:
        # Success
        markup_data = json.loads(response_markup.text)['markup']

        markup_db = models.Markup(
            cs=core_sample,
            user=user
        )
        markup_db.save()

        # Loading: markup in database
        _load_markup_on_server(markup_db, markup_data)

        core_sample.status = models.Core_sample.ANALYSED
        core_sample.save()


@csrf_exempt
@api_view(["PUT"])
def cs_analyse(request, csId):
    # Checking: [exist] - [the core sample]
    try:
        core_sample = models.Core_sample.objects.get(global_id=csId)
    except:
        return Response({'message': ERROR_INVALID_ID.format('core sample')},
                        status=HTTP_404_NOT_FOUND)
    # Checking: [correct] - [status of analysing]
    if core_sample.status == models.Core_sample.ANALYSED:
        return Response({'message': CONFLICT_CORE_SAMPLE_ANALYSED_BEFORE},
                        status=HTTP_409_CONFLICT)
    if core_sample.status == models.Core_sample.IN_PROCESS:
        return Response({'message': CONFLICT_CORE_SAMPLE_IN_PROCESS_ANALYSE},
                        status=HTTP_409_CONFLICT)

    core_sample.status = models.Core_sample.IN_PROCESS
    core_sample.save()

    thread = threading.Thread(target=_analyse, args=(core_sample, request.user, ))
    thread.start()

    return Response({'message': OK_ANALYSIS_RUN}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["PUT"])
def css_status(request):
    # Checking: [exist] - [data of request]
    try:
        csIds = json.loads(QueryDict(request.body).get('csIds'))
    except:
        return Response({'message': ERROR_IS_NOT_ATTACHED.format('csIds')}, status=HTTP_400_BAD_REQUEST)

    statuses = {}
    for csId in csIds:
        # Checking: [exist] - [the core sample]
        try:
            core_sample = models.Core_sample.objects.get(global_id=csId)
        except:
            return Response({'message': ERROR_INVALID_ID.format('core sample')},
                            status=HTTP_404_NOT_FOUND)
        # Checking: [access] - [request's user == author of core sample]
        if request.user != core_sample.user:
            return Response({'message': ERROR_NOT_AUTHOR.format('core sample')},
                            status=HTTP_403_FORBIDDEN)
        statuses[csId] = models.Core_sample.STATUS_TYPES_NAME[core_sample.status]

    return Response({'statuses': statuses}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def cs_markup_get(request, csId):
    # Checking: [exist] - [the core sample]
    try:
        core_sample = models.Core_sample.objects.get(global_id=csId)
    except:
        return Response({'message': ERROR_INVALID_ID.format('core sample')},
                        status=HTTP_404_NOT_FOUND)

    # Checking: [correct] - [status of analysing]
    if core_sample.status != core_sample.ANALYSED:
        return Response({'message': ERROR_NOT_ANALYSED},
                        status=HTTP_400_BAD_REQUEST)

    data = {
        'dlImages': [],
        'uvImages': [],
        'markup': {
            'rock': [],
            'oil': [],
            'carbon': [],
            'ruin': []
        }
    }
    fragments = models.Fragment.objects.filter(cs=core_sample)
    for fragment in fragments:
        data['uvImages'].append({
            'src': fragment.uv_src,
            'height': fragment.uv_height,
            'width': fragment.uv_width,
            'top': fragment.top,
            'bottom': fragment.bottom
        })
        data['dlImages'].append({
            'src': fragment.dl_src,
            'height': fragment.dl_height,
            'width': fragment.dl_width,
            'top': fragment.top,
            'bottom': fragment.bottom
        })
    markup = models.Markup.objects.filter(cs=core_sample).last()
    oil_layers = models.Oil_layer.objects.filter(markup=markup)
    for oil_layer in oil_layers:
        data['markup']['oil'].append({
            'class': models.Oil_layer.CLASS_LABELS_NAME[oil_layer.class_label],
            'top': oil_layer.top,
            'bottom': oil_layer.bottom
        })
    rock_layers = models.Rock_layer.objects.filter(markup=markup)
    for rock_layer in rock_layers:
        data['markup']['rock'].append({
            'class': models.Rock_layer.CLASS_LABELS_NAME[rock_layer.class_label],
            'top': rock_layer.top,
            'bottom': rock_layer.bottom
        })
    carbon_layers = models.Carbon_layer.objects.filter(markup=markup)
    for carbon_layer in carbon_layers:
        data['markup']['carbon'].append({
            'class': models.Carbon_layer.CLASS_LABELS_NAME[carbon_layer.class_label],
            'top': carbon_layer.top,
            'bottom': carbon_layer.bottom
        })
    disruption_layers = models.Ruin_layer.objects.filter(markup=markup)
    for disruption_layer in disruption_layers:
        data['markup']['ruin'].append({
            'class': models.Ruin_layer.CLASS_LABELS_NAME[disruption_layer.class_label],
            'top': disruption_layer.top,
            'bottom': disruption_layer.bottom
        })

    return Response(data, status=HTTP_200_OK)


def _validate_markup(markup_data, core_sample):
    """ Validation:
    - Existing types of markup: 'oil', 'carbon', 'rock', 'ruin'
    - Existing parameters of window: 'top', 'bottom', 'class'
    - Correct values of parameters:
        - Types of class
        - Order of windows
        - Sum of windows length
    """
    oil_general_height = 0
    if 'oil' in markup_data:
        for oil_layer in markup_data['oil']:
            if 'top' not in oil_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('top', 'oil_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if 'bottom' not in oil_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('bottom', 'oil_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if 'class' not in oil_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('class', 'oil_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if oil_layer['bottom'] > oil_layer['top']:
                oil_general_height += oil_layer['bottom'] - oil_layer['top']
            else:
                return False, Response({'message': ERROR_VALUES_ORDER.format('top', 'bottom')},
                                       status=HTTP_400_BAD_REQUEST)
            if oil_layer['class'] not in models.Oil_layer.CLASS_LABELS_NUMBER:
                return False, Response({'message': ERROR_VALUE.format('class')},
                                       status=HTTP_400_BAD_REQUEST)
    else:
        return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('oil', 'markup')},
                               status=HTTP_400_BAD_REQUEST)
    if oil_general_height != core_sample.bottom - core_sample.top:
        return False, Response({'message': ERROR_VALUES_SUM.format('height layers of oil')},
                               status=HTTP_400_BAD_REQUEST)

    carbon_general_height = 0
    if 'carbon' in markup_data:
        for carbon_layer in markup_data['carbon']:
            if 'top' not in carbon_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('top', 'carbon_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if 'bottom' not in carbon_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('bottom', 'carbon_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if 'class' not in carbon_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('class', 'carbon_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if carbon_layer['bottom'] > carbon_layer['top']:
                carbon_general_height += carbon_layer['bottom'] - carbon_layer['top']
            else:
                return False, Response({'message': ERROR_VALUES_ORDER.format('top', 'bottom')},
                                       status=HTTP_400_BAD_REQUEST)
            if carbon_layer['class'] not in models.Carbon_layer.CLASS_LABELS_NUMBER:
                return False, Response({'message': ERROR_VALUE.format('class')},
                                       status=HTTP_400_BAD_REQUEST)
    else:
        return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('carbon', 'markup')},
                               status=HTTP_400_BAD_REQUEST)
    if carbon_general_height != core_sample.bottom - core_sample.top:
        return False, Response({'message': ERROR_VALUES_SUM.format('height layers of carbon')},
                               status=HTTP_400_BAD_REQUEST)

    rock_general_height = 0
    if 'rock' in markup_data:
        for rock_layer in markup_data['rock']:
            if 'top' not in rock_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('top', 'rock_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if 'bottom' not in rock_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('bottom', 'rock_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if 'class' not in rock_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('class', 'rock_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if rock_layer['bottom'] > rock_layer['top']:
                rock_general_height += rock_layer['bottom'] - rock_layer['top']
            else:
                return False, Response({'message': ERROR_VALUES_ORDER.format('top', 'bottom')},
                                       status=HTTP_400_BAD_REQUEST)
            if rock_layer['class'] not in models.Rock_layer.CLASS_LABELS_NUMBER:
                return False, Response({'message': ERROR_VALUE.format('class')},
                                       status=HTTP_400_BAD_REQUEST)
    else:
        return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('rock', 'markup')},
                               status=HTTP_400_BAD_REQUEST)
    if rock_general_height != core_sample.bottom - core_sample.top:
        return False, Response({'message': ERROR_VALUES_SUM.format('height layers of rock')},
                               status=HTTP_400_BAD_REQUEST)

    disruption_general_height = 0
    if 'ruin' in markup_data:
        for disruption_layer in markup_data['ruin']:
            if 'top' not in disruption_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('top', 'disruption_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if 'bottom' not in disruption_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('bottom', 'disruption_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if 'class' not in disruption_layer:
                return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('class', 'disruption_layer')},
                                       status=HTTP_400_BAD_REQUEST)
            if disruption_layer['bottom'] > disruption_layer['top']:
                disruption_general_height += disruption_layer['bottom'] - disruption_layer['top']
            else:
                return False, Response({'message': ERROR_VALUES_ORDER.format('top', 'bottom')},
                                       status=HTTP_400_BAD_REQUEST)
            if disruption_layer['class'] not in models.Ruin_layer.CLASS_LABELS_NUMBER:
                return False, Response({'message': ERROR_VALUE.format('class')},
                                       status=HTTP_400_BAD_REQUEST)
    else:
        return False, Response({'message': ERROR_STRUCT_NOT_INCLUDED.format('ruin', 'markup')},
                               status=HTTP_400_BAD_REQUEST)

    if disruption_general_height != core_sample.bottom - core_sample.top:
        return False, Response({'message': ERROR_VALUES_SUM.format('height layers of ruin')},
                               status=HTTP_400_BAD_REQUEST)

    return True, None


@csrf_exempt
@api_view(["PUT"])
def cs_markup_put(request, csId):
    # Checking: [exist] - [the core sample]
    try:
        core_sample = models.Core_sample.objects.get(global_id=csId)
    except:
        return Response({'message': ERROR_INVALID_ID.format('core sample')},
                        status=HTTP_404_NOT_FOUND)

    # Checking: [correct] - [status of analysing]
    if core_sample.status != core_sample.ANALYSED:
        return Response({'message': ERROR_NOT_ANALYSED},
                        status=HTTP_400_BAD_REQUEST)

    # Checking: [exist] - [data of request]
    try:
        new_markup_data = json.loads(QueryDict(request.body).get('markup'))
    except:
        return Response({'message': ERROR_IS_NOT_ATTACHED.format('Markup')}, status=HTTP_400_BAD_REQUEST)

    # Checking: [correct] - [data of request]
    isCorrect, response = _validate_markup(new_markup_data, core_sample)
    if isCorrect:
        new_markup_db = models.Markup(
            cs=core_sample,
            user=request.user
        )
        new_markup_db.save()

        # Loading: markup in database
        _load_markup_on_server(new_markup_db, new_markup_data)
        return Response(status=HTTP_200_OK)
    else:
        return response




