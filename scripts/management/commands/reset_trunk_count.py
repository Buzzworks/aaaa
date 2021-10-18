from django.core.management.base import BaseCommand
from django.conf import settings
import pickle 

class Command(BaseCommand):

	help = "Reset trunk count in redis"

	def handle(self, **options):
		settings.R_SERVER.set("trunk_status", pickle.dumps({}))
		print('!!!!!!!!!!!!!! Trunk count reset in redis !!!!!!!!!!!!!!')