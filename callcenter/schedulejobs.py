import time
import json
import csv
from django.conf import settings
from datetime import datetime,date,timedelta
from django.utils.timezone import utc
import socket, errno, xmlrpc.client
from django.utils import timezone
from django.db.models import Q, F
# from scripts import eventdump
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.db import connection, connections
from django.db import transaction
# from callcenter.utility import get_current_users, download_call_detail_report, download_agent_perforance_report, campaignwise_performance_report, download_agent_mis, download_agent_activity_report, download_campaignmis_report, download_callbackcall_report,download_abandonedcall_report,set_download_progress_redis, download_call_recordings, download_contactinfo_report, download_billing_report, camp_list_users, DownloadCssQuery
# from  callcenter.utility import download_call_detail_report

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
		'max_workers': '5'
	},
	'apscheduler.job_defaults.coalesce': 'true',
	'apscheduler.job_defaults.max_instances': '3',
})

def add_leadrecycle_db(*args):
	""" adding lead recycle data into the contact data with scheduler """
	try:
		from crm.models import Contact,Phonebook
		from callcenter.models import Campaign,PhonebookBucketCampaign
		campaign_id = None
		if args[0] in ['Drop','Abandonedcall','NC','Invalid Number','AutoFeedback','CBR']:
			contacts = list(Contact.objects.filter(campaign = args[1],status=args[0],churncount__lte=int(args[2])))
		else:
			contacts = list(Contact.objects.filter(campaign = args[1],disposition =args[0],churncount__lte=int(args[2]),
				status='Dialed'))
		campaign_inst = Campaign.objects.filter(name=args[1])
		if campaign_inst.exists():
			campaign_id = campaign_inst.first().id
		if contacts:
			for contact in contacts:
				contact.status='NotDialed'
				contact.churncount = contact.churncount + 1
		Contact.objects.bulk_update(contacts,['status', 'churncount'])
		PhonebookBucketCampaign.objects.filter(id=campaign_id).update(is_contact=True)
		transaction.commit()
		connections['crm'].close()
		connections['default'].close()
	except Exception as e:
		print(e)	

def leadrecycle_add(**kwargs):
	""" adding leadrecycle into the scheduler for job creation and execution """
	try:
		job_id = str(kwargs['instance'].campaign)+'_'+str(kwargs['instance'].id)
		args = [str(kwargs['instance'].name),str(kwargs['instance'].campaign),kwargs['instance'].count]
		if sched.state == 0:
			sched.start()
		lead_job = sched.get_job(job_id)
		if lead_job:
			sched.remove_job(job_id)
		if kwargs['instance'].schedule_type == 'schedule_time':
			schedule_period= json.loads(kwargs['instance'].schedule_period)
			if schedule_period["start_time"] != "" and schedule_period["end_time"] !="":
				start_datetime  = date.today().strftime('%Y-%m-%d')+' '+schedule_period["start_time"]+':00'
				end_datetime = date.today().strftime('%Y-%m-%d')+' '+schedule_period["end_time"]+':00'
				str_datetime_obj = datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')-timedelta(hours=5,minutes=30)
				end_datetime_obj = datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S')-timedelta(hours=5,minutes=30)
				sched.add_job(add_leadrecycle_db, 'interval',args=args, seconds=kwargs['instance'].recycle_time, start_date=str(str_datetime_obj),
						end_date=str(end_datetime_obj), id =job_id)
		elif kwargs['instance'].schedule_type == 'recycle_time':
			if kwargs['instance'].recycle_time != 0 and kwargs['instance'].recycle_time != None:
				sched.add_job(add_leadrecycle_db, 'interval',args=args, seconds=kwargs['instance'].recycle_time, id =job_id)
				
	except Exception as e:
		print(e)
	finally:
		transaction.commit()
		connections['crm'].close()
		connections['default'].close()

