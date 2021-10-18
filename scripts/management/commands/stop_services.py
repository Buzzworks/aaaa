from django.core.management.base import BaseCommand
from django.conf import settings 
import os
import subprocess 

class Command(BaseCommand):

	help = "Stop the application services"

	def handle(self, **options):
		freeswitch_cmd = 'sudo service freeswitch stop'
		cdrd_cmd = 'sudo service flexydial-cdrd stop'
		autodial_cmd = 'sudo service flexydial-autodial stop'
		dialplan_cmd = 'sudo service flexydial-fs-dialplan stop'
		print("Services Stopping................")
		dialplan_status = subprocess.call(dialplan_cmd, shell=True)
		autodial_status = subprocess.call(autodial_cmd, shell=True)
		cdrd_status = subprocess.call(cdrd_cmd, shell=True)
		freeswitch_status = subprocess.call(freeswitch_cmd, shell=True)