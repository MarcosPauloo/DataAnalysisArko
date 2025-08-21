# locations/management/commands/check_app.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'A simple command to check if the app is configured correctly.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('>>> O app "locations" está funcionando! <<<'))