def download_report(*args):
	""" creating a download report with the job scheduler daily"""
	try:
		from callcenter.serializers import CallDetailReportSerializer
		from callcenter.models import PauseBreak,Campaign,CallDetail,ReportColumnVisibility
		from crm.models import DownloadReports
		from  callcenter.utility import (download_call_detail_report,campaignwise_performance_report,download_agent_perforance_report,download_agent_activity_report,download_campaignmis_report,download_agent_mis, download_callbackcall_report,
			download_abandonedcall_report, download_billing_report)
		if args[0] == 'Call Detail':
			columns = ReportColumnVisibility.objects.filter(user_id=args[2], report_name='1')
			col_list = columns.first().columns_name if columns.exists() else ["campaign_name", "user", "full_name", "supervisor_name","phonebook", "customer_cid", "contact_id", "uniqueid", "session_uuid", "init_time", "ring_time", "connect_time", "hangup_time", "wait_time", "ring_duration", "hold_time", "callflow", "callmode", "bill_sec", "ivr_duration", "call_duration", "feedback_time", "call_length", "hangup_source", "internal_tc_number", "progressive_time", "preview_time", "predictive_wait_time", "inbound_wait_time", "blended_wait_time", "hangup_cause", "hangup_cause_code", "dialed_status", "primary_dispo", "sms_sent", "sms_message", "comment"]
			download_call_detail_report(filters=args[3], user=args[2], col_list=col_list, serializer_class=CallDetailReportSerializer, download_report_id=None)
		if args[0] == 'Agent Activity':
			columns = ReportColumnVisibility.objects.filter(user_id=args[2], report_name='5')
			col_list = columns.first().columns_name if columns.exists() else ['user','full_name','event','event_time','tos','app_time','campaign_name','dialer_time','idle_time',
			'media_time','hold_time','spoke_time','preview_time','progressive_time','pause_progressive_time',
			'predictive_time','predictive_wait_time','inbound_time','inbound_wait_time','blended_time',
			'blended_wait_time','transfer_time','feedback_time','break_type','break_time']
			download_agent_activity_report(filters=args[3], user=args[2], col_list=col_list, download_report_id=None)
		if args[0] == 'Agent Performance':
			columns = ReportColumnVisibility.objects.filter(user_id=args[2], report_name='3')
			pause_breaks = list(PauseBreak.objects.values_list('name',flat=True))
			col_list =columns.first().columns_name if columns.exists() else ['username','full_name','supervisor_name','campaign','app_idle_time','dialer_idle_time','pause_progressive_time','progressive_time','preview_time',
			'predictive_wait_time','inbound_wait_time','blended_wait_time','ring_duration','hold_time','media_time','bill_sec','call_duration','feedback_time','break_time','app_login_time'
			] + pause_breaks + ['dialer_login_time','total_login_time','total_calls']
			download_agent_perforance_report(filters=args[3], user=args[2], col_list=col_list, download_report_id=None)
			# DownloadReports.objects.create(report='Agent Performance',filters=args[3], user=args[2],serializers=None, col_list=col_list, status=True)
		if args[0] == 'Campaign Performance':
			columns = ReportColumnVisibility.objects.filter(user_id=args[2], report_name='7')
			col_list= columns.first().columns_name if columns.exists() else ['campaign','dialer_idle_time','pause_progressive_time','progressive_time','preview_time',
			'predictive_wait_time','inbound_wait_time','blended_wait_time','ring_duration','hold_time','media_time','bill_sec','call_duration','feedback_time','break_time',
			'dialer_login_time','total_login_time','total_calls']
			campaignwise_performance_report(filters=args[3], user=args[2], col_list=col_list, download_report_id=None)
			# DownloadReports.objects.create(report='Campaign Wise Performance',filters=args[3], user=args[2],serializers=None, col_list=col_list, status=True)
		if args[0] == 'Agent Mis':
			columns = ReportColumnVisibility.objects.filter(user_id=args[2], report_name='4')
			all_fields =  set(Campaign.objects.filter(status='Active').exclude(disposition=None).values_list("disposition__name", flat=True))
			wfh_dispo_list = list(Campaign.objects.filter(wfh=True, status='Active').values_list('wfh_dispo',flat=True))
			wfh_dispo = set([ d for m in wfh_dispo_list for d in m.values()])
			all_fields.update(wfh_dispo)
			tmp_list = ["User", "Full Name","Supervisor Name","Campaign", "Total Dispo Count", "AutoFeedback", "AbandonedCall",
				'NC','Invalid Number',"RedialCount"]
			col_list = columns.first().columns_name if columns.exists() else tmp_list + list(all_fields)
			download_agent_mis(filters=args[3], user=args[2], col_list=col_list, download_report_id=None)
			# DownloadReports.objects.create(report='Agent Mis Report', filters=args[3], user=args[2], serializers=None, col_list=col_list, status=True)
		if args[0] == 'Campaign Mis': 
			columns = ReportColumnVisibility.objects.filter(user_id=args[2], report_name='6')
			all_fields =  list(set(Campaign.objects.all().exclude(disposition=None).values_list("disposition__name", flat=True)))
			tmp_list = ["Campaign", "Total Dispo Count"]
			statuc_field = list(set(CallDetail.objects.filter().order_by().values_list("dialed_status", flat=True).distinct()))
			statuc_field = ['status_'+status for status in statuc_field]
			col_list =  columns.first().columns_name if columns.exists() else tmp_list + list(set(statuc_field +all_fields)) 
			download_campaignmis_report(filters=args[3], user=args[2], col_list=col_list, download_report_id=None)
			# DownloadReports.objects.create(report='Campaign Mis', filters=args[3], user=args[2], serializers=None, col_list=col_list, status=True)	
		if args[0] == 'CallBack':
			columns = ReportColumnVisibility.objects.filter(user_id=args[2], report_name='8')
			col_list = columns.first().columns_name if columns.exists() else ['campaign', 'phonebook', 'user','full_name','numeric', 'status', 'callback_title',
			'callback_type', 'schedule_date', 'disposition', 'comment']
			download_callbackcall_report(filters=args[3], user=args[2], col_list=col_list, download_report_id=None)
			# DownloadReports.objects.create(report='CallBack', filters=args[3], user=args[2], serializers=None, col_list=col_list, status=True)
		if args[0] == 'Abandoned Call':
			columns = ReportColumnVisibility.objects.filter(user_id=args[2], report_name='9')
			col_list = columns.first().columns_name if columns.exists() else ['campaign', 'user','full_name','numeric', 'status', 'call_date']
			download_abandonedcall_report(filters=args[3], user=args[2], col_list=col_list, download_report_id=None)
			# DownloadReports.objects.create(report='Abandoned Call',filters=args[3], user=args[2], serializers=None, col_list=col_list, status=True)
		if args[0] == 'Billing':
			columns = ReportColumnVisibility.objects.filter(user_id=args[2], report_name='11')
			col_list = columns.first().columns_name if columns.exists() else ['source', 'buzzworks_id', 'user_id', 'location', 'ip_address','days', 'days_band']
			download_billing_report(filters=args[3], user=args[2], col_list=col_list, download_report_id=None)
			# DownloadReports.objects.create(report='Billing Report',filters=args[3], user=args[2], serializers=UserSerializer, col_list=col_list, status=True)
	except Exception as e:
		print("emailing  the report error ",e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)

