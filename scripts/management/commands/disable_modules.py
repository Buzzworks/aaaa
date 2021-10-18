from django.core.management.base import BaseCommand
from flexydial import settings
import pickle
from flexydial.constants import MODULES

class Command(BaseCommand):

	help = "Disable Modules Functionality"

	def add_arguments(self, parser):
		parser.add_argument('module_name', nargs='+', type=str)

	def handle(self, **options):
		module_name = str(options['module_name'][0]).split(',')
		for md_name in module_name:
			if md_name in MODULES:
				disable = pickle.loads(settings.R_SERVER.get(md_name) or pickle.dumps(False))
				if disable:
					settings.R_SERVER.delete(md_name)
					print(md_name,'**** This Module successfully Disabled ****')
				else:
					print(md_name,'**** This Module already Disabled ****')
			else:
				print(md_name, 'This module is unavailable, Please Select option from following ---', MODULES)