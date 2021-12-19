from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'PASSWORD': config('DB_PASSWORD'),
        'USER': config('DB_USER'),
        'HOST': 'localhost',
        'OPTIONS': {
            'isolation_level': 'read committed'
        },
    }
}