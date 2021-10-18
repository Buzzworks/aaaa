from django.core.management.base import BaseCommand
from crm.models import *
from callcenter.models import *
from datetime import date, timedelta

class Command(BaseCommand):

	help = "Alternate number update"

	def handle(self, **options):
		try:
			start_date = date(2020, 8, 12)
			end_date = date(2020, 9, 25)
			delta = timedelta(days=1)
			while start_date <= end_date:
				CallDetail.objects.filter(session_uuid=None, created__date=start_date).delete()
				calldetail_session = CallDetail.objects.filter(created__date=start_date).exclude(session_uuid=None).values_list('session_uuid',flat=True)
				diallerlog_entry = DiallerEventLog.objects.filter(created__date=start_date).exclude(session_uuid__in=calldetail_session).values()
				print(diallerlog_entry.count(), 'missing record entry in diallerevent on', start_date)
				for d_obj in diallerlog_entry:
					uniqueid = None
					if 'contact_id' in d_obj and d_obj['contact_id']:
						contact_obj = Contact.objects.filter(id=d_obj['contact_id'])
						if contact_obj.exists():
							uniqueid = contact_obj.first().uniqueid
							if not d_obj['phonebook'] and contact_obj.first().phonebook:
								d_obj['phonebook'] = contact_obj.first().phonebook.name
					del d_obj['transfer_history']
					del d_obj['info']
					del d_obj['channel']
					del d_obj['id']
					d_obj["uniqueid"] = uniqueid
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
				print('calldetial entry created from diallerevetlog on', start_date)
				start_date += delta
		except Exception as e:
			print('Exception in create_calldetial_missing_contact', e)