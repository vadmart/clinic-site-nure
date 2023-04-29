import os
from .settings import *

ALLOWED_HOSTS = [os.getenv("WEBSITE_HOSTNAME")] if "WEBSITE_HOSTNAME" in os.environ else []
CSRF_TRUSTED_ORIGINS = ["https://" + os.getenv("WEBSITE_HOSTNAME")] if "WEBSITE_HOSTNAME" in os.environ else []
DEBUG = False

conn_str = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
conn_str_params = {pair.split("=")[0]: pair.split("=")[1] for pair in conn_str.split(" ")}

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







