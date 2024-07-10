from .settings import *

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dairyfarmdb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306', 	
    }
}


# Debug mode
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['localhost']
