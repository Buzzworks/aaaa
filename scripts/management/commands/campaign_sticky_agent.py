from django.core.management.base import BaseCommand
from crm.models import *
from callcenter.models import *

class Command(BaseCommand):

	help = "Update campaign sticky_agent_map in campaign dial_method with sticky_agent_map key"

	def handle(self, **options):
		count = 0
		campaigns = Campaign.objects.filter()
		for camp in campaigns:
			dial_method = camp.dial_method
			if 'sticky_agent_map' not in camp.dial_method:
				dial_method['sticky_agent_map'] = False
				camp.dial_method = dial_method
				camp.save()
				count +=1
			else:
				continue
		print("************* Compete With "+str(count)+" *********** Campaign")