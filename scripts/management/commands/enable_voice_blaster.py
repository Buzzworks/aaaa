from django.core.management.base import BaseCommand
from flexydial import settings
from callcenter.models import Campaign
import pickle

class Command(BaseCommand):

	help = "Enable Voice Blaster Functionality"
	def handle(self, **options):
		enable_vb = pickle.loads(settings.R_SERVER.get('enable_vb') or pickle.dumps(False))
		if not enable_vb:
			Campaign.objects.all().update(voice_blaster=True)
			settings.R_SERVER.set('enable_vb',pickle.dumps(True))
			print('Voice Blaster functionality is enable for all campaigns')
		else:
			print('Voice Blaster functionality is already enable for all campaigns')