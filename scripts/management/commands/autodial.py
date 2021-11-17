from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = "Describe AutoDial Commands"
    def handle(self, **options):

        from scripts import autodial
        autodial.exec_autodial()



