"""
Dumping Events in DB or Logger
"""
import json
import time,os, sys
from subprocess import PIPE, Popen, call
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, connection, connections
from datetime import datetime,date,timedelta

import requests
from flexydial import settings
from flexydial.views import sendsmsparam
from callcenter.models import (
	SMSTemplate,
	User,
	UserVariable,
	Campaign,
	CallDetail,DiallerEventLog,
	CallBackContact,Notification,Abandonedcall,
	StickyAgent,
	CdrFeedbck,
	VoiceBlaster
	)
from dialer.dialersession import enable_wfh_user,wfh_progressive_call,get_calltype_state
from crm.models import (Contact,)
from django.db.models import Q, F
from django.apps import apps
from callcenter.utility import format_time, PasswordChangeAndLockedReminder, get_agent_status, set_agent_status
import inspect
import pickle
import csv
import uuid
import pandas as pd
import os.path
import datetime
import logging
logger = logging.getLogger(__name__)
wfh_agents={}


def wfh_agent_login(**kwargs):
	""" enable work from home login"""
	try:
		status = enable_wfh_user(kwargs['sip_server'],**kwargs)
	except Exception as e:
		print("error from wfh_agent_login",e)
	finally:
		transaction.commit()
		connections["default"].close()
		
def dial_next_number(**kwargs):
	""" work form home dial next number """
	try:
		wfh_progressive_call(kwargs['sip_server'],**kwargs)
	except Exception as e:
		print("error from dial_next_number",e)
	finally:
		transaction.commit()
		connections["default"].close()
		connections["crm"].close()		

