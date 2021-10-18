from django.core.management.base import BaseCommand
from crm.models import *
from callcenter.models import *

class Command(BaseCommand):

	help = "Alternate number update"

	def handle(self, **options):
		contact = Contact.objects.all()
		for c in contact.iterator():
			if c.alt_numeric:
				c.alt_numeric = '"alt_num_1" => "'+str(c.alt_numeric)+'"'
				c.save()
		Contact.objects.filter(alt_numeric=None).update(alt_numeric='')

		temcontact = TempContactInfo.objects.all()
		for c in temcontact.iterator():
			if c.alt_numeric:
				c.alt_numeric = '"alt_num_1" => "'+str(c.alt_numeric)+'"'
				c.save()
		TempContactInfo.objects.filter(alt_numeric=None).update(alt_numeric='')

		trashcontact = TrashContact.objects.all()
		for c in trashcontact.iterator():
			if c.alt_numeric:
				c.alt_numeric = '"alt_num_1" => "'+str(c.alt_numeric)+'"'
				c.save()
		TrashContact.objects.filter(alt_numeric=None).update(alt_numeric='')

		callbackcontact = CallBackContact.objects.all()
		for c in callbackcontact.iterator():
			if c.alt_numeric:
				c.alt_numeric = '"alt_num_1" => "'+str(c.alt_numeric)+'"'
				c.save()
		CallBackContact.objects.filter(alt_numeric=None).update(alt_numeric='')

		print("*********************************************************")
		print("!!!!!!!! ALTERNATE NUMBER UPDATED SUCCESSFULLY  !!!!!!!!")
		print("*********************************************************")