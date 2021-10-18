from django.core.management.base import BaseCommand
from callcenter.models import *

class Command(BaseCommand):

	help = "User switch Reference"

	def handle(self, **options):
		switch_obj = Switch.objects.filter()[0]
		user_variable = UserVariable.objects.all()
		for user_obj in user_variable:
			user_obj.domain = switch_obj.id
			user_obj.save()
		print("*********************************************************")
		print("!!!!!!!!!!  User Switch Reference Updated SUCCEFULLY  !!!!!!!!!!")
		print("*********************************************************")