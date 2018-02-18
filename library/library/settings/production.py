from .local import *

DEBUG = False

DATABASES = {
    'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'library',
                    'HOST': 'db',
                    'PORT': '5432'
                }
}

