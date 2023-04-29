import os

from .settings import *
from .settings import BASE_DIR  # noqa

ALLOWED_HOSTS = [os.getenv("WEBSITE_HOSTNAME")] if "WEBSITE_HOSTNAME" in os.environ else []
CSRF_TRUSTED_ORIGINS = ["https://" + os.getenv("WEBSITE_HOSTNAME")] if "WEBSITE_HOSTNAME" in os.environ else []
DEBUG = False

conn_str = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
conn_str_params = {pair.split("=")[0]: pair.split("=")[1] for pair in conn_str.split(" ")}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conn_str_params["dbname"],
        'USER': conn_str_params["user"],
        'PASSWORD': conn_str_params["password"],
        'HOST': conn_str_params["host"],
        'PORT': conn_str_params["port"]
    }
}






