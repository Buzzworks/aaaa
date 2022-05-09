"""
Dumping Events in DB or Logger
"""
#from flexydial.scripts.pyfsm import FsFSM
import time,os, sys, glob, shutil
import dateutil
from subprocess import PIPE, Popen, call
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, connection, connections
from datetime import datetime,date,timedelta
from flexydial import settings,constants
from flexydial.views import sendsmsparam
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from callcenter.models import (
	User,
	UserVariable,
	Campaign,
	DiallerEventLog,
	CallDetail,
	LeadRecycle,
	CallBackContact,CurrentCallBack,Notification,Abandonedcall,BroadcastMessages,
	StickyAgent,
	CdrFeedbck,
	PhonebookBucketCampaign,
	VoiceBlaster
	)
from dialer.dialersession import enable_wfh_user,wfh_progressive_call,get_calltype_state
from crm.models import (Phonebook,DownloadReports,Contact,)
import inspect,json
from django.db.models import Q, F
from callcenter.schedulejobs import add_leadrecycle_db
from django.apps import apps
from callcenter.utility import format_time, PasswordChangeAndLockedReminder
import inspect
import pickle

wfh_agents={}
sched = BackgroundScheduler({
	"apscheduler.jobstores.default": {
		"class": "django_apscheduler.jobstores:DjangoJobStore"
	},
	'apscheduler.executors.default': {
		'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
		'max_workers': '20'
	},
	'apscheduler.executors.processpool': {
		'type': 'processpool',
		'max_workers': '8'
	},
	'apscheduler.job_defaults.coalesce': 'false',
	'apscheduler.job_defaults.max_instances': '5',
})

