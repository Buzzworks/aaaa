from django.core.management.base import BaseCommand
from crm.models import *
from callcenter.models import *
from django.db.models import Q

class Command(BaseCommand):

	help = "Uniqueid update in DiallerEventLog"

	def handle(self, **options):

		calldetail = CallDetail.objects.all().values('uniqueid','session_uuid')
		for index, call_detail in enumerate(calldetail):
			DiallerEventLog.objects.filter(session_uuid=call_detail['session_uuid']).update(uniqueid=call_detail['uniqueid'])
			if (index % 10000 == 0):
				print(index, 'diallereventlog updated')
			
		diller_event_log = DiallerEventLog.objects.filter(Q(uniqueid=None)|Q(uniqueid='')).exclude(contact_id=None)
		print(diller_event_log.count(), 'needs to update')
		for index, evnt_log in enumerate(diller_event_log):
			contact = Contact.objects.filter(id=evnt_log.contact_id)
			if contact.exists():
				evnt_log.uniqueid = contact.first().uniqueid
				evnt_log.save()
			if (index % 10000 == 0):
				print(index, 'diallereventlog updated')

		print("*********************************************************")
		print("!!!!!!!! DiallerEventLog Uniqueid UPDATED SUCCESSFULLY  !!!!!!!!")
		print("*********************************************************")