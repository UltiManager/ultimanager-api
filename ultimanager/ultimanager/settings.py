"""
Django settings for ultimanager project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import logging
import os

import requests


def env_bool(name: str, default=False) -> bool:
    """
    Pull a boolean parameter from the environment. If the value of the
    environment variable is ``True`` (case insensitive) then ``True``
    will be returned. All other values return ``False``.

    Args:
        name:
            The name of the boolean parameter to read.
        default:
            The default value to return.

    Returns:
        The boolean equivalent of the named environment variable
        according to the above rules.
    """
    if name not in os.environ:
        return default

    raw_value = env_param(name, is_required=False, default="false")

    return raw_value.lower() == "true"


def env_list(name: str, delimiter=",") -> list:
    """
    Get a list of delimited parameters from the environment.

    Args:
        name:
            The name of the environment variable to read.
        delimiter:
            The delimiter used to separate values.

    Returns:
        A list of elements produced by splitting the specified
        environment variable on the given delimiter. If the variable is
        missing or has an empty value, an empty list is returned.
    """
    raw_value = env_param(name, is_required=False, default="")

    if not raw_value:
        return []

    return raw_value.split(delimiter)


def env_param(name: str, is_required=True, default=None) -> str:
    """
    Pull a parameter from the environment.

    Args:
        name:
            The name of the parameter to fetch.
        is_required:
            A boolean indicating if the parameter is required.
        default:
            A default value to use if the parameter is not required.

    Returns:
        The string value of the environment variable with the given
        name.
    """
    if is_required:
        return os.environ[name]

    return os.getenv(name, default)


SILENCED_SYSTEM_CHECKS = [
    # Our authentication system relies on unique emails rather than
    # unique usernames.
    "auth.W004"
]


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

DEBUG = env_bool("DEBUG", default=False)
SECRET_KEY = env_param("SECRET_KEY", is_required=not DEBUG, default="secret")


ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")

# If we are running in an ECS environment, we need to add the IP of the
# host machine running the task. This is needed because the load
# balancer checks the status endpoint on the private IP rather than the
# domain name we have set up.
if env_bool("IS_ECS_ENVIRONMENT"):
    resp = requests.get("http://169.254.170.2/v2/metadata")
    data = resp.json()

    container_meta = data["Containers"][0]
    private_ip = container_meta["Networks"][0]["IPv4Addresses"][0]

    ALLOWED_HOSTS.append(private_ip)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-Party Apps
    "email_auth",
    "rest_framework",
    # Custom Apps
    "account",
    "account.api",
    "core",
    "landing",
    "teams",
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

ROOT_URLCONF = "ultimanager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "ultimanager.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASE_TYPE = env_param(
    "DB_TYPE", is_required=False, default="sqlite"
).lower()

if DATABASE_TYPE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "HOST": env_param("DB_HOST"),
            "NAME": env_param("DB_NAME"),
            "PASSWORD": env_param("DB_PASSWORD"),
            "PORT": env_param("DB_PORT", is_required=False, default="5432"),
            "USER": env_param("DB_USER"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }


# Custom User Model

AUTH_USER_MODEL = "account.User"


# Authenticate with email addresses

AUTHENTICATION_BACKENDS = ["email_auth.authentication.VerifiedEmailBackend"]


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"  # noqa
    },
]


# Security Settings (HTTPS Related)

if env_bool("IS_HTTPS"):
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    # If Django is running behind a load balancer that terminates SSL we
    # can use the following header to determine if the original
    # connection came over HTTPS.
    SSL_PROXY_HEADER_NAME = env_param(
        "SSL_PROXY_HEADER_NAME", is_required=False, default=None
    )
    if SSL_PROXY_HEADER_NAME:
        SECURE_PROXY_SSL_HEADER = (
            SSL_PROXY_HEADER_NAME,
            env_param("SSL_PROXY_HEADER_VALUE"),
        )


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Store files in S3

if env_bool("USE_S3_STORAGE"):
    DEFAULT_FILE_STORAGE = "custom_storages.backends.MediaStorage"
    STATICFILES_STORAGE = "custom_storages.backends.StaticStorage"

    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=31536000"}
    AWS_S3_REGION_NAME = env_param("AWS_REGION")

    S3_BUCKET_MEDIA = env_param("S3_BUCKET_MEDIA")
    S3_BUCKET_STATIC = env_param("S3_BUCKET_STATIC")


# Sentry Configuration

SENTRY_DSN = env_param("SENTRY_DSN", is_required=False, default=None)

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    sentry_logging = LoggingIntegration(
        event_level=logging.WARNING, level=logging.INFO
    )
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), sentry_logging],
        release=env_param(
            "SENTRY_RELEASE", is_required=False, default="unknown"
        ),
    )
