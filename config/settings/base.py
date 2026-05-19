import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# CSRF_TRUSTED_ORIGINS = [
#     "http://127.0.0.1:8000",
#     "http://localhost:8000",
# ]

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "web",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.organizations',
    'apps.subscriptions',
    'apps.api_keys',
    'apps.usage',
    'apps.billing',
    'apps.audit',
    'rest_framework',
    'silk',
    'django_celery_beat',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "silk.middleware.SilkyMiddleware",
    "config.utils.middleware.APIResponseMiddleware",

]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"), 
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = "accounts.User"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        "apps.organizations.authentication.OrganizationJWTAuthentication",
        "apps.api_keys.authentication.APIKeyAuthentication",

    ),

    # throttling (APIKey.rate_limit)
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
        "apps.api_keys.throttling.APIKeyRateThrottle",
        "apps.api_keys.throttling.OrganizationRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": "100/min",
        "anon": "20/min",
        "api_key": "1000/hour",
        "organization": "5000/hour",
    },

    # custom exception handler
    "EXCEPTION_HANDLER":
        "config.utils.exceptions.custom_exception_handler",

    # schema generation for API documentation
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',    
    
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://redis:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://redis:6379/0")

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} {message}",
            "style": "{",
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },

    "root": {
        "handlers": ["console"],
        "level": "INFO",
    }
}



# Sentry configuration - https://docs.sentry.io/platforms/python/guides/django/
# sentry_sdk.init(
    # dsn="YOUR_DSN", #link to sentry project
    # integrations=[DjangoIntegration()],
    # traces_sample_rate=1.0,
    # send_default_pii=True
# )



# Celery Beat Schedule for periodic tasks
CELERY_BEAT_SCHEDULE = {

    "cleanup-old-logs": {
        "task": "apps.usage.tasks.cleanup_old_logs",
        "schedule": crontab(hour=0, minute=0),
    },

    "deactivate-expired-subscriptions": {
        "task": "apps.subscriptions.tasks.deactivate_expired_subscriptions",
        "schedule": crontab(hour=1, minute=0),
    },

    "reset-old-usage-records": {
        "task": "apps.usage.tasks.reset_old_usage_records",
        "schedule": crontab(
            day_of_month=1,
            hour=0,
            minute=0
        ),
    },
}


# Logging configuration - logs will be written to logs/app.log 
os.makedirs("logs", exist_ok=True)
LOGGING = {

    "version": 1,

    "disable_existing_loggers": False,

    "formatters": {

        "standard": {
            "format":
                "[{asctime}] "
                "{levelname} "
                "{name} "
                "{message}",
            "style": "{",
        },
    },

    "handlers": {

        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },

        "file": {
            "class": "logging.FileHandler",
            "filename": "logs/app.log",
            "formatter": "standard",
        },
    },

    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}



