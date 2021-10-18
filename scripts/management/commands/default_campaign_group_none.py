from django.core.management.base import BaseCommand
from flexydial import settings
import pickle
from callcenter.models import Campaign
class Command(BaseCommand):

	help = "Set default is group campaign false"

	def handle(self, **options):
		campaigns = Campaign.objects.all()
		for camp in campaigns:
			if not camp.is_trunk_group or camp.is_trunk_group == None:
				camp.is_trunk_group = False
				camp.save()


		