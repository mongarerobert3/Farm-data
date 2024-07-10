import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Create initial superuser and social app'

    def handle(self, *args, **kwargs):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser'))

        # Create social app
        site, _ = Site.objects.get_or_create(domain='farm-data.onrender.com', name='Farm Data')
        if not SocialApp.objects.filter(provider='google').exists():
            SocialApp.objects.create(
                provider='google',
                name='Google',
                client_id= os.environ.get('client_id'),
                secret= os.environ.get('secret'),
                site=site
            )
            self.stdout.write(self.style.SUCCESS('Successfully created Google SocialApp'))
