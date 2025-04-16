
import os
from pathlib import Path
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p#ut&qt1+#sygjtvdfn_^#1kr^!846=l0%u_$hq*=i2loppid%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['isterlab.qateeb.com','127.0.0.1']


CSRF_TRUSTED_ORIGINS = [f"http://{host}" for host in ALLOWED_HOSTS] + [f"https://{host}" for host in ALLOWED_HOSTS]

FILE_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024  # 25 MB in bytes

# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "django.contrib.admin",  # required
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "django.contrib.humanize",

    "daphne",

    'django.contrib.staticfiles',
    'ckeditor',
        'channels',

    "django_eventstream",
    'constance',
    'landing',
    'chatbot'
]
# Allow embedding in iframes
X_FRAME_OPTIONS = 'ALLOWALL'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

ASGI_APPLICATION = "isterlab.asgi.application"
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.gzip.GZipMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'isterlab.urls'

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
                'constance.context_processors.config',
                'landing.context_processors.global_context'

            ],
        },
    },
]

WSGI_APPLICATION = 'isterlab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, "isterlab/static"),
]
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CONSTANCE_ADDITIONAL_FIELDS = {
    'choices_select': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': ((None, "-----"), ("stripe", "Stripe"), ("moyasar", "Moyasar"),("adyent","Adyent"))
    }
    ],
    'image_field': ['django.forms.ImageField', {'required': False}],  # Make it optional

}

CONSTANCE_CONFIG={
    'WEBSITE_NAME': ("Isterlab", 'WEBSITE NAME'),
    'WEBSITE_URL': ("https://isterlab.qateeb.com/", 'WEBSITE URL'),
    'LOGO': ("",'','image_field'),
    'G4_GOOGLE_ANAYTICS_PROPERTY_ID': ("",'G4_GOOGLE_ANAYTICS_PROPERTY_ID'),
    'COVERAGES_EXECLUDE_COUNTRIES': ("Yemen, Sudan,Cuba,Syria,Israel,Mali",'Exclude from coverages area'),
    'PRIVACY': ("",'PRIVACY'),
    'BANNER': ("",'BANNER','image_field'),
    'DESCRIPTION': ("Team up with the best collaboration from the right expertises.", 'WEBSITE DESCRIPTION'),
    'PRIMARY_PHONE': ('', 'PRIMARY_PHONE'),
    'SECONDARY_PHONE': ('', 'SECONDARY_PHONE'),
    'BASE_ADDRESS': ("", 'BASE_ADDRESS'),
    'CONTACT_EMAIL': ("", 'CONTACT_EMAIL'),
    'NUMBER_OF_CLIENTS': ('0', 'NUMBER_OF_CLIENTS'),
    'NUMBER_OF_PROJECTS': ('0', 'NUMBER_OF_PROJECTS'),
    'NUMBER_OF_YEARS': ('10', 'NUMBER_OF_YEARS'),
    'FACEBOOK_PAGE': ('', 'Facebook Page'),
    'X_PAGE': ('', 'X Page'),
    'LINKEDIN_PAGE': ('', 'LinkedIn Page'),
    'RECAPTCHA_API_KEY': (config('RECAPTCHA_API_KEY',''), 'ReCAPTCHA API Key'),
    'RECAPTCHA_SECRET_KEY': (config('RECAPTCHA_SECRET_KEY',''), 'ReCAPTCHA Secret Key'),

}

from .unfold.settings import UNFOLD
