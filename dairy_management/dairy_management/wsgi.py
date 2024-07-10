"""
WSGI config for dairy_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dairy_management.settings')

application = get_wsgi_application()

# Run the management command
from django.core.management import call_command
try:
    call_command('setup_initial_data')
except Exception as e:
    print(f"Error running setup_initial_data: {e}")