def schedulereports_download(**kwargs):
	""" creating a job id and excution of the jobs on defined time """
	try:
		from callcenter.models import Campaign,User
		for report in kwargs['instance'].reports:
			job_id = (str(report)+'_'+str(kwargs['instance'].id)).replace(' ','_')
			filters = {}
			filters['is_scheduler'] = True
			filters['all_campaigns'] = list(Campaign.objects.values_list('name',flat=True))
			filters['all_users'] = list(User.objects.values_list('id',flat=True))
			filters['start_date'] = datetime.today().replace(hour=00, minute=00,second=00).strftime('%Y-%m-%d %H:%M')
			filters['end_date'] = datetime.today().replace(hour=23, minute=55,second=00).strftime('%Y-%m-%d %H:%M')
			if report == "Billing":
				filters = {}
				filters['is_scheduler'] = True
				filters['years'] = date.today().year
				filters['month'] = date.today().month
			args = [report, job_id,kwargs['instance'].created_by_id,filters]
			if sched.state == 0:
				sched.start()
			email_job = sched.get_job(job_id)
			if email_job:
				sched.remove_job(job_id)
			if kwargs['instance'].schedule_time:
				sched.add_job(download_report,'cron',args=args, hour=int(kwargs['instance'].schedule_time[:2]),
				minute=int(kwargs['instance'].schedule_time[3:5]), id=job_id)	
	except Exception as e:
		print(e)
	finally:
		transaction.commit()
		connections['crm'].close()
		connections['default'].close()

def remove_scheduled_job(job_id):
	""" Removing the jobs after job execution """
	try:
		if sched.state == 0:
			sched.start()
		job = sched.get_job(job_id)
		if job:
			sched.remove_job(job_id)        
	except Exception as e:
		print(e)
	finally:
		transaction.commit()
		connections['crm'].close()
		connections['default'].close()

