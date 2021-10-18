from django.core.management.base import BaseCommand
from flexydial import settings
from callcenter.models import Campaign, User
import pickle

class Command(BaseCommand):

	help = "Enable WFH Functionality"
	def handle(self, **options):
		enable_wfh = pickle.loads(settings.R_SERVER.get('enable_wfh') or pickle.dumps(False))
		if not enable_wfh:
			Campaign.objects.update(wfh=True)
			User.objects.update(call_type='2')
			settings.R_SERVER.set('enable_wfh',pickle.dumps(True))
			print('Work From Home functionality is enable for all campaigns')
		else:
			print('Work From Home functionality is already enable for all campaigns')
