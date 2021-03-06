import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class WatchedElement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    html_element = models.CharField(max_length=200, help_text='Css selector for the element to watch.')
    element_value = models.TextField(blank=True, null=True)
    check_interval_hours = models.FloatField(default=1.0, help_text='The interval to check html element in hours.')
    cur_task_id = models.CharField(max_length=36, null=True, blank=True, help_text='Celery task id')
    callback_url = models.URLField()
    last_checked = models.DateTimeField(
        default=timezone.now,
        help_text='Last time the html element was checked for changes.'
    )

    def get_absolute_url(self):
        return reverse('watcher:watched_element_detail', args=[str(self.id)])

    def next_scheduled_update(self):
        return self.last_checked + datetime.timedelta(hours=self.check_interval_hours)

    def __str__(self):
        return f'{self.user} ({self.html_element})'
