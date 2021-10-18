from django.core.management.base import BaseCommand
from django.conf import settings
from callcenter.models import *
from flexydial.constants import MODULE_LIST
from datetime import time
class Command(BaseCommand):
	help = "Dummy Fixture"
	# def add_arguments(self, parser):
	#    parser.add_argument('--verbose', action='store_true')
	def handle(self, **options):
		Modules.objects.all().delete()
		for module in MODULE_LIST:
			children = module['children']
			del module['children']
			parent = Modules.objects.create(**module)
			if children:
				for child in children:
					del child['children']
					child['parent'] = parent
					Modules.objects.create(**child)
		print('!!!!!!!!!!! MOdules Updated !!!!!!!!!!!!!!!!!')

		md_name = list(Modules.objects.filter().exclude(parent=None).values_list('name',flat=True))
		usr_role = UserRole.objects.all()
		for i in usr_role:
			for mod in md_name:
				if mod not in i.permissions:
					i.permissions.update({mod:[]})
			i.save()
		print('!!!!!!!!!!! Modules added in Access management !!!!!!!!!!!!!!!!!')