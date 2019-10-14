from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK
)
from rest_framework.response import Response

from zipfile import ZipFile
from archiveDecoder import decode_archive

from django.conf import settings
from . import models

import os
import shutil
import hashlib

ROOT_STATIC_APP = f'{settings.PROJECT_ROOT}\\static\\core_sample'


def _cs_count_top_bottom(fragments):
    cs_top, cs_bottom = 1e10, 0
    for fragment in fragments:
        cs_top = min(cs_top, float(fragment['top']))
        cs_bottom = max(cs_bottom, float(fragment['bottom']))
    return cs_top, cs_bottom


def _upload_on_server(csName, data, control_sum, user):
    cs_top, cs_bottom = _cs_count_top_bottom(data['fragments'])
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
        dlImg_name = fragment['dlImg'].filename
        fragment['dlImg'].save(f'{src_abs}\\{dlImg_name}')
        uvImg_name = fragment['uvImg'].filename
        fragment['uvImg'].save(f'{src_abs}\\{uvImg_name}')
        fragment_db = models.Fragment(
            cs=core_sample_db,
            dl_src=f'{src_rel}\\{dlImg_name}',
            uv_src=f'{src_rel}\\{uvImg_name}',
            top=fragment['top'],
            bottom=fragment['bottom']
        )
        fragment_db.save()
    return core_sample_db.global_id


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'zip'


@csrf_exempt
@api_view(["POST"])
def upload(request):
    """Decoding archive -> load data -> response(json)"""
    try:
        file = request.FILES['archive']
    except:
        return Response({'message': "File not attached"}, status=HTTP_400_BAD_REQUEST)

    control_sum = hashlib.md5(file.read()).hexdigest()
    try:
        core_sample = models.Core_sample.objects.filter(control_sum=control_sum)[0]
        return Response({'csId': core_sample.global_id, 'message': "This file has been uploaded before"},
                        status=HTTP_200_OK)
    except:
        ...

    if _allowed_file(file.name):
        zip_file = ZipFile(file, 'r')
        result_decode = decode_archive(zip_file)
        if result_decode['Type'] == 'Success':
            csId = _upload_on_server(request.POST['csName'], result_decode['Data'], control_sum, request.user)

            return Response({'csId': csId, 'warnings': result_decode['Warnings']}, status=HTTP_200_OK)
        elif result_decode['Type'] == 'Error':
            return Response({'message': result_decode['Message']}, status=HTTP_400_BAD_REQUEST)
        else:
            raise Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'Error format file (Expected .zip)'}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["DELETE"])
def delete(request, csId):
    try:
        core_sample = models.Core_sample.objects.get(global_id=csId)
    except:
        return Response({'message': 'Bad id! Not found core_sample object on server'},
                        status=HTTP_400_BAD_REQUEST)

    if request.user != core_sample.user:
        return Response({'message': 'The user is not author of this core_sample'},
                        status=HTTP_400_BAD_REQUEST)

    if f'user_{request.user.username}' in os.listdir(ROOT_STATIC_APP):
        if f'cs_{csId}' in os.listdir(f'{ROOT_STATIC_APP}\\user_{request.user.username}'):
            shutil.rmtree(f'{ROOT_STATIC_APP}\\user_{request.user.username}\\cs_{csId}')
            core_sample.delete()
            return Response(status=HTTP_200_OK)
        else:
            return Response({'message': 'Not found core_sample folder in user folder on server'},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message': 'Not found user folder on server'},
                        status=HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["GET"])
def get(request, csId):
    try:
        core_sample = models.Core_sample.objects.get(global_id=csId)
    except:
        return Response({'message': 'Bad id! Not found core_sample object on server'},
                        status=HTTP_400_BAD_REQUEST)

    if request.user != core_sample.user:
        return Response({'message': 'The user is not author of this core_sample'},
                        status=HTTP_400_BAD_REQUEST)

    return Response({
        'csName': core_sample.name,
        'date': core_sample.date,
        'status': core_sample.status
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getAll(request):
    core_sample_all = models.Core_sample.objects.filter(user=request.user)
    data = []
    for core_sample in core_sample_all:
        data.append({
            'csId': core_sample.global_id,
            'csName': core_sample.name,
            'date': core_sample.date,
            'status': core_sample.status
        })
    return Response({'data': data}, status=HTTP_200_OK)
