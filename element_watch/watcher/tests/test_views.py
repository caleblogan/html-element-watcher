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


class TestWatchedElementCreateView(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('test_user1', password='nice_pass')
        self.user2 = User.objects.create_user('test_user2', password='nice_pass')
        self.view_reverse = reverse('watcher:watched_element_create')

    def test_exists_at_url(self):
        resp = self.client.get('/watched-element/create/')
        self.assertNotEqual(resp.status_code, 404)

    def test_anon_user_is_redirected_to_login(self):
        resp = self.client.get('/watched-element/create/')
        self.assertEqual(resp.status_code, 302)

    def test_logged_in_user_can_access_form(self):
        login = self.client.login(username='test_user1', password='nice_pass')
        resp = self.client.get(self.view_reverse)
        self.assertEqual(resp.status_code, 200)

    @mock.patch('watcher.views.check_html_element_task')
    def test_user_can_submit_valid_form(self, task_mock):
        task_mock.configure_mock(**{'delay.return_value.id': '123'})
        login = self.client.login(username='test_user1', password='nice_pass')
        resp = self.client.post(
            self.view_reverse,
            {
                'url': 'http://localhost:8000/',
                'html_element': 'nice',
                'check_interval_hours': 2,
                'callback_url': 'http://localhost:8000/cb/'
            }
        )
        self.assertRedirects(resp, reverse('watcher:home'))
        self.assertEqual(len(WatchedElement.objects.all()), 1)

    @mock.patch('watcher.views.check_html_element_task')
    def test_check_html_element_task_called_correctly(self, task_mock):
        task_mock.configure_mock(**{'delay.return_value.id': '123'})
        login = self.client.login(username='test_user1', password='nice_pass')
        resp = self.client.post(
            self.view_reverse,
            {
                'url': 'http://localhost:8000/',
                'html_element': 'nice',
                'check_interval_hours': 2,
                'callback_url': 'http://localhost:8000/cb/'
            }
        )
        elems = WatchedElement.objects.all()
        task_mock.delay.assert_called_with(elems[0].id)

    @mock.patch('watcher.views.check_html_element_task')
    def test_task_id_is_saved_to_object(self, task_mock):
        task_mock.configure_mock(**{'delay.return_value.id': '123'})
        login = self.client.login(username='test_user1', password='nice_pass')
        resp = self.client.post(
            self.view_reverse,
            {
                'url': 'http://localhost:8000/',
                'html_element': 'nice',
                'check_interval_hours': 2,
                'callback_url': 'http://localhost:8000/cb/'
            }
        )
        elem = WatchedElement.objects.all()[0]
        self.assertEqual(elem.cur_task_id, '123')
