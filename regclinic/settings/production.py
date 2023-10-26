import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = [os.getenv("WEBSITE_HOSTNAME")] if "WEBSITE_HOSTNAME" in os.environ else ["127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["https://" + os.getenv("WEBSITE_HOSTNAME")] if "WEBSITE_HOSTNAME" in os.environ else []

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

conn_str = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
conn_str_params = {pair.split("=")[0]: pair.split("=")[1] for pair in conn_str.split(" ")}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false":
            {
                "()": 'django.utils.log.RequireDebugFalse'
            }},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'clinic.sqlite3'
    }
}
