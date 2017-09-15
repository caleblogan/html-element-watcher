from celery import shared_task


@shared_task
def check_html_element_task(watchelement_id):
    print('nice nice')
    print('id:', watchelement_id)