def leadrecycle_del(job_id):
	""" deleting the leadrecycle after the lead execution """
	try:
		if sched.state == 0:
			sched.start()
		lead_job = sched.get_job(job_id)
		if lead_job:
			sched.remove_job(job_id)
	except Exception as e:
		print(e)
	finally:
		transaction.commit()
		connections['crm'].close()		


def freeswicth_server(server_ip):
	"""
	this function is for making connection to the freeswitch 
	by using the campaign ip_address
	"""
	from callcenter.models import Switch
	rpc_port = Switch.objects.filter(ip_address=server_ip).first().rpc_port
	SERVER = xmlrpc.client.ServerProxy("http://%s:%s@%s:%s" % (settings.RPC_USERNAME,
			 settings.RPC_PASSWORD,server_ip,rpc_port))
	return SERVER 

def add_user(domain,**kwargs):
	""" Add the users into the freeswitch apis"""
	user = kwargs["instance"]
	SERVER = freeswicth_server(domain)
	try:
		extension = user.extension
		if type(extension) == int:
			extension = str(user.extension)
		user_in_server = SERVER.freeswitch.api("callcenter_config","agent list "+extension)
		if (kwargs.get("created", None) in [True, False]):
			if user_in_server[1:][0].split('|')[0] != extension:
				SERVER.freeswitch.api("callcenter_config",
					"agent add %s %s" % (extension, user.type))
		else:
			pass
		if 'freetdm' not in user.contact:
			SERVER.freeswitch.api("callcenter_config",
					"agent set contact %s %s/%s@%s" % (extension, user.contact,
						extension, user.domain.ip_address))
		else:
			SERVER.freeswitch.api("callcenter_config",
					"agent set contact %s %s/%s" % (extension, user.contact,
						extension))
		SERVER.freeswitch.api("callcenter_config",
				"agent set type %s %s" % (extension, user.type))
		SERVER.freeswitch.api("callcenter_config",
				"agent set status %s '%s'" % (extension, user.dial_status))
		SERVER.freeswitch.api("callcenter_config",
				"agent set max_no_answer %s %s" % (extension,
					user.max_no_answer))
		SERVER.freeswitch.api("callcenter_config",
				"agent set wrap_up_time %s %s" % (extension,
					user.wrap_up_time))
		SERVER.freeswitch.api("callcenter_config",
				"agent set reject_delay_time %s %s" % (extension,
					user.reject_delay_time))
		SERVER.freeswitch.api("callcenter_config",
				"agent set busy_delay_time %s %s" % (extension,
					user.busy_delay_time))
		SERVER.freeswitch.api("reload", "mod_callcenter")
	except socket.error as e:
		print ("RPC Error %s: Freeswitch RPC module may not be" \
				"loaded or properly configured" % e)
	finally:
		transaction.commit()
		connections['default'].close()


def add_user_rpc(**kwargs):
	""" Getting the users and assign it to the campaign """
	try:
		user = kwargs["instance"]
		from callcenter.models import Campaign
		if (user.user.group.all()):
			campaign_ip = Campaign.objects.filter(group__in=user.user.group.all()).prefetch_related('switch')
			if campaign_ip:
				for campaign in campaign_ip:
					camp_domain = campaign.switch.ip_address
					add_user(camp_domain,**kwargs)
			else:
				domain = user.domain.ip_address
				add_user(domain,**kwargs)			

		campaign_ip = Campaign.objects.filter(users=user.user).prefetch_related('switch')
		if campaign_ip:
			for campaign in campaign_ip:
				camp_domain = campaign.switch.ip_address
				add_user(camp_domain,**kwargs)
		if not campaign_ip and not user.user.group.all():
			domain = user.domain.ip_address
			print(domain,'-------')
			add_user(domain,**kwargs)
		#Create server xml file
		from django.core import management
		management.call_command('create_call_server_xml')
		transaction.commit()
		connections['default'].close()
		print("===============================")
	except Exception as e:
		print("emailing  the report error ",e)

def del_user_rpc(**kwargs):
	""" This method is used to delete the freeswitch rpc users """
	try:
		print(314, '--------')
		user = kwargs["instance"]
		SERVER = freeswicth_server(user.domain.ip_address)
		SERVER.freeswitch.api("callcenter_config",
				"agent del %s" % (user.extension))
		SERVER.freeswitch.api("xml_flush_cache",
				"id %s %s" % (user.extension, user.domain.ip_address))
		#Create server xml file
		from django.core import management
		management.call_command('create_call_server_xml')
	except socket.error as v:
		print ("RPC Error %s: Freeswitch RPC module may not be" \
				"loaded or properly configured" % v[0])
	finally:
		transaction.commit()
		connections['default'].close()

