from django.core.management.base import BaseCommand
from optparse import make_option
import time

class Command(BaseCommand):

    help = "Describe CDR commands"

    #def add_arguments(self, parser):
    #    parser.add_argument('--verbose', action='store_true')

    def handle(self, **options):
        print ("Starting CDR Daemon...\n")
        print (time.strftime("%Y-%m-%d %I:%M:%S", time.localtime()))
        print ("CDR Daemon is running...")
        print ("Quit the daemon with CONTROL-C")
        from scripts import fecd
        fecd.run_task()

