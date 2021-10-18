from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from callcenter.models import User

class Command(BaseCommand):

	help = "force logout superuser"
	def handle(self, **options):
		user = User.objects.get(username='admin')
		[s.delete() for s in Session.objects.all() if str(s.get_decoded().get('_auth_user_id')) == str(user.id) ]



