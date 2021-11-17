from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = "FlexyDial Manager- Managing Back-end Activities"
    def handle(self, **options):
        from scripts import manager
        manager.Execute()