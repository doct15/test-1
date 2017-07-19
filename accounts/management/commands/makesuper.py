from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


#python manage.py makesuper

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="superu").exists():
            User.objects.create_superuser("superu", "admin@maasdigital.io", "admin1979")
