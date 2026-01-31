from decouple import config
from pathlib import Path
from datetime import timedelta
from .unfold_config import UNFOLD
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import os


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(-#7l!t!w92wdex1%e*1llm7q@g67hj3%@+f8lnopi+ntd+0ez'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'https://api.sufismarket.com',
    'https://sufismarket.com',
]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://sufismarket.com',
    'https://api.sufismarket.com',
]


INSTALLED_APPS = [
    "unfold",  
    "unfold.contrib.filters",
    "unfold.contrib.forms",  
    "unfold.contrib.inlines",  
    "unfold.contrib.import_export", 
    "unfold.contrib.guardian",  
    "unfold.contrib.simple_history",  
    "unfold.contrib.location_field",  
    "unfold.contrib.constance",  
    "django.contrib.admin",  
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    

     # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'rest_framework_simplejwt.token_blacklist',
    'query_counter',
    'corsheaders',


    # Local apps
    'apps.user',
    'apps.product',
    'apps.cart',
    'apps.checkout',
    'apps.review',
    'apps.order',
    'apps.authentication',
    'apps.favorite',
    'apps.address',
]

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'apps.common.exception_handler.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'query_counter.middleware.DjangoQueryCounterMiddleware',
]

AUTH_USER_MODEL = 'user.User'

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Enable efficient static file serving in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=None)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=None)
ADMIN_EMAIL = config('ADMIN_EMAIL', default=None)
