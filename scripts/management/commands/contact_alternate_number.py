from django.core.management.base import BaseCommand
from crm.models import *

class Command(BaseCommand):

	help = "Alternate number create at alternate number table"

	def handle(self, **options):
		contact = Contact.objects.all()
		for c in contact.iterator():
			if c.alt_numeric:
				AlternateContact.objects.create(contact=c,phonebook=c.phonebook, uniqueid=c.uniqueid, alt_numeric=c.alt_numeric)

		print("*********************************************************")
		print("!!!!!!!! ALTERNATE NUMBER Created SUCCESSFULLY   !!!!!!!!")
		print("*********************************************************")