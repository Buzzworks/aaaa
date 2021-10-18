from django.core.management.base import BaseCommand
from flexydial import settings
from callcenter.models import Campaign, User
import pickle

class Command(BaseCommand):

	help = "Disable WFH Functionality"
	def handle(self, **options):
		enable_wfh = pickle.loads(settings.R_SERVER.get('enable_wfh') or pickle.dumps(False))
		if enable_wfh:
			Campaign.objects.all().update(wfh=False)
			User.objects.update(call_type='webrtc')
			settings.R_SERVER.delete('enable_wfh')
			print('Work From Home functionality is disabled for all campaigns')
		else:
			print('Work From Home functionality is already disabled for all campaigns')