def callback_queue():
	"""
	This function is used for update the callback contacts into queue and send notifications.
	"""
	try:
		queue_callbacks = CallBackContact.objects.filter(Q(schedule_time__lte = datetime.now() + timedelta(minutes=5)
			)&Q(status = 'NotDialed'))
		if queue_callbacks:
			CallBackContact_list=[]
			CurrentCallBack_list=[]		
			for queue_call in queue_callbacks:
				if queue_call.callback_type == 'self' or queue_call.assigned_by:
					message = "Dear Agent you have callback call scheduled by {}".format(queue_call.assigned_by)
					noti_id = Notification.objects.create(campaign=queue_call.campaign,user=queue_call.user,title='callback',
						message=message,numeric=queue_call.numeric, contact_id=queue_call.contact_id)
				else:
					message ="Dear Agent you have a {} schedule call on {} to {}".format(queue_call.callback_type,queue_call.schedule_time,queue_call.numeric)
					noti_id = Notification.objects.create(campaign=queue_call.campaign,title='callback',message=message,numeric = queue_call.numeric,contact_id=queue_call.contact_id)

				CurrentCallBack_list.append(CurrentCallBack(campaign=queue_call.campaign,user=queue_call.user,numeric = queue_call.numeric,
						status ='NotDialed', contact_id =queue_call.contact_id, phonebook=queue_call.phonebook,callback_type=queue_call.callback_type,
						schedule_time=queue_call.schedule_time,disposition=queue_call.disposition,comment=queue_call.comment,
						callbackcontact_id=queue_call.id, notification_id=noti_id.id, callmode=queue_call.callmode))
				camp_obj = Campaign.objects.filter(name=queue_call.campaign).first()
				if camp_obj:
					if camp_obj.auto_qcb_dial:
						PhonebookBucketCampaign.objects.filter(id=camp_obj.id).update(is_contact=True)
				queue_call.status ='Queued'
			CurrentCallBack.objects.bulk_create(CurrentCallBack_list)
			CallBackContact.objects.bulk_update(queue_callbacks,['status'])
	except Exception as e:
		print(e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	finally:
		transaction.commit()
		connections["default"].close()

def update_leadrecycle_datetime():
	"""
	This function is used for update the lead recycle scheduletime for scheduling the lead into next day.
	"""	
	try:
		leads =  LeadRecycle.objects.filter(Q(status='Active')&Q(schedule_type='schedule_time')&Q(ldr_period_update__lt=datetime.date(datetime.now())))
		if leads:
			for lead in leads:
				schedule_period= json.loads(lead.schedule_period)
				if schedule_period["start_time"] != "" and schedule_period["end_time"] !="":
					start_datetime  = date.today().strftime('%Y-%m-%d')+' '+schedule_period["start_time"]+':00'
					end_datetime = date.today().strftime('%Y-%m-%d')+' '+schedule_period["end_time"]+':00'
					str_datetime_obj = datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')-timedelta(hours=5,minutes=30)
					end_datetime_obj = datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S')-timedelta(hours=5,minutes=30)
					job_id = str(lead.campaign)+'_'+str(lead.id)
					args=[str(lead.campaign),lead.name]			
					sched.add_job(add_leadrecycle_db, 'interval',args=args, seconds=lead.recycle_time, start_date=str(str_datetime_obj),
					end_date=str(end_datetime_obj), id =job_id)
			leads.update(ldr_period_update=datetime.date(datetime.now()))
	except Exception as e:
		print(e)
	finally:
		transaction.commit()
		connections['default'].close()

def dump_database(host_name, db_name, user_name, db_password, backup_path='/var/lib/postgresql/'):
	""" dumping the data into the folder for backup"""
	try:
		backup_date = time.strftime('%Y-%m-%d')
		command = 'PGPASSWORD={5} pg_dump -h {0} -U {1} {2} | gzip > {3}{4}_{2}_backup.gz'.format(host_name, user_name, db_name, backup_path, backup_date,db_password)
		p = Popen(command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)
		#p.communicate(bytes(db_password,'utf-8'))
		return 
	except Exception as e:
		print(e)

def dump_contact(file_path):
	""" dumping the contact into the folder for backup"""
	command = 'PGPASSWORD=flexydial pg_dump -h localhost -U flexydial --column-inserts --data-only -t crm_contact crm > {}'.format(file_path)
	p = Popen(command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)
	
def delete_all_downloads():
	""" deleting all the downloads after one day"""
	try:
		last_date = datetime.now() - timedelta(days=1)
		reports = DownloadReports.objects.filter(start_date__date__lte=last_date.date())
		for report in reports:
			report.downloaded_file.delete(save=False)
			report.delete()
	except Exception as e:
		print(e,"delete_all_downloads error")

def delete_lead_priority_after_period():
	""" deleting the lead priority after the specific time """
	try:
		campaigns=Campaign.objects.filter().exclude(lead_priotize={})
		if campaigns.exists():
			for campaign in campaigns:
				key = ''
				for keys in campaign.lead_priotize.keys():
					key = str(keys)
				if 'tapd' in campaign.lead_priotize[key]:
					current_date = datetime.now()
					period = timedelta(days=1)
					if 'weekly' in campaign.lead_priotize[key]['period']:
						period = 7
					if 'monthly' in campaign.lead_priotize[key]['period']:
						period = 30
					last_date = current_date - period
					LeadListPriority.objects.filter(campaign_id=campaign.id,created_date__date__lte=last_date.date()).delete()
	except Exception as e:
		print(e,"delete_lead_priority_after_period error")
		
def restart_all_services():
	""" restarting all the services """
	try:
		freeswitch_cmd = 'sudo service freeswitch restart'
		cdrd_cmd = 'sudo service flexydial-cdrd restart'
		autodial_cmd = 'sudo service flexydial-autodial restart'
		dialplan_cmd = 'sudo service flexydial-fs-dialplan restart'
		event_zmq = 'fs_cli -x "reload mod_event_zmq"'
		xml_rpc ='fs_cli -x "reload  mod_xml_rpc"'
		xml_curl ='fs_cli -x "reload  mod_xml_curl"'
		freeswitch_status = call(freeswitch_cmd, shell=True)
		print("services Re-starting................")
		if freeswitch_status == 0:
				event_zmq_status = call(event_zmq, shell=True)
				xml_rpc_status = call(xml_rpc, shell=True)
				xml_curl_status = call(xml_curl, shell=True)
				cdrd_status = call(cdrd_cmd, shell=True)
				autodial_status = call(autodial_cmd, shell=True)
				dialplan_status = call(dialplan_cmd, shell=True)
		else:
				print("Error Re-starting freeswitch !...........")
	except Exception as e:
		print(e,"restart_all_services error")

def reset_Redisdata():
	""" resetting the redis data keys"""
	try:
		settings.R_SERVER.set("agent_status", pickle.dumps({}))
		settings.R_SERVER.set("campaign_status", pickle.dumps({}))
		settings.R_SERVER.set("inbound_status", pickle.dumps({}))
		settings.R_SERVER.set("transfer_agents",{})
		settings.R_SERVER.set("wfh_agents",pickle.dumps({}))
		settings.R_SERVER.set("trunk_status", pickle.dumps({}))
		settings.R_SERVER.set("phonebook", pickle.dumps({}))
		settings.R_SERVER.set("download", pickle.dumps({}))
		campaign = Campaign.objects.values('id','name')
		for camp in campaign:
			settings.R_SERVER.hset("ad_campaign_status",camp['name'], True)
			settings.R_SERVER.hset("pb_campaign_status",camp['id'], True)
		PhonebookBucketCampaign.objects.filter().update(agent_login_count=0)
	except Exception as e:
		print('Error in reset_Redisdata',e)

def sagregate_recording_file():
	""" segregatting the recording files into the folder"""
	yesterday_date = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
	parent_dir = '/var/spool/freeswitch/default'
	recording_dir_path = os.path.join(parent_dir, yesterday_date)
	if not os.path.exists(recording_dir_path):
		os.makedirs(recording_dir_path,0o777)
	files = glob.glob(recording_dir_path+'-*')
	for file in files:
		shutil.move(file, recording_dir_path)
	print('recording move to recording date directory')
	

def delete_one_month_ago_file():
	"""
	This function is used to delete
	"""
	now = datetime.now()
	month_back = now + dateutil.relativedelta.relativedelta(months=-1)
	month_back_date = month_back.date().strftime("%m.%d.%Y")
	download_folder = settings.MEDIA_ROOT+"/download/"+month_back_date
	contact_folder = settings.MEDIA_ROOT+"/contact_backup/"+month_back_date
	if os.path.exists(download_folder):
		shutil.rmtree(download_folder)	
	if os.path.exists(contact_folder):
		shutil.rmtree(contact_folder)	

def sticky_agent_delete():
	"""
	This function is used for delete sticky agent entry for more than 7 days
	"""
	try:
		last_date = datetime.now() - timedelta(days=7)
		StickyAgent.objects.filter(created__date__lte=last_date.date()).delete()
		Notification.objects.filter(created_date__date__lte=last_date.date()).delete()
		BroadcastMessages.objects.filter(created__lte=last_date.date()).delete()
		print('<----------------- DB Backup Start ------------------->')
		db_backup_path = '/usr/local/src/db_backup/'
		dump_database('localhost','flexydial','flexydial','flexydial',db_backup_path)
		dump_database('localhost','crm','flexydial','flexydial',db_backup_path)
		print('<----------------- DB Backup Complete ------------------->')
		delete_all_downloads()
		delete_lead_priority_after_period()
		reset_Redisdata()
		sagregate_recording_file()
		delete_one_month_ago_file()
		# restart_all_services()
		# app.logger.info("Starting database backup at: " + backup_date)
	except Exception as e:
		print(e)
	finally:
		transaction.commit()
		connections["crm"].close()
		connections["default"].close()
		
connected = False
while not connected:
	try:
		sched.add_job(callback_queue, "interval", seconds=15, id='callback_queue')
		sched.add_job(update_leadrecycle_datetime, "interval", minutes=60, id='update_leadrecycle_datetime')
		db_backup_time = datetime.strptime('00:00','%H:%M') - timedelta(hours=5, minutes=30)
		sched.add_job(sticky_agent_delete, 'cron', day_of_week='*', hour=db_backup_time.hour, minute=db_backup_time.minute, id='sticky_agent_delete')
		password_reminder_email_time = datetime.strptime('00:00','%H:%M') - timedelta(hours=13, minutes=00)
		sched.add_job(PasswordChangeAndLockedReminder, 'cron', day_of_week='*', hour=password_reminder_email_time.hour, minute=password_reminder_email_time.minute, id='password_change_and_locked_reminder')
		print("Connection to db established.")
		connected = True
	except Exception as e:
		print("Connection to db failed. Retrying....%s"%(e))
		time.sleep(1)
if sched.state == 0:
	sched.start()

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
					AGENTS = pickle.loads(settings.R_SERVER.get("agent_status") or pickle.dumps({}))
					if username in AGENTS and AGENTS[username]['wfh']:
						AGENTS[username]['call_type'] = call_type
						AGENTS[username]['state'] = state
						settings.R_SERVER.set("agent_status", pickle.dumps(AGENTS))
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
				user_obj = None
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
						abandoned_obj.user = kwargs.get('user')
						abandoned_obj.save()
					notification_obj.save()				
		if wfh:
			wfh_agents = {}
			AGENTS = pickle.loads(settings.R_SERVER.get("agent_status") or
			pickle.dumps({}))
			if username in AGENTS and AGENTS[username]['wfh'] or kwargs.get('wfh_call'):
				models=['CallDetail','DiallerEventLog']
			wfh_agents = pickle.loads(settings.R_SERVER.get("wfh_agents") or pickle.dumps(wfh_agents))
			if wfh_agents:
				if kwargs.get('session_uuid') in wfh_agents:
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
	except Exception as e:
		print("erro from event_dump : %s"%(e))
	finally:
		transaction.commit()
		connections["crm"].close()
		connections["default"].close()

def cdr_save(model,kwargs,campaign_obj,user_obj,primary_dispo, campaign_name):
	""" saving the reports into the database thats has been dumped"""
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
	except Exception as e:
		print("erro from cdr_save : %s"%(e))
	finally:
		transaction.commit()
		connections["crm"].close()
		connections["default"].close()
