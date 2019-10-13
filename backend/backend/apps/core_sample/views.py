from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.status import (
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


def _cs_count_top_bottom(fragments):
    cs_top, cs_bottom = 1e10, 0
    for fragment in fragments:
        cs_top = min(cs_top, float(fragment['top']))
        cs_bottom = max(cs_bottom, float(fragment['bottom']))
    return cs_top, cs_bottom


def _upload_server(csName, data, user):
    cs_top, cs_bottom = _cs_count_top_bottom(data['fragments'])
    core_sample_db = models.Core_sample(
        name=csName,
        user=user,
        deposit=data['deposit'],
        hole=data['hole'],
        top=cs_top,
        bottom=cs_bottom
    )
    core_sample_db.save()

    ROOT_STATIC_APP = f'{settings.PROJECT_ROOT}\\static\\core_sample'
    src_rel = f'user_{user.id}\\cs_{core_sample_db.global_id}'
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

    file = request.FILES['archive']
    csName = request.POST['csName']

    if _allowed_file(file.name):
        zip_file = ZipFile(file, 'r')
        result_decode = decode_archive(zip_file)
        if result_decode['Type'] == 'Success':
            csId = _upload_server(csName, result_decode['Data'], request.user)
            return Response({'csId:': csId, 'warnings': result_decode['Warnings']}, status=HTTP_200_OK)
        elif result_decode['Type'] == 'Error':
            return Response({'message:': result_decode['Message']}, status=HTTP_400_BAD_REQUEST)
        else:
            raise Exception('Not correct result of decode')

    return Response({'Message:': 'Error format file (Expected .zip)'}, status=HTTP_400_BAD_REQUEST)

