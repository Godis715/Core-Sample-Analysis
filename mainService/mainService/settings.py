"""
Django settings for mainService workstation.

Generated by 'django-admin startproject' using Django 2.2.5.

"""

import os
import sys
import environ

# reading .env file and added variable in os.environ
environ.Env.read_env('.env')


# if 'INSTALL' not in os.environ or os.environ['INSTALL'] != 'Done':   
#     # os.system ('pip install -r requirements.txt')
#     os.system ('ls -a')
#     os.environ['INSTALL'] = 'Done'


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

# Paths for import
sys.path.append(os.path.join(BASE_DIR, 'archiveDecoder'))


if 'IS_PRODACTION' in os.environ:

	DEBUG = False

	STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

	ALLOWED_HOSTS = ['localhost', '46.149.233.52']

	# Raises django's ImproperlyConfigured exception if KEY not in os.environ
	if 'DATABASE_USER' in os.environ and 'DATABASE_PASSWORD' in os.environ:
		DATABASES = {
		    'default': {
		        'ENGINE': 'django.db.backends.postgresql_psycopg2',
		        'NAME': 'Core-Sample-Analysis-db-prod',
		        'USER': os.environ['DATABASE_USER'],
		        'PASSWORD': os.environ['DATABASE_PASSWORD'],
		        'HOST': '46.149.233.52',
		        'PORT': 5432,
		    }
		}
	else:
		DATABASES = {
		    'default': {
		        'ENGINE': 'django.db.backends.sqlite3',
		        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
		    }
		}
else:

	DEBUG = True

	STATICFILES_DIRS = [
    	os.path.join(PROJECT_ROOT, 'static'),
	]

	ALLOWED_HOSTS = ['*']

	# Raises django's ImproperlyConfigured exception if KEY not in os.environ
	if 'DATABASE_USER' in os.environ and 'DATABASE_PASSWORD' in os.environ:
		DATABASES = {
		    'default': {
		        'ENGINE': 'django.db.backends.postgresql_psycopg2',
		        'NAME': 'Core-Sample-Analysis-db-dev',
		        'USER': os.environ['DATABASE_USER'],
		        'PASSWORD': os.environ['DATABASE_PASSWORD'],
		        'HOST': '46.149.233.52',
		        'PORT': 5432,
		    }
		}
	else:
		DATABASES = {
		    'default': {
		        'ENGINE': 'django.db.backends.sqlite3',
		        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
		    }
		}

# Raises django's ImproperlyConfigured exception if KEY not in os.environ
if 'SECRET_KEY' in os.environ:

	SECRET_KEY = os.environ['SECRET_KEY']

else:

	from django.utils.crypto import get_random_string
	chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

	SECRET_KEY = get_random_string(50, chars)

if 'test' in sys.argv:
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.sqlite3',
	        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	    }
	}

# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
)

LOCAL_APPS = (
    'workstation',
    'core_sample',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mainService.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'template'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mainService.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# Settings of rest_framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', )
}

# To allow all hosts.
CORS_ORIGIN_ALLOW_ALL = True

# If ``True``, cookies will be allowed to be included in cross-site HTTP requests.
CORS_ALLOW_CREDENTIALS = True

#Created root static apps
if not os.path.exists(f'{PROJECT_ROOT}/static/core_sample'):
	os.makedirs(f'{PROJECT_ROOT}/static/core_sample')
