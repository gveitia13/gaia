"""
Django settings for gaia project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['currency', 'X-Session-ID', 'content-type']
CORS_ALLOWED_ORIGINS = ['http://localhost:5173',]
CSRF_TRUSTED_ORIGINS = ['https://*.127.0.0.1', 'https://gaia-mercado.com/', 'https://*.gaia-mercado.com/', 'http://localhost:5173']
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5s5r7(&3kc#x&(a3%@$ienldvsj$axcl7k(81s&aojt)%zk5jl'
TECHNOSTAR = False
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_main',
    'app_cart',
    'ckeditor',
    'ckeditor_uploader',
    'corsheaders',
    'widget_tweaks',
    'rest_framework',
    'django_cleanup.apps.CleanupConfig',
    # 'chatmarket.apps.ChatmarketConfig',
]

CKEDITOR_CONFIGS = {
    'default': {
        "skin": "moono-lisa",
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
        "toolbar_Full": [
            [
                "Styles",
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                "Undo",
                "Redo",
            ],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Flash", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
        ],
        "toolbar": "Full",
        "height": 150,
        "width": 500,
        "filebrowserWindowWidth": 940,
        "filebrowserWindowHeight": 725,
    }
}

BUSINESS_LOGO_PATH = 'img/logo_pill.png'
BUSINESS_NAME = 'GAIA'
BUSINESS_NAME_IMG_PATH = 'img/gaia_bg.png'
BUSINESS_BANNER = 'img/banner.png'

JAZZMIN_SETTINGS = {
    "site_brand": BUSINESS_NAME,
    "welcome_sign": '',
    'site_icon': BUSINESS_LOGO_PATH,
    'site_logo': BUSINESS_LOGO_PATH,
    'site_logo_classes': 'brand-image',
    "login_logo": BUSINESS_NAME_IMG_PATH,
    "login_logo_dark": False,
    'site_header': BUSINESS_NAME,
    "custom_css": 'css/admin.css',
    'copyright': 'GAIA',
    'custom_js': 'js/admin.js',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

ROOT_URLCONF = 'gaia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'gaia.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gaia_test',
        'USER': 'postgres',
        'PASSWORD': 'gaia098*',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'gaia',
#         'USER': 'postgres',
#         'PASSWORD': 'rootzenBL',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Havana'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

CKEDITOR_UPLOAD_PATH = "info/"
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'gaia.store.cuba@gmail.com'
EMAIL_HOST_PASSWORD = 'ehyqfphlarwlrizj'  # past the key or password app here
EMAIL_PORT = 587
EMAIL_USE_TLS = True

LOGIN_REDIRECT_URL = '/admin/'

LOGOUT_REDIRECT_URL = reverse_lazy('admin:login')

LOGIN_URL = reverse_lazy('admin:login')

CART_SESSION_ID = "cart"

SESSION_COOKIE_AGE = 7200

TPP_CLIENT_ID = 'f12538a0aa85242baa9f137380ab1926'
TPP_CLIENT_SECRET = '323b25d45c305000cec8c8a70afc4cda'
TPP_CLIENT_EMAIL = 'gaia.habana2021@gmail.com'
TPP_CLIENT_PASSWORD = 'Gaia2021'
TPP_URL = "www.tropipay.com"
TPP_SUCCESS_URL = 'https://gaia-mercado.com/tropipay/success/'
TPP_FAILED_URL = 'https://gaia-mercado.com/tropipay/fails/'
TPP_NOTIFICACION_URL = 'https://gaia-mercado.com/tropipay/verificar/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'local': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
