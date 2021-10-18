from django.core.management.base import BaseCommand
from crm.models import *

class Command(BaseCommand):

	help = "Alternate number update"

	def handle(self, **options):
		count = 0
		crm_fields = CrmField.objects.all()
		for crm_field in crm_fields:
			for unique_row in crm_field.crm_fields:
				for section_field in unique_row['section_fields']:
					if section_field['unique']:
						section_field['size'] = 30
						count += 1
			crm_field.save()
		print("*********************************************************************")
		print("!!!!!!!! CRM FIELD "+str(count)+" DATA UPDATED SUCCESSFULLY  !!!!!!!!")
		print("*********************************************************************")