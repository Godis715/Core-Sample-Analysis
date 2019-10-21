import json
import os

from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Core_sample


# initialize the APIClient app
client = Client()
client.login(username='dima12101', password='Lbvf12101')


class UploadCoreSampleTest(TestCase):
    """ Test module for Upload core sample API """
    def setUp(self):
        self.valid_zipFile = open(os.path.join(os.path.dirname(__file__), 'files/sample.zip'), 'rb')

    def test_upload_valid_zipFile(self):
        response = client.post(
            reverse('upload'),
            files={"archive": self.valid_zipFile},
            data={'csName': 'Тест'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

