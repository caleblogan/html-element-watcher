from datetime import timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import DataError
from django.utils import timezone

from watcher.models import WatchedElement


class TestWatchedElement(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='bob', password='nice_pass')
        WatchedElement.objects.create(
            user=user,
            url='http://127.0.0.1',
            html_element='tag',
            callback_url='http://localhost:8000/cb/'
        )

    def setUp(self):
        pass

    def test_str(self):
        elem = WatchedElement.objects.all()[0]
        self.assertEqual(str(elem), 'bob (tag)')

    def test_absolute_url(self):
        elem = WatchedElement.objects.all()[0]
        self.assertEqual(elem.get_absolute_url(), f'/watched-element/{elem.id}/')
