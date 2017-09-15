import datetime
from unittest import mock

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.http import Http404
from django.contrib.sites.models import Site

import requests
import responses

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken

from ..models import WatchedElement
from ..tasks import check_html_element_task


class TestCheckHtmlElementTask(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('test_user1', password='nice_pass')
        self.watched_element = WatchedElement.objects.create(
            user=self.user1,
            url='http://127.0.0.1/',
            html_element='.likes',
            callback_url='http://localhost:8000/cb/',
            last_checked=timezone.now() - datetime.timedelta(minutes=30),
        )

    @responses.activate
    def test_requests_called_with_correct_url(self):
        responses.add(responses.GET, self.watched_element.url, status=200)

        check_html_element_task(self.watched_element.id)
        self.assertEqual(responses.calls[0].request.url, self.watched_element.url)

    @responses.activate
    def test_sets_last_checked_to_now(self):
        responses.add(responses.GET, self.watched_element.url, status=200)

        check_html_element_task(self.watched_element.id)
        elem = WatchedElement.objects.get(pk=self.watched_element.id)
        self.assertIs(timezone.now() - elem.last_checked < datetime.timedelta(seconds=30), True)

    @responses.activate
    def test_sets_last_checked_to_now_on_errors(self):
        check_html_element_task(self.watched_element.id)
        elem = WatchedElement.objects.get(pk=self.watched_element.id)
        self.assertIs(timezone.now() - elem.last_checked < datetime.timedelta(seconds=30), True)

    @responses.activate
    def test_new_element_value_saved(self):
        html = """
            <div class="midcol unvoted">
                <div class="arrow up login-required access-required" data-event-action="upvote" role="button" aria-label="upvote" tabindex="0">
                </div>
                <div class="score dislikes" title="37244">37.2k</div>
                <div class="score unvoted" title="37245">37.2k</div>
                <div class="score likes" title="37246">37.2k</div>
                <div class="arrow down login-required access-required" data-event-action="downvote" role="button" aria-label="downvote" tabindex="0">
                </div>
            </div>
        """
        responses.add(responses.GET, self.watched_element.url, status=200, body=html)
        responses.add(responses.POST, self.watched_element.callback_url, status=200)

        check_html_element_task(self.watched_element.id)

        self.assertIs(f'class="score likes"' in responses.calls[0].response.text, True)
        elem = WatchedElement.objects.get(pk=self.watched_element.id)
        self.assertEqual(elem.element_value, '37.2k')

    @responses.activate
    def test_callback_url_called_with_data(self):
        responses.add(responses.GET, self.watched_element.url, status=200, body='<div class="likes">nice</div>')
        responses.add(responses.POST, self.watched_element.callback_url, status=200)

        check_html_element_task(self.watched_element.id)
        elem = WatchedElement.objects.get(pk=self.watched_element.id)
        self.assertEqual(responses.calls[1].request.url, self.watched_element.callback_url)
        self.assertEqual(responses.calls[1].request.body, 'new_value=nice')

    @responses.activate
    def test_callback_url_not_called_if_data_has_not_changed(self):
        responses.add(responses.GET, self.watched_element.url, status=200, body='<div class="likes">nice</div>')
        responses.add(responses.POST, self.watched_element.callback_url, status=200)
        self.watched_element.element_value = 'nice'
        self.watched_element.save()

        check_html_element_task(self.watched_element.id)
        elem = WatchedElement.objects.get(pk=self.watched_element.id)
        self.assertEqual(len(responses.calls), 1)
