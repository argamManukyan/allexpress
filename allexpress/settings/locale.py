from .settings import *
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'PASSWORD': config('DB_PASSWORD'),
        'USER': config('DB_USER'),
        'HOST': 'localhost',
        'OPTIONS': {
            'isolation_level': ISOLATION_LEVEL_READ_COMMITTED

        },
    }
}

DEBUG = True