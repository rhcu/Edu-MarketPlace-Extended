from django.test import TestCase
from django.urls import reverse

# Create your tests here.
import datetime

class BasicTests(TestCase):

    def test_index_page_returns_200_code(self):
        """
        returns true, if starting page always returns something
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page_returns_200_code(self):
        """
        returns true, if logout page always returns something
        """
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
