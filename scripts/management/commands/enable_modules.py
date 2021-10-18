from django.core.management.base import BaseCommand
from flexydial import settings
import pickle
from flexydial.constants import MODULES as MODULES_LIST	

class Command(BaseCommand):

	help = "Enable Modules Functionality"

	def add_arguments(self, parser):
		parser.add_argument('module_name', nargs='+', type=str)

	def handle(self, **options):
		module_name = str(options['module_name'][0]).split(',')
		for md_name in module_name:
			if md_name in MODULES_LIST:
				enable = pickle.loads(settings.R_SERVER.get(md_name) or pickle.dumps(False))
				if not enable:
					settings.R_SERVER.set(md_name,pickle.dumps(True))
					print(md_name,'**** This Module successfully enabled ****')
				else:
					print(md_name,'**** This Module already enabled ****')
			else:
				print(md_name, 'This module is unavailable, Please Select option from following ---', MODULES_LIST)