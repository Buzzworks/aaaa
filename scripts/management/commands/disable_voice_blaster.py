from django.core.management.base import BaseCommand
from flexydial import settings
from callcenter.models import Campaign
import pickle

class Command(BaseCommand):

	help = "Disable Voice Blaster Functionality"
	def handle(self, **options):
		enable_vb = pickle.loads(settings.R_SERVER.get('enable_vb') or pickle.dumps(False))
		if enable_vb:
			Campaign.objects.all().update(voice_blaster=False)
			settings.R_SERVER.delete('enable_vb')
			print('Voice Blaster functionality is disabled for all campaigns')
		else:
			print('Voice Blaster functionality is already disabled for all campaigns')