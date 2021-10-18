import louie
from scripts.livereport import liveAgent
from django.conf import settings
import pickle
from crm.models import TempContactInfo

def liveStatus(signal, sender, **kwargs):
	""" capturing signal events and performing events"""
	if kwargs.get('variable_usertype') == "client":
		live_agent = liveAgent()
		live_agent.agentStatusUpdate(signal, **kwargs)
		print("signal is ",signal)
		if signal == 'CHANNEL_ORIGINATE':
			chennals = pickle.loads(settings.R_SERVER.get("trunk_status") or pickle.dumps({}))
			chennals[kwargs['variable_trunk_id']] += 1
			settings.R_SERVER.set("trunk_status", pickle.dumps(chennals))
			if kwargs['variable_call_mode'] in ['predictive', 'voice-blaster']:
				if 'variable_contact_id' in kwargs:
					TempContactInfo.objects.filter(contact_id=kwargs['variable_contact_id']).delete()
	elif signal == 'CHANNEL_HANGUP' or signal == 'CHANNEL_HANGUP_COMPLETE':
		if 'variable_wfh' in kwargs and kwargs.get('variable_wfh') == 'true':
			live_agent = liveAgent()
			live_agent.wfh_agentStatusUpdate(signal, **kwargs)
for sig in ['CHANNEL_ORIGINATE','CHANNEL_PROGRESS','CHANNEL_PROGRESS_MEDIA','CHANNEL_ANSWER','CHANNEL_BRIDGE', \
		 'CHANNEL_HANGUP','bridge-agent-start', 'bridge-agent-end', \
		'CHANNEL_HANGUP_COMPLETE']:
	louie.connect(liveStatus, signal=sig)