from django.core.management.base import BaseCommand
from django.conf import settings 
import os
import subprocess 

class Command(BaseCommand):

	help = "Re-Start the application services"

	def handle(self, **options):
		freeswitch_cmd = 'sudo service freeswitch restart'
		cdrd_cmd = 'sudo service flexydial-cdrd restart'
		autodial_cmd = 'sudo service flexydial-autodial restart'
		dialplan_cmd = 'sudo service flexydial-fs-dialplan restart'
		freeswitch_status = subprocess.call(freeswitch_cmd, shell=True)
		print("services Re-starting................")
		if freeswitch_status == 0:
			cdrd_status = subprocess.call(cdrd_cmd, shell=True)
			autodial_status = subprocess.call(autodial_cmd, shell=True)
			dialplan_status = subprocess.call(dialplan_cmd, shell=True)
		else:
			print("Error Re-starting freeswitch !...........")