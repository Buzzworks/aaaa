from django.core.management.base import BaseCommand
from crm.models import Contact,ContactInfo

class Command(BaseCommand):

	help = "Update campaign sticky_agent_map in campaign dial_method with sticky_agent_map key"

	def handle(self, **options):
		count = 0
		contact_info = ContactInfo.objects.filter()
		for con_inf in contact_info:
			Contact.objects.filter(id=con_inf.contact_id).update(customer_raw_data=con_inf.customer_raw_data)
			count +=1
			
		print("************* Compete With "+str(count)+" *********** ContactInfo")