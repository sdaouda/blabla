"""
Django settings for myshop project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
# -*- coding: utf-8 -*-
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '97vqo*t)m)h_3pjjw4(=9m&kc*-_a*30icly_ifg$80jeg_cbz'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '97vqo*t)m)h_3pjjw4(=9m&kc*-_a*30icly_ifg$80jeg_cbz')

# SECURITY WARNING: don't run with debug turned on in production!

#export DJANGO_DEBUG='False'
#DEBUG = True
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

#ALLOWED_HOSTS = ['immoniger.herokuapp.com']
ALLOWED_HOSTS = ['blablacarniger.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'blablaCar',
    'widget_tweaks',
    'tempus_dominus',
    'crispy_forms',
   # 'bootstrap_datepicker_plus',
  #  "bootstrap4",
)
CRISPY_TEMPLATE_PACK = 'bootstrap4'
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'blablaCar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blablaCar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blablaDB',
        'USER': 'postgres',
        'PASSWORD': 'Mar@2019',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
TEMPUS_DOMINUS_LOCALIZE = False
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Africa/Niamey'
#TIME_ZONE = 'UTC'
USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
#LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, '/blablaCar/static/')

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

##os.makedirs(STATIC_TMP, exist_ok=True)
##os.makedirs(STATIC_ROOT, exist_ok=True)
##
### Extra places for collectstatic to find static files.
##STATICFILES_DIRS = (
##    os.path.join(BASE_DIR, 'static'),
##)
