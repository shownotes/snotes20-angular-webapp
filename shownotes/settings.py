"""
Django settings for shownotes project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'snotes20',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'shownotes.urls'

WSGI_APPLICATION = 'shownotes.wsgi.application'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
#    'DEFAULT_PERMISSION_CLASSES': [
#        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#    ]
}

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Logging
# https://docs.djangoproject.com/en/1.7/topics/logging/

LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'snotes20.management.commands.importexternal': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'snotes20.management.commands.refreshdocstate': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

AUTHENTICATION_BACKENDS = (
    'snotes20.showpadauth.NModelBackend',
    'snotes20.showpadauth.ShowPadBackend'
)

PASSWORD_HASHERS = (
    'snotes20.showpadauth.NPBKDF2PasswordHasher',
)

SITEURL = ""

EMAILS = {
    'activation': {
        'subject': {
            'en': 'shownot.es account activation',
            'de': 'shownot.es Kontoaktivierung',
        }
    },
    'newmail_confirmation': {
        'subject': {
            'en': 'shownot.es email confirmation',
            'de': 'shownot.es Emailbestätigung',
        }
    },
    'pwreset': {
        'subject': {
            'en': 'shownot.es password reset',
            'de': 'shownot.es Passwortreset',
        }
    }
}

DEFAULT_FROM_EMAIL = ''

EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

TEMPLATE_DIRS = (
    BASE_DIR + '/snotes20/emailtemplates/',
)


# for CORS-Headers via CorsMiddleware
ALLOWED_HOSTS = []
CORS_ALLOW_CREDENTIALS = True


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# custom user model
AUTH_USER_MODEL = 'snotes20.NUser'

# import deployment settings form local_settings.py
try:
    from .local_settings import *
except ImportError:
    pass
