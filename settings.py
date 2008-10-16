import os
basedir = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(basedir, 'solmujeres.sqlite')

TIME_ZONE = 'America/La_Paz'

LANGUAGE_CODE = 'es'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = os.path.join(basedir, 'sitemedia') 

MEDIA_URL = '/sitemedia/'

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'z&1x(4mfvg!_1_xt3l&93h#oh_9s2cculed#4f3^_yf0%)2nxa'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'congreso.urls'

TEMPLATE_DIRS = (os.path.join(basedir, 'templates'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'contact_form',
    'registration',
    'blog',
    'program',
    'register',
)

ACCOUNT_ACTIVATION_DAYS = 7