def camp_add_user(SERVER,user):
	""" This method used to add the campaign and users list  into freeswitch"""
	user_in_server = SERVER.freeswitch.api("callcenter_config","agent list "+user.extension)
	try:
		if user_in_server[1:][0].split('|')[0] != user.extension:
			SERVER.freeswitch.api("callcenter_config",
					"agent add %s %s" % (user.extension, user.type))
		if 'freetdm' not in user.contact:
			SERVER.freeswitch.api("callcenter_config",
					"agent set contact %s %s/%s@%s" % (user.extension, user.contact,
						user.extension, user.domain.ip_address))
		else:
			SERVER.freeswitch.api("callcenter_config",
					"agent set contact %s %s/%s" % (user.extension, user.contact,
						user.extension))
		SERVER.freeswitch.api("callcenter_config",
				"agent set type %s %s" % (user.extension, user.type))
		SERVER.freeswitch.api("callcenter_config",
				"agent set status %s '%s'" % (user.extension, user.status))
		SERVER.freeswitch.api("callcenter_config",
				"agent set max_no_answer %s %s" % (user.extension,
					user.max_no_answer))
		SERVER.freeswitch.api("callcenter_config",
				"agent set wrap_up_time %s %s" % (user.extension,
					user.wrap_up_time))
		SERVER.freeswitch.api("callcenter_config",
				"agent set reject_delay_time %s %s" % (user.extension,
					user.reject_delay_time))
		SERVER.freeswitch.api("callcenter_config",
				"agent set busy_delay_time %s %s" % (user.extension,
					user.busy_delay_time))
	except socket.error as v:
		print ("RPC Error %s: Freeswitch RPC module may not be" \
				"loaded or properly configured" % v)
	finally:
		transaction.commit()
		connections['default'].close()
		
def campaign_action_rpc(**kwargs):
	""" This method is used to chcek the campaign action with the freeswitch """
	campaign = kwargs["instance"]
	SERVER = freeswicth_server(campaign.trunk.switch.ip_address)	
	try:
		campaigns = kwargs["instance"]
		if (kwargs.get("created", None) in [True, False]):
			#    (campaign.enabled <= datetime.utcnow().replace(tzinfo=utc))):
			for campaign in campaigns.all():
				SERVER.freeswitch.api("callcenter_config",
						"queue load %s" % (campaign.slug))
		else:
			for campaign in campaigns.all():
				SERVER.freeswitch.api("callcenter_config",
						"queue unload %s" % (campaign.slug))
	except socket.error as v:
		print ("RPC Error %s: Freeswitch RPC module may not be" \
				"loaded or properly configured" % v[0])
	finally:
		transaction.commit()
		connections['default'].close()

def campaign_rpc(**kwargs):
	""" This method is used to create campaign rpc"""
	try:
		campaign = kwargs["instance"]
		camp_domain = campaign.campaign.switch.ip_address
		SERVER = freeswicth_server(camp_domain)
		if ((kwargs.get("created", None) in [True, False]) and
				(campaign.campaign.status == 'Active')):
			SERVER.freeswitch.api("callcenter_config",
					"queue load %s" % (campaign.campaign.slug))
			from callcenter.models import Campaign,User
			users = User.objects.filter(Q(group__in = Campaign.objects.get(
							slug = campaign.campaign.slug).group.all())|Q(
							id__in = Campaign.objects.get(slug = campaign.campaign.slug
							).users.all().values_list("id", flat=True))).prefetch_related()
			for user in users:
				if user.uservariable.domain.ip_address != camp_domain:
					camp_add_user(SERVER,user.uservariable)
		else:
			SERVER.freeswitch.api("callcenter_config",
					"queue unload %s" % (campaign.campaign.slug))
		#Create server xml file
		from django.core import management
		management.call_command('create_call_server_xml')
	except socket.error as v:
		print ("RPC Error %s: Freeswitch RPC module may not be" \
				"loaded or properly configured campaign" % v)
	finally:
		transaction.commit()
		connections['default'].close()

