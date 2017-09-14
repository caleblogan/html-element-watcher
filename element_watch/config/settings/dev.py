from .base import *


SECRET_KEY = 'ullff*1p(44e@)8^y&i!(fwy!lt+d^++z=s7a4hzube#)aiv&w'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'nice_pass'),
        'HOST': os.environ.get('POSTGRES_HOST', '192.168.99.100'),
        'PORT': os.environ.get('POSTGRES_PORT', '5433'),
    }
}

