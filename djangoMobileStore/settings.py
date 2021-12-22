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
    'storages'
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


# # Статика через WhiteNoise
# STATIC_URL = '/static/'
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# # Статика и медиа через Amazon S3
# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
# AWS_DEFAULT_ACL = 'public-read'
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
#
# AWS_STATIC_LOCATION = 'static'
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/'
# STATICFILES_STORAGE = 'djangoMobileStore.s3utils.StaticStorage'
#
# MEDIA_ROOT = 'media'
# AWS_PUBLIC_MEDIA_LOCATION = 'media'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_PUBLIC_MEDIA_LOCATION}/'
# DEFAULT_FILE_STORAGE = 'djangoMobileStore.s3utils.MediaStorage'
# STATICFILES_STORAGE = 'djangoMobileStore.s3utils.StaticStorage'
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, 'static')





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_DEFAULT_ACL = 'None'    #'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'djangoMobileStore.s3utils.StaticStorage'
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'djangoMobileStore.s3utils.PublicMediaStorage'
    # s3 private media settings
    PRIVATE_MEDIA_LOCATION = 'private'
    PRIVATE_FILE_STORAGE = 'djangoMobileStore.s3utils.PrivateMediaStorage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)