def user_campaign_rpc(**kwargs):
	""" this method is used to create the user campaign rpc in freeswitch """
	try:
		campaign = kwargs["instance"]
		SERVER =freeswicth_server(campaign.switch.ip_address)
		if (kwargs["action"] == "pre_remove"):
			fs_camp_tiers = SERVER.freeswitch.api("callcenter_config",
					"queue list tiers '%s'" % str(campaign.slug))
			camp_tiers = fs_camp_tiers.splitlines()
			for tier in camp_tiers[1:-1]:
				fs_tier =  tier.split('|')
				SERVER.freeswitch.api("callcenter_config",
						"tier del %s %s" % (fs_tier[0], fs_tier[1]))
		if (kwargs["action"] == "post_add"):
			for user in campaign.users.all():
				SERVER.freeswitch.api("callcenter_config",
					"tier add %s %s %s %s" % (campaign.slug, user.properties.extension,
						user.properties.level, user.properties.position))
	except socket.error as v:
		print ("RPC Error %s: Freeswitch RPC module may not be" \
				"loaded or properly configured" % v[0])
	finally:
		transaction.commit()
		connections['default'].close()

def group_campaign_rpc(**kwargs):
	""" this method create a group in campaign with freeswitch """
	try:
		campaign = kwargs["instance"]
		SERVER =freeswicth_server(campaign.switch.ip_address)
		if (kwargs["action"] == "pre_remove"):
			fs_camp_tiers = SERVER.freeswitch.api("callcenter_config",
					"queue list tiers '%s'" % str(campaign.slug))
			camp_tiers = fs_camp_tiers.splitlines()
			for tier in camp_tiers[1:-1]:
				fs_tier =  tier.split('|')
				SERVER.freeswitch.api("callcenter_config",
						"tier del %s %s" % (fs_tier[0], fs_tier[1]))
		if (kwargs["action"] == "post_add"):
			from callcenter.models import User,Campaign
			users = User.objects.filter(group__in = Campaign.objects.get(
							slug = campaign.slug).group.all()).prefetch_related()			
			for user in users:
				SERVER.freeswitch.api("callcenter_config",
					"tier add %s %s %s %s" % (campaign.slug, user.properties.extension,
						user.properties.level, user.properties.position))
	except socket.error as v:
		print ("RPC Error %s: Freeswitch RPC module may not be" \
				"loaded or properly configured" % v[0])
	finally:
		transaction.commit()
		connections['default'].close()

def del_campaign_rpc(**kwargs):
	""" this method deletes the created campaign in the freeswitch """
	try:
		campaign = kwargs["instance"]
		camp_domain = campaign.switch.ip_address
		SERVER = freeswicth_server(camp_domain)
		SERVER.freeswitch.api("callcenter_config",
					"queue unload %s" % (campaign.slug))
		#Create server xml file
		from django.core import management
		management.call_command('create_call_server_xml')
	except socket.error as v:
		print ("RPC Error %s: Freeswitch RPC module may not be" \
				"loaded or properly configured" % v[0])
	finally:
		transaction.commit()
		connections['default'].close()

def usr_campaign_switch_rpc(**kwargs):
	""" this method will create the user campaign and switch config in freeswith """
	try:
		switch = kwargs["instance"]
		switch_address = switch.ip_address
		SERVER = freeswicth_server(switch_address)
		if switch.status == 'Active':
			from callcenter.models import Campaign,User,UserVariable
			campaigns = Campaign.objects.filter(switch=switch)
			for campaign in campaigns:
				camp_domain = campaign.switch.ip_address
				SERVER.freeswitch.api("callcenter_config",
						"queue load %s" % (campaign.slug))
				users = User.objects.filter(Q(group__in = Campaign.objects.get(
								slug = campaign.slug).group.all())|Q(
								id__in = Campaign.objects.get(slug = campaign.slug
								).users.all().values_list("id", flat=True))).prefetch_related()
				for user in users:
					if user.uservariable.domain.ip_address != camp_domain:
						camp_add_user(SERVER,user.uservariable)
		#Create server xml file
		from django.core import management
		management.call_command('create_call_server_xml')
		SERVER.freeswitch.api("reload", "mod_callcenter")
		print("Callcenter loaded")
	except socket.error as v:
		print ("RPC Error %s: Freeswitch RPC module may not be" \
				"loaded or properly configured campaign" % v)
	finally:
		transaction.commit()
		connections['default'].close()