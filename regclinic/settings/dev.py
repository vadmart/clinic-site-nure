from .base import *
from dotenv import load_dotenv

dotenv_path = "regclinic/vars.env"
load_dotenv(dotenv_path)

ALLOWED_HOSTS = ["192.168.1.246", "127.0.0.1", "8e9b-178-150-167-216.ngrok-free.app", "polyclinic.azurewebsites.net"]
DEBUG = True
SECRET_KEY = 'django-insecure-v(l07qvqd1q0@1_521)pho5_lzw_ttgjjcvt-fhink_o0*#^ot'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_NAME"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': "localhost",
        'PORT': 5432
    }
}
