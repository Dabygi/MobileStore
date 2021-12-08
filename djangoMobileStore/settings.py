"""
Django settings for djangoMobileStore project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import dj_database_url
from pathlib import Path
from django.contrib.messages import constants as message_constants

from todo.mail.producers import imap_producer
from todo.mail.consumers import tracker_consumer
from todo.mail.delivery import smtp_backend, console_backend


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'v9dhgv_^7!cals+&2b-zt*g!ltar=@mr5m+b05uj!284a@'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'v9dhgv_^7!cals+&2b-zt*g!ltar=@mr5m+b05uj!284a@')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

DEBUG = bool( os.environ.get('DJANGO_DEBUG', True) )

ALLOWED_HOSTS = ['mobile-my-store.herokuapp.com','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'store',
    'specs',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'rest_framework',
    'todo',
    'dal',
    'dal_select2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'djangoMobileStore.urls'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SECURITY_WARN_AFTER = 5
SESSION_SECURITY_EXPIRE_AFTER = 12

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'store/templates', 'todo/templates/todo'), os.path.join(BASE_DIR, 'store/templates', 'allauth', 'todo/templates/todo')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoMobileStore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ecom_mobile_db',
        'USER': 'ecomuser',
        'PASSWORD': 'devpass',
        'HOST': '127.0.0.1',
        'PORT': 5432
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_REDIRECT_URL = "/"

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


gettext = lambda s: s

LANGUAGES = (
    ('ru', gettext('Russia')),
    ('en', gettext('English')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Without this, uploaded files > 4MB end up with perm 0600, unreadable by web server process
FILE_UPLOAD_PERMISSIONS = 0o644

CRISPY_TEMPLATE_PACK = 'bootstrap4'

SITE_ID = 1

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Override CSS class for the ERROR tag level to match Bootstrap class name
MESSAGE_TAGS = {message_constants.ERROR: "danger"}

# Todo-specific settings
TODO_STAFF_ONLY = False
TODO_DEFAULT_LIST_ID = None
TODO_DEFAULT_ASSIGNEE = 'Dabygi'
TODO_DEFAULT_LIST_SLUG = 'trouble'
TODO_PUBLIC_SUBMIT_REDIRECT = '/'
TODO_ALLOW_FILE_ATTACHMENTS = True
TODO_LIMIT_FILE_ATTACHMENTS = [".jpg", ".gif", ".png", ".csv", ".pdf"]


# Heroku: Update database configuration from $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/1.10/howto/static-files/
#
# # The URL to use when referring to static files (where they will be served from)
# STATIC_URL = '/static/'
#
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
#
# # The absolute path to the directory where collectstatic will collect static files for deployment.
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#
# # Simplified static file serving.
# # https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "live-static", "static-root")

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#STATIC_ROOT = "/home/cfedeploy/webapps/cfehome_static_root/"

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "live-static", "media-root")