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
    "delivery.apps.DeliveryConfig",
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

# Тестовые данные SDEK
# При использовании в реальном проекте необходимо заменить на боевые данные
SDEK_CALCULATOR_URL = "https://api.edu.cdek.ru/v2/calculator/tarifflist"
SDEK_USER_REGISTER_URL = "https://api.edu.cdek.ru/v2/oauth/token?parameter"
SDEK_CITIES_URL = "https://api.cdek.ru/v2/location/cities/"
SDEK_TEST_USER_DATA = {
    "grant_type": "client_credentials",
    "client_id": "EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI",
    "client_secret": "PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG",
}
# Калькулятор SDEK позволяет получить стомость доставки для всех доступных
# тарифов.
TARIFF_COUNT = 5
SDEK_CURRENCY = 1
SDEK_LANG = "rus"

# Почта РФ
POCHTA_RF_CALCULATOR_URL = "https://delivery.pochta.ru/v2/calculate/tariff?json&object=4030"
MONEY_KOEF = 100  # Перевод копеек в рубли
