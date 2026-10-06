import logging
from pathlib import Path

import environ
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)

# load .env if exists
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

# SECURITY
SECRET_KEY = env("SECRET_KEY", default="unsafe-secret-key")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Applications

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'jalali_date',
    'OMS',
    'UMS',
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

ROOT_URLCONF = 'gold.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'OMS.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'gold.wsgi.application'

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="secret-c901ba7flocalhost:5432/gold"
    )
}

AUTH_USER_MODEL = 'UMS.User'
LOGIN_URL = 'do_login'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

USE_X_FORWARDED_HOST = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CELERY_BROKER_URL = env(
#     "CELERY_BROKER_URL",
#     default="redis://127.0.0.1:6379/0"
# )
#
# CELERY_RESULT_BACKEND = env(
#     "CELERY_RESULT_BACKEND",
#     default="redis://127.0.0.1:6379/1"
# )
#
# CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_TASK_SERIALIZER = "json"

# CELERY_BEAT_SCHEDULE = {
#     "fetch-every-5-seconds": {
#         "task": "OMS.tasks.task.test_task",
#         "schedule": 5.0,
#     },
# }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "[{levelname}] {asctime} {name}: {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },

    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },

        "OMS": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },

        "UMS": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },

        # Celery logs (if you enable Celery)
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
