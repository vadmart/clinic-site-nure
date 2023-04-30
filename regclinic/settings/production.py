import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = [os.getenv("WEBSITE_HOSTNAME")] if "WEBSITE_HOSTNAME" in os.environ else []
CSRF_TRUSTED_ORIGINS = ["https://" + os.getenv("WEBSITE_HOSTNAME")] if "WEBSITE_HOSTNAME" in os.environ else []


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
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conn_str_params["dbname"],
        'USER': conn_str_params["user"],
        'PASSWORD': conn_str_params["password"],
        'HOST': conn_str_params["host"],
        'PORT': int(conn_str_params["port"])
    }
}
