import sys, os
import psycopg2
from datetime import datetime, timedelta
from django.conf import settings
from django.db import transaction
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from django.db import connections
from callcenter.models import (Campaign)
from scripts.fsautodial import fsdial,fs_voice_blaster

ENABLE = False

job_defaults = {
	'coalesce': True,
	'max_instances': 15
}
sched = BlockingScheduler()
sched.configure(job_defaults=job_defaults)
CAMPAIGNS={}


def fs_call():
	"""
	This function is use to schedule dial process recursively.
	"""
	try:
		campaign = Campaign.objects.filter(status="Active",switch__ip_address=settings.FREESWITCH_IP_ADDRESS).prefetch_related()
		for camp in campaign:
			if camp.vbcampaign.exists() and camp.vbcampaign.filter(status="Active"):
				fs_voice_blaster(camp)
			elif 'outbound' in camp.dial_method and camp.dial_method['outbound'] == 'Predictive':
				fsdial(camp)
	except (NameError, psycopg2.OperationalError, psycopg2.InterfaceError):
		print("Postgres server not loaded")
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	finally:
		transaction.commit()
		connections['default'].close()

def set_ad_campaign_status():
	""" setting true all the ad campaings in redis"""
	try:
		campaign = Campaign.objects.values('id','name')
		for camp in campaign:
			settings.R_SERVER.hset("ad_campaign_status",camp['name'], True)
		print('all campaign set to true in redis for autodial')
	except Exception as e:
		print('exception set_ad_campaign_status',e)

def exec_autodial():
	"""
	Start APSchedular for autodialing.
	"""
	global ENABLE
	sched.add_jobstore(MemoryJobStore(), 'list')
	set_ad_campaign_status()
	execution_time = datetime.now() + timedelta(minutes=0.1)
	sched.add_job(fs_call,'interval',seconds=10, start_date=execution_time,
						   id='autodial', jobstore='list')
	if sched.state == 0:
		sched.start()
if __name__ == '__main__':
	exec_autodial()
