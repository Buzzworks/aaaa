from django.core.management.base import BaseCommand
from crm.models import *
from callcenter.models import *
from django.conf  import settings
import pickle

class Command(BaseCommand):

	help = "Create or Update Trunk Channel in redis"

	def handle(self, **options):
		TRUNK = pickle.loads(settings.R_SERVER.get("trunk_status") or pickle.dumps({}))
		campaigns = Campaign.objects.all()
		for camp in campaigns:
			if camp.status =='Active':
				if camp.is_trunk_group:
					for trunk in camp.trunk_group.trunks.all().order_by('priority'):
						if trunk.trunk.status =='Active':
							if str(trunk.trunk.id) not in TRUNK:
								TRUNK[str(trunk.trunk.id)] = 0
								# TRUNK[str(trunk.id)][camp.name] = {'c_total_chennals':0,'predictive':0,'progressive':0,'preview':0,'manual':0,'inbound':0,'redial':0,'callback':0,'voice-blaster':0}
							# else:
							# 	if str(camp.name) not in TRUNK[str(trunk.id)]:
							# 		TRUNK[str(trunk.id)][camp.name] = {'c_total_chennals':0,'predictive':0,'progressive':0,'preview':0,'manual':0,'inbound':0,'redial':0,'callback':0,'voice-blaster':0}
						else:
							if str(trunk.trunk.id) in TRUNK:
								del TRUNK[str(trunk.trunk.id)]
				else:
					if camp.trunk and camp.trunk.status =='Active':
						if str(camp.trunk.id) not in TRUNK:
								TRUNK[str(camp.trunk.id)] = 0
								# TRUNK[str(camp.trunk.id)][camp.name] = {'c_total_chennals':0,'predictive':0,'progressive':0,'preview':0,'manual':0,'inbound':0,'redial':0,'callback':0,'voice-blaster':0}
						# else:
						# 	if str(camp.name) not in TRUNK[str(camp.trunk.id)]:
						# 		TRUNK[str(camp.trunk.id)][camp.name] = {'c_total_chennals':0,'predictive':0,'progressive':0,'preview':0,'manual':0,'inbound':0,'redial':0,'callback':0,'voice-blaster':0}
					else:
						if camp.trunk and str(camp.trunk.id) in TRUNK:
							del TRUNK[str(camp.trunk.id)]
			# else:
			# 	for trunk_keys in TRUNK.keys():
			# 		if camp.name in TRUNK[str(trunk_keys)]:
			# 			del TRUNK[str(trunk_keys)][camp.name]
		settings.R_SERVER.set("trunk_status", pickle.dumps(TRUNK))
		print("************************************************ \n")
		print(TRUNK)
		print(" \n************************************************")
		print("Trunk Status dictionary successfully created!")