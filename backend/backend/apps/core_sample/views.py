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
import hashlib


def _cs_count_top_bottom(fragments):
    cs_top, cs_bottom = 1e10, 0
    for fragment in fragments:
        cs_top = min(cs_top, float(fragment['top']))
        cs_bottom = max(cs_bottom, float(fragment['bottom']))
    return cs_top, cs_bottom


def _upload_server(csName, data, control_sum, user):
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

    ROOT_STATIC_APP = f'{settings.PROJECT_ROOT}\\static\\core_sample'
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
    if _allowed_file(file.name):
        zip_file = ZipFile(file, 'r')
        result_decode = decode_archive(zip_file)
        if result_decode['Type'] == 'Success':
            csId = _upload_server(request.POST['csName'], result_decode['Data'], control_sum, request.user)

            control_sum_warning = []
            if len(models.Core_sample.objects.filter(control_sum=control_sum)) >= 2:
                control_sum_warning = ['This file has been uploaded before']

            return Response({'csId:': csId, 'warnings': control_sum_warning + result_decode['Warnings']}, status=HTTP_200_OK)
        elif result_decode['Type'] == 'Error':
            return Response({'message:': result_decode['Message']}, status=HTTP_400_BAD_REQUEST)
        else:
            raise Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'Message:': 'Error format file (Expected .zip)'}, status=HTTP_400_BAD_REQUEST)
