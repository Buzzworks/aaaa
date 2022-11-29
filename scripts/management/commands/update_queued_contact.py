from django.core.management.base import BaseCommand
from crm.models import *
from callcenter.models import *
from datetime import date, timedelta

class Command(BaseCommand):

	help = "Alternate number update"

	def handle(self, **options):
		try:
			tempcontact = TempContactInfo.objects.values_list('contact_id',flat=True)
			contacts = Contact.objects.filter(status='Queued').exclude(id__in=tempcontact)
			print(contacts.count(), 'contacts in queued')
			for contact in contacts:
				calldetail = CallDetail.objects.filter(contact_id=contact.id, created__gte=contact.modified_date)
				if not calldetail.exists():
					diallerevent = DiallerEventLog.objects.filter(contact_id=contact.id, created__gte=contact.modified_date)
					if diallerevent.exists():
						d_obj = diallerevent.values().first()
						if not d_obj['phonebook'] and contact.phonebook:
							d_obj['phonebook'] = contact.phonebook.name
						del d_obj['transfer_history']
						del d_obj['info']
						del d_obj['channel']
						del d_obj['id']
						d_obj["uniqueid"] = d_obj.uniqueid
						c_obj = CallDetail.objects.create(**d_obj)
						c_obj.hangup_source = 'System'
						c_obj.created = d_obj['created']
						c_obj.updated = d_obj['updated']
						c_obj.save()
						if not CdrFeedbck.objects.filter(session_uuid = d_obj['session_uuid']).exists():
							cdr_feedback = CdrFeedbck.objects.create(feedback={},relation_tag=[],session_uuid=d_obj['session_uuid'],contact_id=d_obj['contact_id'],comment='',calldetail=c_obj)
							if d_obj['dialed_status'] == 'Connected':
								cdr_feedback.primary_dispo = 'AutoFeedback'
								cdr_feedback.save()
						if d_obj['dialed_status'] == 'Connected':
							contact.status = 'Dialed'
						else:
							contact.status = d_obj['dialed_status']
						if diallerevent.first().user:
							contact.last_connected_user = diallerevent.first().user.extension
						contact.last_dialed_date = d_obj.get('init_time', None)
						contact.dial_count = contact.dial_count + 1
						contact.save()
					else:
						prev_calldetail = CallDetail.objects.filter(contact_id=contact.id).order_by('-created')
						if prev_calldetail.exists():
							if prev_calldetail.first().dialed_status == 'Connected':
								contact.status = 'Dialed'
							elif prev_calldetail.first().dialed_status == 'NOT_FOUND':
								contact.status = 'NC'
							else:
								contact.status = prev_calldetail.first().dialed_status
						else:
							contact.status = 'NotDialed'
						contact.save()
				else:
					if calldetail.first().dialed_status == 'Connected':
						contact.status = 'Dialed'
					else:
						contact.status = calldetail.first().dialed_status
					if calldetail.first().user:
						contact.last_connected_user = calldetail.first().user.extension
					contact.last_dialed_date = calldetail.first().init_time
					contact.dial_count = contact.dial_count + 1
					contact.save()
			print('Contacts status updated')
		except Exception as e:
			print('Exception in create_calldetial_missing_contact', e)