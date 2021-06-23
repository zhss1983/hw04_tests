from http import HTTPStatus

from django.test import TestCase


class StaticURLTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
