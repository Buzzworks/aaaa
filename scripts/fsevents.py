"""
Receiving signals for events.
"""
import louie
from concurrent.futures import ThreadPoolExecutor
from scripts.eventdump import event_dump
import urllib3
from callcenter.models import (UserVariable, Abandonedcall,Notification,Campaign,DialTrunk)
from crm.models import TempContactInfo,Contact
from django.conf import settings
import pickle,sys,os
from django.db.models import F
import os,sys
AGENTS={}
urllib3.disable_warnings()
pool = ThreadPoolExecutor(max_workers=20)

def capture_events(signal, sender, **kwargs):
	""" 
	Capturing the events that are through from freeswitch 
	and generating the reports 
	"""
	try:
		trunk_id = ''
		ivr_duration = 0 # Ivr Duration if skilled routing is defined
		context = {}
		bill_sec = kwargs.get('variable_billsec', None) # if ivr duration exists billsec zero
		# print(kwargs)
		if kwargs.get('variable_usertype') == "client" or kwargs.get('variable_usertype') == "client_ipphone":
			if kwargs.get('Call-Direction') != 'inbound':
				customer_cid = kwargs.get('variable_cc_customer',kwargs.get('variable_original_caller_id_number', kwargs.get('Caller-Destination-Number',
				 kwargs.get('Caller-Caller-ID-Number', ''))))
			else:
				customer_cid = kwargs.get('Caller-Caller-ID-Number', kwargs.get('Caller-Destination-Number', kwargs.get('variable_original_caller_id_number', '')))[-10:]
			context.update({
				'customer_cid':customer_cid,
				'usertype':kwargs.get('variable_usertype',None),
				'contact_id': kwargs.get('variable_contact_id',None),
				'campaign':kwargs.get('variable_cc_queue', kwargs.get('variable_campaign',kwargs.get('variable_campaign_name',None))),
				'user': kwargs.get('variable_cc_agent',kwargs.get('variable_user_uname',kwargs.get('Caller-Orig-Caller-ID-Number', None))),
				'phonebook':kwargs.get('variable_phonebook', None),
				'session_uuid':kwargs.get('Unique-ID', ''),
				# 'a_leg_uuid':kwargs.get('variable_bridge_uuid', None),
				'a_leg_uuid':kwargs.get('variable_agent-Unique-ID',kwargs.get('variable_bridge_uuid', None)),
				'b_leg_uuid':kwargs.get('Unique-ID', ''),
				'init_time':kwargs.get('variable_start_stamp', None),
				'ring_time':kwargs.get('variable_profile_start_stamp', None),
				'connect_time':kwargs.get('variable_answer_stamp', None),
				'wait_time':kwargs.get('variable_waitsec', None),
				'hold_time':kwargs.get('variable_hold_accum_seconds', None),
				'media_time':kwargs.get('variable_progress_mediasec', None),
				'callflow':kwargs.get('variable_call_direction',kwargs.get('Call-Direction', '')),
				'call_mode':kwargs.get('variable_call_mode', ''),
				'destination_extension': kwargs.get('variable_cc_agent',kwargs.get('Other-Leg-Caller-ID-Number', '')),
				'transfer_history':kwargs.get('variable_transfer_history', ''),
				'call_duration':kwargs.get('variable_duration', None),
				'bill_sec':bill_sec,
				'ivr_duration':ivr_duration,
				'hangup_time':kwargs.get('variable_end_stamp', None),
				'hangup_cause':kwargs.get('variable_hangup_cause', ''),
				'hangup_cause_code':kwargs.get('variable_hangup_cause_q850', None),
				'channel':kwargs.get('variable_channel_name', None),
				'dialed_status':kwargs.get('variable_disposition', kwargs.get('variable_hangup_cause', '')),
				'info':kwargs.get('variable_details', ''),
				'dtmf':kwargs.get('variable_digits_received',None),
				# 'caller_id':kwargs.get('Caller-Destination-Number', kwargs.get('variable_user_uname', None)),
				'caller_id':kwargs.get('variable_origination_caller_id_number',kwargs.get('Caller-Destination-Number', kwargs.get('variable_user_uname', None))),
				'unique_id':kwargs.get('variable_uniqueid',None),
				'wfh_call' :kwargs.get('variable_wfh_call',None),
			})
			if kwargs.get('variable_usertype') != "client_ipphone":
				trunk_id = str(kwargs.get('variable_trunk_id', ''))
				if kwargs.get('Call-Direction') == 'inbound':
					dialed_string = kwargs.get('variable_channel_name',kwargs.get('Channel-Name'))
					destination_number = kwargs.get('Caller-Caller-ID-Number',kwargs.get('Caller-Orig-Caller-ID-Numberv'))
					dial_string1 = str(dialed_string).replace('internal/'+str(destination_number),'external/${destination_number}')
					dial_trunk = DialTrunk.objects.filter(dial_string=dial_string1)
					TRUNK = pickle.loads(settings.R_SERVER.get("trunk_status") or pickle.dumps({}))
					if dial_trunk.exists():
						for trunk in dial_trunk:
							if trunk.status=='Active' and str(trunk.id) in TRUNK:
								trunk_id = str(trunk.id)
								break
				chennals = pickle.loads(settings.R_SERVER.get("trunk_status") or pickle.dumps({}))
				if trunk_id in chennals:
					chennals[trunk_id] -= 1
					if chennals[trunk_id] >=0:
						settings.R_SERVER.set("trunk_status", pickle.dumps(chennals))
			else:
				context['customer_cid'] = kwargs.get('variable_cc_customer',kwargs.get('variable_original_caller_id_number', kwargs.get('Caller-Destination-Number',
				 kwargs.get('Caller-Caller-ID-Number', ''))))
				context['session_uuid'] = context['a_leg_uuid']
				context['b_leg_uuid']   = context['a_leg_uuid']
				context['a_leg_uuid']   = context['b_leg_uuid']
			pool.submit(event_dump,context)
		else:
			if kwargs.get('variable_usertype') in ["conference_client","wfh-agent-req-dial","ctc_agent"]:
				trunk_id = str(kwargs.get('variable_trunk_id', ''))
				chennals = pickle.loads(settings.R_SERVER.get("trunk_status") or pickle.dumps({}))
				if trunk_id in chennals:
					chennals[trunk_id] -= 1
					if chennals[trunk_id] >=0:
						settings.R_SERVER.set("trunk_status", pickle.dumps(chennals))
			if kwargs.get('variable_usertype') == "wfh_agent":
				dialed_string = kwargs.get('variable_channel_name',kwargs.get('Channel-Name'))
				destination_number = kwargs.get('Caller-Caller-ID-Number',kwargs.get('Caller-Orig-Caller-ID-Numberv'))
				dial_string1 = str(dialed_string).replace('internal/'+str(destination_number),'external/${destination_number}')
				dial_trunk = DialTrunk.objects.filter(dial_string=dial_string1)
				TRUNK = pickle.loads(settings.R_SERVER.get("trunk_status") or pickle.dumps({}))
				if dial_trunk.exists():
					for trunk in dial_trunk:
						if trunk.status=='Active' and str(trunk.id) in TRUNK:
							TRUNK[str(trunk.id)]  -= 1
							settings.R_SERVER.set("trunk_status", pickle.dumps(TRUNK))
							break
			return
	except Exception as e:
		print("error from capture_events ",e)
	
for sig in ['CHANNEL_HANGUP_COMPLETE']:
	louie.connect(capture_events, signal=sig)
