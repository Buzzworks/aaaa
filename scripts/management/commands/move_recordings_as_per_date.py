from django.core.management.base import BaseCommand
import os, shutil
from datetime import date

class Command(BaseCommand):

	help = "sagregate recording dir"

	def handle(self, **options):
		record_path = '/var/spool/freeswitch/default/'
		for file in os.listdir(record_path):
			if len(file)>10 and file[:10]!=date.today().strftime('%d-%m-%Y'):
				dir_name = file[:10]
				dir_path = record_path + dir_name
				if not os.path.exists(dir_path):
					os.makedirs(dir_path)
				if os.path.exists(dir_path):
					file_path = record_path + file
					shutil.move(file_path, dir_path)
		print('=========== Previous day call recordings sorted =================')