def custom_dump(campaign, user, dispo_code, uuid, name, e_type, created):
	""" dumping the custom reports into the database """
	try:
		cdr = CdrFeedbck.objects.none()
		primary_disposition = 'NF(No Feedback)'
		for x in range(10):
			try:
				cdr = CdrFeedbck.objects.get(session_uuid=uuid)
				if cdr:
					break
			except (ObjectDoesNotExist,):
				time.sleep(1)
		if cdr:
			dispo_code = dispo_code.split(':')
			if dispo_code[0]:
				try:
					campaign_obj = Campaign.objects.get(name=campaign)
				except Exception:
					campaign_obj = None
				dispo_code = dispo_code[0]
				if len(dispo_code) > 1:
					dispo_code = dispo_code[0][0]
				if campaign_obj:
					call_type, state = get_calltype_state(campaign_obj.dial_method)
					if user is not None or user != '':
						try:
							username = UserVariable.objects.get(extension=user).user.username
						except:
							username = ''
					else:
						username = ''
					AGENTS = get_agent_status(username)
					if username in AGENTS and AGENTS[username]['wfh']:
						AGENTS[username]['call_type'] = call_type
						AGENTS[username]['state'] = state
						set_agent_status(username,AGENTS[username])
					if dispo_code in campaign_obj.wfh_dispo:
						primary_disposition = campaign_obj.wfh_dispo[dispo_code]
				if primary_disposition=='CallBack':
					# next_callback_time = datetime.now()+ timedelta(hours=24)
					next_callback_time = datetime.now()+ timedelta(hours=5,minutes=30)
					CallBackContact.objects.create(numeric = cdr.calldetail.customer_cid,campaign = campaign,disposition=primary_disposition,
					 callback_type = 'queue',phonebook = cdr.calldetail.phonebook, schedule_time = next_callback_time,status = 'NotDialed',customer_raw_data={},
					 contact_id=cdr.contact_id, callmode=cdr.calldetail.callmode)
			cdr.primary_dispo = primary_disposition
			cdr.save()
		else:
			try:
				calldetail = CallDetail.objects.get(session_uuid=uuid)
				contact_id = calldetail.contact_id
			except Exception as e:
				print("error from custom_dump",e)
				calldetail = None
				contact_id = None
			cdr = CdrFeedbck.objects.create(session_uuid = uuid,primary_dispo=primary_disposition,
				feedback ={}, relation_tag=[], calldetail=calldetail, contact_id=contact_id)
		if cdr.contact_id:
			Contact.objects.filter(id=cdr.contact_id).update(status='Dialed', disposition=primary_disposition)
	except Exception as e:
		print("error from custom_dump",e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	finally:
		transaction.commit()
		connections["crm"].close()
		connections["default"].close()

def event_dump(kwargs):
	""" dumping the events into the database for generating reports"""
	for i in range(3):
		try:
			wfh = False
			username=None
			campaign_name = None
			if kwargs.get('campaign') is not None or kwargs.get('campaign') != '':
				try:
					campaign_obj = Campaign.objects.get(slug=kwargs.get('campaign'))
					wfh=campaign_obj.wfh
					campaign_name = campaign_obj.name
				except:
					campaign_name = None
					campaign_obj = None
			else:
				campaign_obj = None
			if kwargs.get('user') is not None or kwargs.get('user') != '':
				try:
					user_obj = UserVariable.objects.get(extension=kwargs.get('user')).user
					username = user_obj.username
				except:
					user_obj = User.objects.filter(caller_id = kwargs.get('caller_id')).first()
					if user_obj:
						username = user_obj.username
					else:
						user_obj = None
			else:
				print('2222')
				user_obj = User.objects.filter(caller_id = kwargs.get('caller_id')).first()
				if user_obj:
					username = user_obj.username
				else:
					user_obj = None
			primary_dispo='NF(No Feedback)'
			list_causecode = ["USER_BUSY","NO_ANSWER","NO_USER_RESPONSE","NORMAL_CLEARING","NORMAL_TEMPORARY_FAILURE","CALL_REJECTED","ORIGINATOR_CANCEL"]			
			models=['DiallerEventLog']
			if kwargs.get('dialed_status') != 'Connected':
				if kwargs.get('callflow') != 'inbound':
					if kwargs.get('hangup_cause', '') in list_causecode:
						if kwargs.get('hangup_cause', '') != "NORMAL_CLEARING":
							kwargs['dialed_status'] = 'NC'
							if kwargs.get('call_mode', '') == 'predictive':
								models=['CallDetail','DiallerEventLog']						
						else:
							if kwargs.get('call_mode', '') != 'predictive':
								kwargs['dialed_status'] = 'NC'
							else:
								models=['CallDetail','DiallerEventLog']
								if kwargs.get('dialed_status') == 'CBR':
									CallBackContact.objects.create(numeric = kwargs.get('customer_cid'),campaign = kwargs.get('campaign'),disposition = kwargs.get('dialed_status'),callback_type = 'queue',schedule_time = datetime.now(),status = 'NotDialed',customer_raw_data={},contact_id=kwargs["contact_id"], callmode=kwargs.get('call_mode', ''))								
								else:
									kwargs['dialed_status'] = 'Drop'
				else:
					models=['CallDetail','DiallerEventLog']
					ivr_duration = kwargs.get('billsec', None)
					bill_sec = 0
					inbound_uuids = pickle.loads(settings.R_SERVER.get("inbound_status") or pickle.dumps(AGENTS))
					if kwargs['session_uuid'] in inbound_uuids:
						del inbound_uuids[kwargs['session_uuid']]
						settings.R_SERVER.set("inbound_status", pickle.dumps(inbound_uuids))
					if kwargs.get('dialed_status') == 'CBR':
						CallBackContact.objects.create(numeric = kwargs.get('customer_cid'),campaign = kwargs.get('campaign'),disposition = kwargs.get('dialed_status'),callback_type = 'queue',schedule_time = datetime.now(),status = 'NotDialed',customer_raw_data={},contact_id=kwargs["contact_id"], callmode=kwargs.get('call_mode', ''))					
					else:
						message = "Dear Agent you have a Call Back Request from this number {}".format(kwargs.get('customer_cid'))
						abandoned_obj = Abandonedcall.objects.create(campaign=kwargs.get('campaign'),caller_id=kwargs.get('caller_id'),numeric = kwargs.get('customer_cid'), status =kwargs.get('dialed_status'))
						notification_obj = Notification.objects.create(campaign=kwargs.get('campaign'),title='Abandonedcall', 					
							message=message,numeric = kwargs.get('customer_cid'))
						if user_obj == None:
							notification_obj.notification_type = "campaign_abandonedcall"
						else:
							notification_obj.notification_type = "user_abandonedcall"
							notification_obj.user=user_obj.username
							abandoned_obj.user = user_obj.username
							abandoned_obj.save()
							contact = Contact.objects.filter(numeric=kwargs.get('customer_cid')).order_by('-id').first()
							if contact:
								campaign_obj_sms =  Campaign.objects.filter(name=contact.campaign).first()
							if contact and campaign_obj_sms and campaign_obj_sms.sms_gateway and campaign_obj_sms.sms_gateway.status == "Active":
								trigger_params = campaign_obj_sms.sms_gateway.trigger_params
								if trigger_params:
									trigger_types = list(trigger_params.keys())
									if '3' in trigger_types:
										sms_template = SMSTemplate.objects.filter(id__in=trigger_params['3'],status="Active").values('id','text')
										numeric = kwargs.get('customer_cid','')
										session_uuid = kwargs.get('session_uuid','')
										try:
											web_url = settings.WEB_URL
											if not web_url: #contact_id, campaign_obj, user_obj, primary_disp='aban'.
												primary_dispo='aban'
												contact_obj=str(kwargs.get('customer_cid'))
												sendsmsparam(campaign_obj_sms,numeric,session_uuid,sms_template,user_obj,primary_dispo,contact_obj)
											else:
												res = requests.post(f"{web_url}/api/send_sms/",data={"campaign_id":campaign_obj_sms.id,"numeric":numeric,"abd_trigger":"true","session_uuid":session_uuid,"templates":json.dumps(list(sms_template))},verify=False)
												print("SENDSMS RES",res)
										except Exception as e:
											print("sendSMS exception",e)
						notification_obj.save()
			if wfh:
				wfh_agents = {}
				AGENTS = get_agent_status(username)
				if username in AGENTS and AGENTS[username]['wfh'] or kwargs.get('wfh_call'):
					models=['CallDetail','DiallerEventLog']
				wfh_agents = pickle.loads(settings.R_SERVER.get("wfh_agents") or pickle.dumps(wfh_agents))
				if wfh_agents and kwargs.get('session_uuid') in wfh_agents:
					del wfh_agents[kwargs.get('session_uuid')]
					settings.R_SERVER.set("wfh_agents",pickle.dumps(wfh_agents))
			if kwargs.get('call_mode') == 'click-to-call' or kwargs.get('call_mode') == "voice-blaster":
					models=['CallDetail','DiallerEventLog']
					if kwargs.get('call_mode') == "voice-blaster" and kwargs.get('dialed_status')=="Connected":
						vb_info = VoiceBlaster.objects.filter(campaign=campaign_obj.id).first()
						audio_duration = int(vb_info.vb_data['vb_audio_duration'])
						talk_time = int(kwargs.get('bill_sec'))
						if talk_time >= audio_duration:
							kwargs['dialed_status']="Full Audio Played"
						else:
							kwargs['dialed_status']="Not Played Full Audio"	
						if kwargs.get('dtmf') != None and  kwargs.get('dtmf') in vb_info.vb_data['vb_dtmf'].keys():
							primary_dispo = vb_info.vb_data['vb_dtmf'][kwargs.get('dtmf')]['dispo']
							if vb_info.vb_data['vb_dtmf'][kwargs.get('dtmf')]['is_sms']:
								try: 
									if vb_info.campaign.exists():
										for camp in vb_info.campaign.all():
											if camp.sms_gateway and camp.name == campaign_name:
												message = camp.sms_gateway.template.values('text','id')
												numeric = kwargs.get('customer_cid')
												session_uuid = kwargs.get('session_uuid')
												sendsmsparam(camp,numeric,session_uuid,message)
								except Exception as e:
									print(e)
			if kwargs.get('usertype') == 'client_ipphone':
				if kwargs.get('hangup_cause', '') in list_causecode:
					if kwargs.get('hangup_cause', '') != "NORMAL_CLEARING":
						kwargs['dialed_status'] = 'NC'	
				models=['CallDetail','DiallerEventLog']
			if kwargs.get('contact_id') is not None or kwargs.get('contact_id') != '':
				if kwargs.get('dialed_status') != 'Connected' and kwargs.get('call_mode') in ["voice-blaster","predictive"]:
					status = kwargs.get('dialed_status','Dialed')
					if kwargs.get('dialed_status') in ['Full Audio Played','Not Played Full Audio']:
						status = 'Dialed'
					Contact.objects.filter(id = kwargs.get('contact_id')).update(status =status, disposition=primary_dispo, dial_count=F('dial_count')+1, last_dialed_date =kwargs.get('init_time', None))
			print(kwargs)
			for model in models:
				model = apps.get_model(app_label='callcenter', model_name=model)
				cdr_save(model,kwargs,campaign_obj,user_obj,primary_dispo, campaign_name)
			break
		except Exception as e:
			logger.debug("erro from event_dump : %s"%(e))
			time.sleep(1)
			if (e.__class__.__name__ == 'InterfaceError' or e == 'connection already closed') and i==2 :
				missing_report(kwargs,e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			logger.debug("%s , %s , %s" %(exc_type, fname, exc_tb.tb_lineno))
		finally:
			transaction.commit()
			connections["crm"].close()
			connections["default"].close()


def missing_report(kwargs,e):
	try:
		download_folder = settings.MEDIA_ROOT+"/upload/"+"missingreports.csv" 
		dic=kwargs             
		s=uuid.UUID(dic['session_uuid']).hex
		session_uuid=uuid.UUID(s)
		session_id=dic['session_uuid']
		if DiallerEventLog.objects.filter(session_uuid=session_uuid).exists(): 
			file_exists = os.path.isfile(download_folder)
			with open(download_folder, 'a') as f:
				headers=['customer_cid','usertype','contact_id','campaign','user','phonebook','session_uuid','a_leg_uuid','b_leg_uuid','init_time','ring_time','connect_time','wait_time','hold_time','media_time',
				'callflow','call_mode','destination_extension','transfer_history','call_duration','bill_sec','ivr_duration','hangup_time','hangup_cause','hangup_cause_code','channel','dialed_status','info','dtmf','caller_id','unique_id','wfh_call','callserver']
				writer = csv.DictWriter(f, delimiter=',', lineterminator='\n',fieldnames=headers)
				if not file_exists:
					writer.writeheader()
				else:
					writer.writerow(dic)
			call_detail_data = pd.read_csv(download_folder,na_filter=False)  
			call_detail_data=call_detail_data.drop_duplicates()
			campaign = Campaign.objects.filter(name=kwargs.get('campaign')).first()
			user_obj = UserVariable.objects.filter(extension=kwargs.get('user')).first()
			username = User.objects.filter(username=user_obj.user.username).first()
			init_time=kwargs.get('init_time')
			ring_time=kwargs.get('ring_time')
			connect_time=kwargs.get('connect_time')
			wait_time=kwargs.get('wait_time')
			hold_time=kwargs.get('hold_time')
			media_time=kwargs.get('media_time')
			call_duration=kwargs.get('call_duration')
			bill_sec=kwargs.get('bill_sec')
			ivr_duration=kwargs.get('ivr_duration')
			for index, row in call_detail_data.iterrows():	
				dialler_event_dict = {}
				dialler_event_dict["customer_cid"] = row["customer_cid"]
				dialler_event_dict["contact_id"] = row["contact_id"]
				dialler_event_dict["campaign"] = campaign
				dialler_event_dict["user"] = username
				dialler_event_dict["phonebook"] = row["phonebook"]
				dialler_event_dict["session_uuid"] = row['session_uuid']
				dialler_event_dict["a_leg_uuid"] = row["a_leg_uuid"]
				dialler_event_dict["b_leg_uuid"] = row["b_leg_uuid"]
				dialler_event_dict["init_time"] = format_time(init_time)
				dialler_event_dict["ring_time"] = format_time(ring_time)
				if row["connect_time"]:
					dialler_event_dict["connect_time"] = format_time(connect_time)
				if row["wait_time"]:
					dialler_event_dict["wait_time"] = format_time(wait_time)
				if row["hold_time"]:
					dialler_event_dict["hold_time"] =format_time(hold_time)
				if row["media_time"]:
					dialler_event_dict["media_time"] = format_time(media_time)
				dialler_event_dict["callflow"]=row["callflow"]
				dialler_event_dict["callmode"]=row["call_mode"]
				dialler_event_dict["destination_extension"]=row["destination_extension"]
				dialler_event_dict["transfer_history"]=row["transfer_history"]
				dialler_event_dict["bill_sec"] =  time.strftime('%H:%M:%S',time.gmtime(int(kwargs.get('bill_sec'))))
				dialler_event_dict["call_duration"] = time.strftime('%H:%M:%S',time.gmtime(int(kwargs.get('call_duration'))))
				dialler_event_dict["ivr_duration"] = time.strftime('%H:%M:%S',time.gmtime(int(kwargs.get('ivr_duration'))))
				dialler_event_dict["hangup_time"] = row["hangup_time"]
				dialler_event_dict["hangup_cause"] = row["hangup_cause"]
				dialler_event_dict["hangup_cause_code"] = row["hangup_cause_code"]
				dialler_event_dict["channel"] = row["channel"]
				dialler_event_dict["dialed_status"] = row["dialed_status"]
				dialler_event_dict["info"] = row["info"]
				dialler_event_dict["uniqueid"] = row["unique_id"]
				dialler_event_dict["callserver"] = row["callserver"]
				DiallerEventLog.objects.create(**dialler_event_dict)
				indexdrop = call_detail_data[ (call_detail_data['session_uuid'] == session_id)].index
				call_detail_data.drop(indexdrop , inplace=True)
				call_detail_data.to_csv(download_folder,index=False, mode='w')
	except Exception as e:
		logger.debug("erro from missing_report : %s"%(e))


def cdr_save(model,kwargs,campaign_obj,user_obj,primary_dispo, campaign_name):
	""" saving the reports into the database thats has been dumped"""
	for i in range(3):
		try:
			cdr = model(
					contact_id = kwargs.get('contact_id'),
					campaign_name = campaign_name,
					user=user_obj,
					phonebook=kwargs.get('phonebook'),
					session_uuid=kwargs.get('session_uuid'),
					a_leg_uuid=kwargs.get('a_leg_uuid'),
					b_leg_uuid=kwargs.get('b_leg_uuid'),
					init_time=kwargs.get('init_time'),
					ring_time=kwargs.get('ring_time'),
					connect_time=kwargs.get('connect_time'),
					wait_time=time.strftime('%H:%M:%S', time.gmtime(int(kwargs.get('wait_time')))),
					hold_time=time.strftime('%H:%M:%S', time.gmtime(int(kwargs.get('hold_time')))),
					media_time=time.strftime('%H:%M:%S', time.gmtime(int(kwargs.get('media_time')))),
					callflow=kwargs.get('callflow', ''),
					callmode=kwargs.get('call_mode', ''),
					customer_cid=kwargs.get('customer_cid')[-10:],
					destination_extension=kwargs.get('destination_extension'),
					call_duration=time.strftime('%H:%M:%S', time.gmtime(int(kwargs.get('call_duration')))),
					bill_sec=time.strftime('%H:%M:%S', time.gmtime(int(kwargs.get('bill_sec')))),
					ivr_duration=time.strftime('%H:%M:%S', time.gmtime(int(kwargs.get('ivr_duration')))),
					hangup_time=kwargs.get('hangup_time'),
					hangup_cause=kwargs.get('hangup_cause'),
					hangup_cause_code=kwargs.get('hangup_cause_code'),
					dialed_status=kwargs.get('dialed_status'),
					)
			if cdr.__class__.__name__== 'DiallerEventLog':
				cdr.callserver=kwargs.get('callserver')
			if cdr.__class__.__name__!='CallDetail':
				cdr.transfer_history=kwargs.get('transfer_history'),
				cdr.info=kwargs.get('info'),
				cdr.channel=kwargs.get('channel')
			else:
				cdr.hangup_source = 'System'
			cdr.uniqueid = kwargs.get('unique_id',None)
			formatted_connect_time = format_time(cdr.connect_time)
			formatted_hangup_time = format_time(cdr.hangup_time)
			formatted_ring_time = format_time(cdr.ring_time)
			if cdr.connect_time:
				if formatted_connect_time < formatted_ring_time:
					r_time = cdr.connect_time
					c_time = cdr.ring_time
					cdr.connect_time = c_time
					cdr.ring_time = r_time
					calculate_ring_duration = formatted_ring_time - formatted_connect_time	
				else:	
					calculate_ring_duration = formatted_connect_time - formatted_ring_time
			else:
				calculate_ring_duration = formatted_hangup_time - formatted_ring_time
			formatted_ring_duration = time.strftime('%H:%M:%S', time.gmtime(
						calculate_ring_duration.total_seconds()))
			cdr.ring_duration = formatted_ring_duration
			cdr.save()
			if cdr.__class__.__name__!='CallDetail' and kwargs.get('dialed_status') == 'Connected' and kwargs.get('call_mode') not in ["click-to-call",'voice-blaster'] :
				if user_obj and campaign_obj and campaign_obj.dial_method['sticky_agent_map'] and campaign_obj.dial_method['inbound']:
					StickyAgent.objects.create(numeric=kwargs.get('customer_cid'),campaign_name=campaign_name,agent=user_obj)
			if cdr.__class__.__name__=='CallDetail':
				if not CdrFeedbck.objects.filter(session_uuid=kwargs.get('session_uuid')).exists():
					CdrFeedbck.objects.create(primary_dispo = primary_dispo,session_uuid=kwargs.get('session_uuid'),
						contact_id=kwargs.get('contact_id'), feedback={}, relation_tag=[], calldetail=cdr)
			break
		except Exception as e:
			logger.debug("erro from cdr_save : %s"%(e))
			time.sleep(1)
		finally:
			transaction.commit()
			connections["crm"].close()
			connections["default"].close()
