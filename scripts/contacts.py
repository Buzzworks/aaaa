from crm.models import Contact, TempContactInfo, LeadListPriority
from datetime import datetime, timedelta
from django.db.models import Q
from django.db import transaction
from django.db import connections

def num_update(numbers):
	for number in numbers:
		number.status = 'Dialed'
	TempContactInfo.objects.bulk_update(numbers,['status'])

def delete_lead_priority(campaign, contacts):
	key = ''
	if campaign.lead_priotize:
		for keys in campaign.lead_priotize.keys():
			key = str(keys)
		if key and 'status' in campaign.lead_priotize[key] and campaign.lead_priotize[key]['status']==str('true') and contacts.exists():
			for i in contacts:
				if i.uniqueid and 'tac' in campaign.lead_priotize[key]:
					LeadListPriority.objects.filter(uniqueid=i.uniqueid,campaign_id=campaign.id).exclude(is_global=True).delete()
					
def autodial_num_fetch(campaign, count, check_user):
	"""Return list of numbers
	Takes campaign and total count of numbers to fetch from DB to dial call.
	"""
	try:
		before_one_minute = datetime.now() - timedelta(minutes=1)
		TempContactInfo.objects.filter(campaign=campaign, modified_date__lte=before_one_minute, status='Dialed-Queued').update(status='NotDialed')
		if check_user:
			contacts = TempContactInfo.objects.filter(Q(campaign=campaign, status='NotDialed'), Q(user=None)|Q(user='')).order_by('created_date','priority')[0:count]
		else:
			contacts = TempContactInfo.objects.filter(Q(campaign=campaign, status='NotDialed')).order_by('created_date','priority')[0:count]
		delete_lead_priority(campaign, contacts)
		return contacts
	except Exception as e:
		print("Expection at Autodial_num_fetch")
	finally:
		transaction.commit()
		connections["crm"].close()
		connections["default"].close()

def autodial_num_update(campaign, numbers, description=""):
	"""
	Takes campaign and list of numbers in arguments
	and update those numbers in DB on which the call has happened.
	"""
	try:
		if description == 'NDNC':
			TempContactInfo.objects.filter(contact_id__in=numbers).delete()
			Contact.objects.filter(id__in=numbers).update(status='NDNC')
		else:
			print("autodial_num_update",numbers)
			TempContactInfo.objects.filter(id__in=numbers).update(status='Dialed-Queued', modified_date=datetime.now())
			# TempContactInfo.objects.filter(id__in=numbers).delete()
	except Exception as e:
		print(e)
	finally:
		transaction.commit()
		connections["crm"].close()
		connections["default"].close()
