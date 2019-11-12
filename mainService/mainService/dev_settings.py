import os
import sys


ALLOWED_HOSTS = ['*']


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))


DEBUG = True

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]


try:
	from local_settings import *

	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.postgresql_psycopg2',
	        'NAME': DATABASE_NAME_DEV,
	        'USER': DATABASE_USER,
	        'PASSWORD': DATABASE_PASSWORD,
	        'HOST': HOST,
	        'PORT': DATABASE_PORT,
	    }
	}

except ImportError:

	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.sqlite3',
	        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	    }
	}
