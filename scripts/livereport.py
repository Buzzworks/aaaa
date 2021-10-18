import pickle
import datetime
from datetime import datetime, timedelta
from flexydial.settings import R_SERVER as r_server, WEB_LIVE_STATUS_CHANNEL as web_live_status,MEDIA_ROOT
from dialer.dialersession import autodial_session_hangup,play_fake_ring_agent
import os
from callcenter.models import UserVariable,CallDetail,Campaign
from callcenter.utility import create_agentactivity
from django.db.models import Sum
from django.db.models.functions import Coalesce

AGENTS = {}
class liveAgent:
	""" 
		Updating the redis agent data for live call reports in both application 
		and work from home features 
	"""
	def __init__(self):
		self.AGENTS = pickle.loads(r_server.get("agent_status") or
				pickle.dumps(AGENTS))

	def fake_ring_main(self, **kwargs):
		context={'campaign_name':kwargs.get('variable_campaign_name',None),'agent_unique_id':kwargs.get('variable_agent-Unique-ID',None),'play_status':kwargs.get('play_status','stop'),'Unique-ID':kwargs.get('Unique-ID',None)}
		context['fake_ring'] = kwargs.get('variable_fake_ring','false')
		fs_server = kwargs.get('FreeSWITCH-IPv4',None)
		if context['campaign_name']:
			campaign_obj = Campaign.objects.filter(name=context['campaign_name'])
			if campaign_obj:
				fs_server = campaign_obj[0].switch.ip_address
		play_fake_ring_agent(fs_server,**context)

	def  agentStatusUpdate(self, signal, **kwargs):
		if ( signal == 'CHANNEL_PROGRESS_MEDIA'):
			if kwargs['variable_call_mode'] not in ['predictive','Inbound','Blended']:
				kwargs['play_status'] = 'dnp'
				self.fake_ring_main(**kwargs)
		elif ( signal == 'CHANNEL_PROGRESS'):
			if 'variable_fake_ring' not in kwargs:
				if kwargs['variable_call_mode'] not in ['predictive','Inbound','Blended']:
					kwargs['play_status'] = 'play'
					self.fake_ring_main(**kwargs)
		elif ( signal == 'CHANNEL_ANSWER' ):
			if 'variable_call_mode' in kwargs and kwargs['variable_call_mode']!='predictive':
				if kwargs.get('variable_fake_ring',None) == 'true':
					kwargs['play_status'] = 'stop'
					self.fake_ring_main(**kwargs)
				agent = kwargs.get('variable_cc_agent', kwargs.get('Caller-Caller-ID-Number'))
				if agent in self.AGENTS:
					print(kwargs.get('Event-Date-Timestamp', None)[:13],'-----',kwargs.get('variable_cc_agent'),'----', kwargs.get('Caller-Caller-ID-Number'))
					self.AGENTS[agent].update({'call_timestamp':kwargs.get('Event-Date-Timestamp', None)[:13]})
					r_server.set("agent_status", pickle.dumps(self. AGENTS))
		elif (signal == 'CHANNEL_HANGUP'):
				try:
					if kwargs.get('variable_fake_ring',None) == 'true':
						kwargs['play_status'] = 'stop'
						self.fake_ring_main(**kwargs)
					agent = kwargs.get('variable_cc_agent', kwargs.get('Caller-Caller-ID-Number'))
					if agent in self.AGENTS:
						self.AGENTS[agent].update({'call_timestamp':''})
						self.AGENTS[agent].update({'state':'Feedback'})
						self.AGENTS[agent].update({'event_time':datetime.now().strftime('%H:%M:%S')})
						self.AGENTS[agent].update({'call_type':''})
						r_server.set("agent_status", pickle.dumps(self.AGENTS))
				except Exception as e:
					print("error from liveAgent,CHANNEL_HANGUP",e)
					pass
		elif (signal == 'CHANNEL_HANGUP_COMPLETE'):
			try:
				agent = kwargs.get('variable_cc_agent', kwargs.get('Caller-Caller-ID-Number'))
				if agent in self.AGENTS:
					self.AGENTS[agent].update({'call_timestamp':''})
					r_server.set("agent_status", pickle.dumps(self.AGENTS))
			except Exception as e:
				print("error from liveAgent,CHANNEL_HANGUP_COMPLETE",e)
				pass
		elif (signal == 'SHUTDOWN'):
			try:
				r_server.delete("agent_status")
			except (ValueError, KeyError):
				pass
	def wfh_agentStatusUpdate(self, signal, **kwargs):
		try:
			if signal == 'CHANNEL_HANGUP' or signal == 'CHANNEL_HANGUP_COMPLETE':
				agent = kwargs.get('variable_cc_agent', kwargs.get('Caller-Caller-ID-Number'))
				if agent in self.AGENTS:
					user_id = None
					activity_dict = {}
					login_time = datetime.combine(datetime.now(), datetime.strptime(self.AGENTS[agent]['dialer_login_time'],'%H:%M:%S').time())

					user = UserVariable.objects.filter(extension=agent)
					if user.exists():
						user_id = user.first().user_id
					call_duration = CallDetail.objects.filter(user_id=user_id,created__gte=login_time, created__lte=datetime.now()).aggregate(call_duration=Coalesce(Sum('call_duration'),timedelta(seconds=0)))
					tos = datetime.now().replace(microsecond=0) - login_time
					idle_time = tos - call_duration['call_duration']
					activity_dict["user_id"] = user_id
					activity_dict["event"] = "WFH AGENT LOGOUT"
					activity_dict["event_time"] = datetime.now()
					activity_dict["campaign_name"] = self.AGENTS[agent]['campaign']
					activity_dict["break_type"] = None
					activity_dict["tos"] = str(tos)
					activity_dict["idle_time"] = str(idle_time)
					activity_dict["spoke_time"] = str(call_duration['call_duration'])
					create_agentactivity(activity_dict)
					del self.AGENTS[agent]
					r_server.set("agent_status", pickle.dumps(self.AGENTS))
					autodial_session_hangup(kwargs.get('variable_sip_req_host'),extension=agent)
					session_uuid = kwargs.get('Unique-ID')
					os.system('echo %s|sudo -S %s' % ('flexydial', 'rm -r '+MEDIA_ROOT+'/'+session_uuid+'.mp3'))
					# os.system('echo %s|sudo -S %s' % ('flexydial', 'rm -r '+MEDIA_ROOT+'/'+session_uuid+'.wav'))
		except Exception as e:
			print("error from liveAgent,wfh-CHANNEL_HANGUP",e)
			pass	