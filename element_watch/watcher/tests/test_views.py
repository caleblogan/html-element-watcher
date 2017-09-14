import datetime
from unittest import mock

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.http import Http404
from django.contrib.sites.models import Site

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken

from ..models import WatchedElement


class TestHomeView(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('test_user1', password='nice_pass')
        self.user2 = User.objects.create_user('test_user2', password='nice_pass')
        self.view_reverse = reverse('watcher:home')

    def test_exists_at_desired_url(self):
        resp = self.client.get('/')
        self.assertNotEqual(resp.status_code, 404)

    def test_anon_user_is_redirected_to_login(self):
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.redirect_chain[0][1], 302)
        self.assertEqual(resp.redirect_chain[0][0], '/accounts/login/?next=/')

    def test_logged_in_user_can_access_page(self):
        login = self.client.login(username='test_user1', password='nice_pass')
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_context_watched_tasks(self):
        WatchedElement.objects.create(
            user=self.user1,
            url='http://127.0.0.1',
            html_element='tag',
            callback_url='http://localhost:8000/cb/'
        )
        login = self.client.login(username='test_user1', password='nice_pass')
        resp = self.client.get('/')
        self.assertIn('watched_elements', resp.context)
        self.assertEqual(len(resp.context['watched_elements']), 1)
