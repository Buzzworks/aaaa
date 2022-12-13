from datetime import datetime, timedelta
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from flexydial import settings
from callcenter.schedulejobs import (
	add_user_rpc,
	del_user_rpc,
	campaign_rpc,
	group_campaign_rpc,
	campaign_action_rpc,
	user_campaign_rpc,
	del_campaign_rpc,
	leadrecycle_add,
	leadrecycle_del,
	usr_campaign_switch_rpc,
	)
from django.core.files import File



sched = BackgroundScheduler()
sched.add_jobstore(MemoryJobStore(), 'task')
if sched.state != 'STATE_STOPPED':
	sched.start()

def aps_phonebook_upload(**kwargs):
	"""
	this is the function defined for  upload and update phonebook .
	"""	
	from crm.utility import validate_uploaded_phonebook, validate_updated_phonebook
	execution_time = datetime.now() + timedelta(seconds=1)
	job_id = kwargs['phone_inst'].campaign.replace(" ", "")+kwargs['phone_inst'].name.replace(" ", "")+str(kwargs['phone_inst'].id)
	if kwargs['action_type']=='insert' or kwargs['action_type']=='':
		sched.add_job(validate_uploaded_phonebook,'date', run_date=execution_time, name=job_id,
			jobstore='task', kwargs=kwargs)
	else:
		sched.add_job(validate_updated_phonebook,'date', run_date=execution_time, name=job_id,
			jobstore='task', kwargs=kwargs)
	
def fs_pre_del_user(user_ext,domain):
	"""
	this is the function defined for delete user .
	"""	
	execution_time = datetime.now() + timedelta(seconds=3)
	data={'extension':user_ext,'domain':domain}
	sched.add_job(del_user,'date', run_date=execution_time, name='calls',
				jobstore='task', kwargs=data)

def fs_camp_action(sender, **kwargs):
	"""
	this is the function defined for camp action.
	"""	
	execution_time = datetime.now() + timedelta(seconds=5)
	sched.add_job(campaign_action_rpc,'date', run_date=execution_time, name='calls',
			jobstore='task', kwargs=kwargs)

def fs_switch_action(sender, **kwargs):
	"""
	this is the function defined for switch action in freeswitch.
	"""	
	execution_time = datetime.now() + timedelta(seconds=5)
	sched.add_job(usr_campaign_switch_rpc,'date', run_date=execution_time, name='calls',
			jobstore='task', kwargs=kwargs)

def fs_add_user(sender, **kwargs):
	"""
	this is the function defined for add user action in freeswitch.
	"""	
	execution_time = datetime.now() + timedelta(seconds=10)
	sched.add_job(add_user_rpc,'date', run_date=execution_time, name='calls',
			jobstore='task', kwargs=kwargs)

def fs_del_user(sender, **kwargs):
	"""
	this is the function defined for delete user action in freeswitch.
	"""	
	execution_time = datetime.now() + timedelta(seconds=5)
	sched.add_job(del_user_rpc,'date', run_date=execution_time, name='calls',
			jobstore='task', kwargs=kwargs)

def fs_campaign(sender, **kwargs):
	"""
	this is the function defined for campaign action in freeswitch.
	"""	
	execution_time = datetime.now() + timedelta(seconds=5)
	sched.add_job(campaign_rpc,'date', run_date=execution_time, name='calls',
			jobstore='task', kwargs=kwargs)

def fs_del_campaign(sender, **kwargs):
	"""
	this is the function defined for del campaign action in freeswitch.
	"""	
	execution_time = datetime.now() + timedelta(seconds=3)
	sched.add_job(del_campaign_rpc,'date', run_date=execution_time, name='calls',
			jobstore='task', kwargs=kwargs)

def fs_group_campaign(sender, **kwargs):
	"""
	this is the function defined for group delete action in freeswitch.
	"""	
	if kwargs["action"] == "pre_remove":
		execution_time = datetime.now() + timedelta(seconds=3)
	elif kwargs["action"] == "post_add":
		execution_time = datetime.now() + timedelta(seconds=6)
	else:
		execution_time = datetime.now() + timedelta(seconds=5)
	sched.add_job(group_campaign_rpc,'date', run_date=execution_time,name='calls',
			jobstore='task', kwargs=kwargs)


def fs_user_campaign(sender, **kwargs):
	"""
	this is the function defined for user campaign  action in freeswitch.
	"""	
	if kwargs["action"] == "pre_remove":
		execution_time = datetime.now() + timedelta(seconds=3)
	elif kwargs["action"] == "post_add":
		execution_time = datetime.now() + timedelta(seconds=6)
	else:
		execution_time = datetime.now() + timedelta(seconds=5)
	sched.add_job(user_campaign_rpc,'date', run_date=execution_time,name='calls',
			jobstore='task', kwargs=kwargs)



def recording_file_move(sender,**kwargs):
	"""
	this function to insert recording file into bucket
	"""

	if settings.AWS_STORAGE_BUCKET_NAME or settings.GS_BUCKET_NAME:
		dialereventlog = kwargs["instance"]
		instance_id = dialereventlog.pk
		filter_instance = sender.objects.filter(id = instance_id)

		if not dialereventlog.recording_file:
			file_path=settings.RECORDING_ROOT+"/"+datetime.strptime(dialereventlog.ring_time,"%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y-%H-%M")+"_"+dialereventlog.customer_cid+"_"+dialereventlog.session_uuid+".mp3"
			if os.path.isfile(file_path):
				f = open(file_path, 'rb')
				filter_instance.update(recording_file = File(f,os.path.basename(f.name)))
				# dialereventlog.save()
				f.close()
			else:
				print('File not exists ::',file_path)