import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    default="django-insecure-&*0d2s9fk(6f3^cr6r1$fl5-^vm7*m)ry5i+b0v3%&2z#%@w#b",
)


DEBUG = False

ALLOWED_HOSTS = (
    os.getenv("LOCALHOST_IP"),
    os.getenv("LOCALHOST"),
    os.getenv("CONTAINER_NAME"),
)
INTERNAL_IPS = (os.getenv("LOCALHOST_IP"),)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Сторонние либы
    "rest_framework",

    # Приложения
    "data_handler.apps.DataHandlerConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "root.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "root.wsgi.application"


# Sqlite
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#         "ATOMIC_REQUESTS": True,
#     }
# }

# Postgress
DATABASES = {
    "default": {
        "ENGINE": os.getenv(
            "DB_ENGINE", default="django.db.backends.postgresql"
        ),
        "NAME": os.getenv("DB_NAME", default="postgres7"),
        "USER": os.getenv("POSTGRES_USER", default="postgres7"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="adm"),
        "HOST": os.getenv("DB_HOST", default="db"),
        "PORT": os.getenv("DB_PORT", default="5432"),
        "ATOMIC_REQUESTS": True,
    },
    "test": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


if "test" in sys.argv:
    DATABASES["default"] = DATABASES["test"]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = False

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "120/min",
    },
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
}

CACHE_TIMEOUT = 2 * 60 * 60  # 2 часа
DATA_FIELDS = (
    "customer",
    "item",
    "total",
    "quantity",
    "date",
)
DELIMITER = ","
CLIENT_LIMIT = 5
