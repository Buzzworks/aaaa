from django.core.management.base import BaseCommand
from django.conf import settings 
from callcenter.models import Campaign

class Command(BaseCommand):

	help = "Campaign dfmf wfh dict change"

	def handle(self, **options):
		camp_obj = Campaign.objects.filter()
		for camp in camp_obj:
			if '0' in camp.wfh_dispo:
				camp.wfh_dispo['0']= 'Redial'
				camp.wfh_dispo['1'] = 'CallBack'
				camp.wfh_dispo['2'] = camp.wfh_dispo.pop('1')
				camp.wfh_dispo['1'] = camp.wfh_dispo['1'] = camp.wfh_dispo.pop('0')
			camp.wfh_dispo = camp.wfh_dispo
			camp.save()
		print("campaings Udated with  Dtmf")
