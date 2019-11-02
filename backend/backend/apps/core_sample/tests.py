from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

client = APIClient()


class Account_APITestCase(APITestCase):
    def setUp(self):
        self.username = "username_test"
        self.email = "TestUser@test.com"
        self.password = "password_test"

        self.user = User.objects.create_user(
            self.username, self.email, self.password
        )

        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_login__correct_credentials(self):
        """Test api/login with correct credentials"""
        response = client.post(reverse('login'), data={
                "username": self.username,
                "password": self.password})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'token': self.token.key}, response.data)

    def test_login__not_correct_credentials(self):
        """Test api/login with not correct credentials"""
        response = client.post(reverse('login'), data={
                "username": 'username_not_valid',
                "password": 'password_not_valid'})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_login__without_credentials(self):
        """Test api/login without credentials"""
        response = client.post(reverse('login'))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_logout__without_token(self):
        """Test api/logout without token"""
        response = client.post(reverse('logout'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_logout__with_token(self):
        """Test api/logout with token"""
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.post(reverse('logout'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        token_new, _ = Token.objects.get_or_create(user=self.user)
        self.assertNotEqual(token_new.key, self.token.key)
