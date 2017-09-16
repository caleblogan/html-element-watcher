from .base import *


SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = os.environ.get('DJANGO_DEBUG', False)

ALLOWED_HOSTS += ['murmuring-wave-93908.herokuapp.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_NAME'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT']
    }
}


CELERY_BROKER_READ_URL = os.environ['RABBITMQ_BIGWIG_RX_URL']
CELERY_BROKER_WRITE_URL = os.environ['RABBITMQ_BIGWIG_TX_URL']
