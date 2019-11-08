from django.test import TestCase


class Temp_Test(TestCase):
    def setUp(self):
        self.value = 6

    def test_1(self):
        self.assertEqual(self.value, 6)

    def test_2(self):
        self.assertEqual(self.value + 1, 7)
from django.test import TestCase


class Temp_Test(TestCase):
    def setUp(self):
        self.value = 6

    def test_1(self):
        self.assertEqual(self.value, 6)

    def test_2(self):
        self.assertEqual(self.value + 1, 7)
