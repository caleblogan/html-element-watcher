import datetime

from django.utils import timezone

import requests
from celery import shared_task
from bs4 import BeautifulSoup

from .models import WatchedElement


@shared_task
def check_html_element_task(watched_element_id):
    watched_element = WatchedElement.objects.get(pk=watched_element_id)
    try:
        resp = requests.get(watched_element.url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        selected_elems = soup.select(watched_element.html_element)
        if len(selected_elems) > 0:
            element_value = ''.join(selected_elems[0].contents)
            if element_value != watched_element.element_value:
                requests.post(watched_element.callback_url, data={'new_value': element_value})
            watched_element.element_value = element_value
    except requests.ConnectionError as e:
        pass
    finally:
        watched_element.last_checked = timezone.now()
        task = check_html_element_task.apply_async(
            (watched_element.id,),
            eta=timezone.now() + datetime.timedelta(hours=watched_element.check_interval_hours)
        )
        watched_element.cur_task_id = task.id
        watched_element.save()


if __name__ == '__main__':
    resp = requests.get('https://www.reddit.com/r/all/', headers={'User-agent': 'Mozman'})
    print(resp.status_code)
    soup = BeautifulSoup(resp.text, 'html.parser')
    print(soup.select('#siteTable > div:nth-of-type(1) .likes')[0].contents)
