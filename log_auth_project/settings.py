import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'test-secret-key'

DEBUG = True

ALLOWED_HOSTS = []

ROOT_URLCONF = "log_auth_project.urls"

STATIC_URL = '/static/'

# Установленные приложения.
INSTALLED_APPS = [
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",

	# Мои приложения.
	"apps.users",
	"apps.mock_objects",
	"apps.admin_tools",
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

WSGI_APPLICATION = "log_auth_project.wsgi.application"

# Конфигурация базы данных для тестов.
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		"NAME": BASE_DIR / 'db.sqlite3',
	}
}

# Настройки для времени и локации.
USE_TZ = True
TIME_ZONE = 'UTC'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"