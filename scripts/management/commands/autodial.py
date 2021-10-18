from django.core.management.base import BaseCommand
from optparse import make_option
import time
import logging

class Command(BaseCommand):

    help = "Describe AutoDial Commands"
    def handle(self, **options):
        logging.basicConfig(format='[%(asctime)s] %(levelno)s' \
                '(%(process)d) %(module)s: %(message)s', level=logging.DEBUG)
        logging.debug("Starting AutoDial Daemon...")
        logging.warning("AutoDial Daemon is running...")
        logging.warning("Quit the daemon with CONTROL-C")
        from scripts import autodial
        autodial.exec_autodial()



