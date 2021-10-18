"""
Receiving signals for events.
"""
import louie
from scripts.eventdump import custom_dump,wfh_agent_login,dial_next_number
from concurrent.futures import ThreadPoolExecutor
dispo_pool = ThreadPoolExecutor(max_workers=20)

def custom_event(signal, sender, **kwargs):
	""" Custom events of the wfh"""
	if signal == 'CUSTOM::LOGIN':
		dialed_string = kwargs.get('variable_channel_name',kwargs.get('Channel-Name'))
		destination_number = kwargs.get('Caller-Caller-ID-Number',kwargs.get('Caller-Orig-Caller-ID-Numberv'))
		data={'customer_number':kwargs.get('Caller-Caller-ID-Number',None)[-10:],'sip_server':kwargs.get('variable_sip_req_host',kwargs.get('FreeSWITCH-IPv4', None)),
		'session_uuid':kwargs.get('Unique-ID',None),'extension':kwargs.get('variable_cc_agent',None),'campaign':kwargs.get('variable_campaign',None),
		'phonebook':kwargs.get('variable_phonebook',None),'contact_id':kwargs.get('variable_contact_id',None), 'destination_number':destination_number, 'dialed_string':dialed_string}
		dispo_pool.submit(wfh_agent_login, **data)
	elif signal == 'CUSTOM::DIAL-NEXT-NUMBER':
		data={'customer_number':kwargs.get('Caller-Caller-ID-Number',None)[-10:],'sip_server':kwargs.get('variable_sip_req_host',kwargs.get('FreeSWITCH-IPv4', None)),
		'session_uuid':kwargs.get('Unique-ID',None),'extension':kwargs.get('variable_cc_agent',None),'campaign':kwargs.get('variable_campaign',None)}
		dispo_pool.submit(dial_next_number, **data)
	elif signal == 'CUSTOM::WFH-REQ-CALLBACK':
		dialed_string = kwargs.get('variable_channel_name',kwargs.get('Channel-Name'))
		destination_number = kwargs.get('Caller-Caller-ID-Number',kwargs.get('Caller-Orig-Caller-ID-Numberv'))
		data={'customer_number':kwargs.get('Caller-Caller-ID-Number',None)[-10:],'sip_server':kwargs.get('variable_sip_req_host',kwargs.get('FreeSWITCH-IPv4', None)),
		'session_uuid':kwargs.get('Unique-ID',None),'extension':kwargs.get('variable_cc_agent',None),'campaign':kwargs.get('variable_campaign',None),
		'phonebook':kwargs.get('variable_phonebook',None),'contact_id':kwargs.get('variable_contact_id',None),'wfh_agent_req_dial':True,'destination_number':destination_number, 'dialed_string':dialed_string}
		dispo_pool.submit(wfh_agent_login, **data)		
	else:
		dispo_pool.submit(custom_dump,
				kwargs.get('variable_cc_queue', kwargs.get('variable_campaign', None)),
				kwargs.get('variable_cc_agent', None),
				kwargs.get('dispo_code', None),
				kwargs.get('variable_last_bridge_to', kwargs.get('variable_bridge_uuid', kwargs.get('variable_b_uuid',None))),
				kwargs.get('Event-Subclass', None),
				'Freeswitch',
				kwargs.get('Event-Date-Local', None),
				)
for sig in ['CUSTOM::DISPOSITION','CUSTOM::LOGIN','CUSTOM::DIAL-NEXT-NUMBER','CUSTOM::WFH-REQ-CALLBACK']:
	louie.connect(custom_event, signal=sig)

