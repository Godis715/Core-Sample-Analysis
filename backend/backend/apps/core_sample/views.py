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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'zip'

@csrf_exempt
@api_view(["POST"])
def upload(request):
    """Decoding archive -> load data -> result(json)"""
    """result:
        {'Type': 'Error', 'Message:': '...'}
        or
        {'Type': 'Success', 'Data:': result_analysis} 
    """

    file = request.FILES['archive']

    if allowed_file(file.name):
        zip_file = ZipFile(file, 'r')
        result_decode = decode_archive(zip_file)
        if result_decode['Type'] == 'Error':
            return Response({'message:': result_decode['Message']}, status=HTTP_400_BAD_REQUEST)
        else:
            ...
            # csId = upload_server(result_decode)
            # if result_decode['Type'] == 'Success':
            #     return Response({'csId:': csId}, status=HTTP_200_OK)
            # if result_decode['Type'] == 'Warnings':
            #     return Response({'csId:': csId, 'warnings': result_decode['Warnings']}, status=HTTP_200_OK)

    return Response({'Message:': 'Error format file (Expected .zip)'}, status=HTTP_400_BAD_REQUEST)

