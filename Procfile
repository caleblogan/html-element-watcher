web: gunicorn --env DJANGO_SETTINGS_MODULE=element_watch.config.settings.prod element_watch.config.wsgi --log-file - --log-level debug
worker: celery -A config worker -l info --workdir ./element_watch/
