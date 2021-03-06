"""
Django settings for sm project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# To avoid the problem of local development or production modifications
# to settings.py in git, we created a local_settings.py file to store the
# particular settings for running this application either in the development
# or production environments.
# The local_settings.py file should exist in the same directory as settings.py
# and should have the following variables:
# LOCAL_SECRET_KEY
# LOCAL_DEBUG 
# LOCAL_ALLOWED_HOSTS
# LOCAL_STAGE_DATABASE_NAME
# LOCAL_STAGE_DATABASE_USER
# LOCAL_STAGE_DATABASE_PASSWORD
# LOCAL_PRODUCTION_DATABASE_NAME
# LOCAL_PRODUCTION_DATABASE_USER
# LOCAL_PRODUCTION_DATABASE_PASSWORD
# with the proper values for the environment in which the application is running.
# THIS FILE SHOULD NOT BE ADDED TO GIT 

# Import local_settings.py, this file should not be added to git
# since it should only contain settings for the current environment

from .local_settings import (LOCAL_SECRET_KEY, LOCAL_DEBUG, LOCAL_ALLOWED_HOSTS,
                             LOCAL_STAGE_DATABASE_NAME, LOCAL_STAGE_DATABASE_USER,
                             LOCAL_STAGE_DATABASE_PASSWORD, LOCAL_PRODUCTION_DATABASE_NAME,
                             LOCAL_PRODUCTION_DATABASE_USER, LOCAL_PRODUCTION_DATABASE_PASSWORD)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = LOCAL_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = LOCAL_DEBUG

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = LOCAL_ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'sm_tests.apps.SmTestsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    # COMMENTED FOR NOW THIS HAS TO BE ENABLED 'rest_framework_swagger',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'sm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'development': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': LOCAL_STAGE_DATABASE_NAME,
        'USER': LOCAL_STAGE_DATABASE_USER,
        'PASSWORD': LOCAL_STAGE_DATABASE_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },


    'stage': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': LOCAL_STAGE_DATABASE_NAME,
        'USER': LOCAL_STAGE_DATABASE_USER,
        'PASSWORD': LOCAL_STAGE_DATABASE_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },

    'production': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': LOCAL_PRODUCTION_DATABASE_NAME,
        'USER': LOCAL_PRODUCTION_DATABASE_USER,
        'PASSWORD': LOCAL_PRODUCTION_DATABASE_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }



}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
