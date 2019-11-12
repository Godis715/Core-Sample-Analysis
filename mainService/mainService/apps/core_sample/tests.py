from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from PIL import Image
from zipfile import ZipFile

import os
import shutil
import random
import json


client = APIClient()


def LOGIN(user):
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


def LOGOUT():
    client.credentials(HTTP_AUTHORIZATION='')


class Account_APITestCase(APITestCase):
    def setUp(self):
        self.username = "username_test"
        self.email = "TestUser@test.com"
        self.password = "password_test"

        self.user = User.objects.create_user(
            self.username, self.email, self.password
        )

        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_login__success(self):
        """Test api/login with correct credentials"""
        response = client.post(reverse('login'), data={
                "username": self.username,
                "password": self.password})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'token': self.token.key}, response.data)

    def test_login__error__not_correct_credentials(self):
        """Test api/login with not correct credentials"""
        response = client.post(reverse('login'), data={
                "username": 'username_not_valid',
                "password": 'password_not_valid'})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_login__error__without_credentials(self):
        """Test api/login without credentials"""
        response = client.post(reverse('login'))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_logout__success(self):
        """Test api/logout with token"""
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.post(reverse('logout'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        token_new, _ = Token.objects.get_or_create(user=self.user)
        self.assertNotEqual(token_new.key, self.token.key)

    def test_logout__error__without_token(self):
        """Test api/logout without token"""
        response = client.post(reverse('logout'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class Archive_Generator:
    def __init__(self, load_path):
        self.path_root = load_path
        self.path_images = f'{self.path_root}/images'

    def _generate_images(self, count):
        os.makedirs(self.path_images)
        path_images = []
        for i in range(count):
            size = (random.randint(100, 400), random.randint(100, 2000))
            name_imageDl = f'imgDl_{i}.jpg'
            name_imageUv = f'imgUv_{i}.jpg'
            Image.new("RGB", size, "green").save(f'{self.path_images}/{name_imageDl}')
            Image.new("RGB", size, "red").save(f'{self.path_images}/{name_imageUv}')
            path_images.append(name_imageDl)
            path_images.append(name_imageUv)
        return path_images

    def _delete_images(self):
        shutil.rmtree(self.path_images)

    def _generate_base(self):
        name_images = self._generate_images(count=4)
        data_description = {
            'deposit': random.randint(1, 10),
            'hole': random.randint(1, 10),
            'fragments': []
        }
        with ZipFile(f'{self.path_root}/archive_correct.zip', 'w') as archive_correct:
            current_height = 0
            for i in range(0, len(name_images), 2):
                name_imageDl = name_images[i]
                name_imageUv = name_images[i + 1]
                archive_correct.write(f'{self.path_images}/{name_imageDl}', f"sample/{name_imageDl}")
                archive_correct.write(f'{self.path_images}/{name_imageUv}', f"sample/{name_imageUv}")
                height_fragment = random.randint(1, 100)
                data_description['fragments'].append({
                    'dlImg': name_imageDl,
                    'uvImg': name_imageUv,
                    'top': current_height,
                    'bottom': current_height + height_fragment
                })
                current_height += height_fragment
            with open(f'{self.path_root}/description.json', 'w') as description_file:
                json.dump(data_description, description_file, indent=4)
            archive_correct.write(f'{self.path_root}/description.json', 'sample/description.json')
            os.remove(f'{self.path_root}/description.json')
        self._delete_images()
        return f'{self.path_root}/archive_correct.zip'

    def correct(self):
        return self._generate_base()


def CREATE_CORE_SAMPLE():
    archive_generator = Archive_Generator(f'{settings.PROJECT_ROOT}/static/tests')
    path_archive = archive_generator.correct()
    with open(path_archive, 'rb') as obj_archive:
        response = client.post(reverse('core_sample:cs_upload'), data={'archive': obj_archive,
                                                                       'csName': 'test_delete'})
    os.remove(path_archive)
    return response.data['csId']


def DELETE_CORE_SAMPLE(csId):
    client.delete(f'api/core_sample/{csId}/delete')


class Delete_APITestCase(APITestCase):

    def setUp(self):
        self.main_user = User.objects.create_user(
            username="username_test", email="TestUser@test.com", password="password_test")
        self.url = '/api/core_sample/{}/delete'
        self.csId_not_exist = 'b664248e-09a2-4e2e-8934-dade9cf31946'

    def test_success(self):
        """Test DELETE api/core_sample/<uuid:csId>/delete with correct csId"""
        LOGIN(self.main_user)
        csId = CREATE_CORE_SAMPLE()
        response = client.delete(self.url.format(csId))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_error__not_authorization(self):
        """Test DELETE api/core_sample/<uuid:csId>/delete without token"""
        response = client.delete(self.url.format(self.csId_not_exist))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_error__not_valid_csId(self):
        """Test DELETE api/core_sample/<uuid:csId>/delete with not valid csId"""
        LOGIN(self.main_user)
        response = client.delete(self.url.format(self.csId_not_exist))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_error__not_author(self):
        """Test DELETE api/core_sample/<uuid:csId>/delete when user is not author"""
        LOGIN(self.main_user)
        csId = CREATE_CORE_SAMPLE()

        user_temp = User.objects.create_user(
            "username_test_temp", "TestUser_temp@test.com", "password_test_temp"
        )
        LOGIN(user_temp)
        response = client.delete(self.url.format(csId))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        LOGIN(self.main_user)
        DELETE_CORE_SAMPLE(csId)


class Upload_APITestCase(APITestCase):

    def setUp(self):
        self.main_user = User.objects.create_user(
            username="username_test", email="TestUser@test.com", password="password_test")
        self.url = reverse('core_sample:cs_upload')
        self.archive_generator = Archive_Generator(f'{settings.PROJECT_ROOT}/static/tests')

    def test__not_valid(self):
        self.assertTrue(False)

    def test_success(self):
        """Test POST api/core_sample/upload with correct archive"""
        LOGIN(self.main_user)
        path_archive = self.archive_generator.correct()
        with open(path_archive, 'rb') as obj_archive:
            response = client.post(self.url, data={'archive': obj_archive, 'csName': 'correct'})
        os.remove(path_archive)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue('csId' in response.data)
        if 'csId' in response.data:
            DELETE_CORE_SAMPLE(response.data['csId'])

    def test_conflict(self):
        """Test POST api/core_sample/upload with same archive"""
        LOGIN(self.main_user)
        path_archive = self.archive_generator.correct()

        archive = open(path_archive, 'rb')
        client.post(self.url, data={'archive': archive, 'csName': 'archive'})
        archive.close()

        same_archive = open(path_archive, 'rb')
        response = client.post(self.url, data={'archive': same_archive, 'csName': 'same_archive'})
        same_archive.close()

        os.remove(path_archive)
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
        self.assertTrue('csId' in response.data)
        if 'csId' in response.data:
            DELETE_CORE_SAMPLE(response.data['csId'])

    def test_error__not_authorization(self):
        """Test POST api/core_sample/upload without token"""
        LOGOUT()
        response = client.post(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_error__without_archive(self):
        """Test POST api/core_sample/upload without archive"""
        LOGIN(self.main_user)
        response = client.post(self.url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


