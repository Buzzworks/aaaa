from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = "Describe AutoDial Commands"
    def handle(self, **options):

        from scripts import missing_rec_mv
        missing_rec_mv.missing_recording_transfer()