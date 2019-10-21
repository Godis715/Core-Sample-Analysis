from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Core_sample


class Core_sample_Test(TestCase):
    """ Test module for Core_sample model """

    def __init__(self):
        self.user = User.objects.get(username='dima12101')

    def setUp(self):
        Core_sample.objects.create(
            control_sum='', name='Cs_1', user=self.user, deposit='1', hole='2', top='1.0', bottom='5.5')
        Core_sample.objects.create(
            control_sum='', name='Cs_2', user=self.user, deposit='5', hole='1', top='0', bottom='5.1')

    def test_puppy_breed(self):
        cs_1 = Core_sample.objects.get(name='Cs_1')
        cs_2 = Core_sample.objects.get(name='cs_2')
        self.assertEqual(cs_1.user, self.user)
