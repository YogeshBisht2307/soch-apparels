import os
import logging
from dotenv import load_dotenv
from typing import List, Dict

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger()

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KEY_ID: str = os.environ['RAZORPAY_APP_ID']
KEY_SECRET: str = os.environ['RAZORPAY_SECRET_ID']
SECRET_KEY: str = os.environ['APPLICATION_SECRET_KEY']

DEBUG: bool = True if os.environ['STAGE'].upper() == 'DEV' else False

ALLOWED_HOSTS: List = [ '*' ]

INSTALLED_APPS: List = [
    'store',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms'
]

CRISPY_TEMPLATE_PACK: str = 'bootstrap4'

MIDDLEWARE: List = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF: str = 'SochApparels.urls'

TEMPLATES: List = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION: str = 'SochApparels.wsgi.application'


# Database

# DATABASES: Dict = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES: Dict = {
    'default': {
        'ENGINE'  : 'django.db.backends.mysql', 
        'NAME'    : os.environ['DATABASE_NAME'],
        'USER'    : os.environ['DATABASE_USERNAME'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST'    : os.environ['DATABASE_HOST'],
        'PORT'    : '',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS: List = [
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
LANGUAGE_CODE: str = 'en-us'
TIME_ZONE: str = 'UTC'
USE_I18N: bool = True
USE_L10N: bool = True
USE_TZ: bool = True


# Static files (CSS, JavaScript, Images)
STATIC_URL: str = '/static/'

# Media URL
print(BASE_DIR)
MEDIA_ROOT: str = BASE_DIR
MEDIA_URL: str = '/upload/images/media/'

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'


#smtp configurations

EMAIL_HOST: str = os.environ['EMAIL_HOST']
EMAIL_PORT: str = os.environ['EMAIL_PORT']
EMAIL_USE_TLS: str = os.environ['EMAIL_USE_TLS']
EMAIL_HOST_USER: str = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD: str = os.environ['EMAIL_HOST_PASSWORD']
