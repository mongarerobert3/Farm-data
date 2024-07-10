from .settings import *

# Database
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('ENGINE'),
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOST'),
        'PORT': os.environ.get('PORT'), 	
    }
}


# Debug mode
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['localhost']
