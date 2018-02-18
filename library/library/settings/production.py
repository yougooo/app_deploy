from .local import *

DEBUG = False

DATABASES = {
    'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'library',
                    'USER': 'postgres',
                    'PASSWORD': 'postgres',
                    'HOST': 'db',
                    'PORT': '5432'

                }
}

