from django.core.management.base import BaseCommand
from django.conf import settings 
from callcenter.models import * 

class Command(BaseCommand):

	help = "Update switch screen modules"

	def handle(self, **options):
		md_name = list(Modules.objects.filter().values_list('name',flat=True))
		if 'switchscreen' not in md_name:
			update_screen = {'switchscreen':[]}
			Modules.objects.create(name='switchscreen',permissions='R')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_screen)
				i.save()
		else:
			print("already Module is present")
		print("********************************************************************")
		print("!!!!!!!!!!  Module and UserRole Updated with switchscreen !!!!!!!!!!")
		print("********************************************************************")
