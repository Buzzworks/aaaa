from django.core.management.base import BaseCommand
from crm.models import *
from callcenter.models import *

class Command(BaseCommand):

	help = "Update campaign sticky_agent_map in campaign dial_method with sticky_agent_map key"

	def handle(self, **options):
		count = 0
		broadcast_obj = BroadcastMessages.objects.filter()
		for broadcast in broadcast_obj:
			if type(broadcast.receivers) == list:
				user_dict = {}
				for user_extension in broadcast.receivers:
					user_dict[user_extension] = True
			broadcast.receivers = user_dict
			broadcast.save()
			count +=1
		print("************* Compete With "+str(count)+" *********** ")