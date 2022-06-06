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



from crm.models import MasterContact,ScheduleMasterContact, Contact
from crm.serializers import MasterContactSerializer
import numpy as np
import pandas as pd
def MasterContactAutodial():
	try:
		contactobjs=ScheduleMasterContact.objects.filter(status='scheduled').order_by('id').first()

		if contactobjs:
			contactobjs.status='started'
			contactobjs.save()
			contact_objs_excel=contactobjs.mcdata
			orginal_df=pd.read_csv(contact_objs_excel)

			if orginal_df.dtypes['numeric']==int:#checking if numeric is intege, if integer then convert to object else pass
				orginal_df.numeric=orginal_df['numeric'].astype(str)

			lst=[]#list of unique id's for messages in improper data
			improper_df_numerics=orginal_df[~orginal_df.numeric.apply(lambda x: x.isnumeric())]# remove ~ for proper df
			lst.append({"notnumericid":improper_df_numerics['unique_id'].tolist()})

			# improper_df_length=orginal_df[~(orginal_df['numeric'].str.len() == 10)]#make == for properdf, for 10 legth use range
			improper_df_length=orginal_df[((orginal_df['numeric'].str.len() < 6)|(orginal_df['numeric'].str.len() > 10))]
			# df[(x <= df['columnX']) & (df['columnX'] <= y)]

			lst.append({"notlength":improper_df_length['unique_id'].tolist()})

			cust_unique_id=list(MasterContact.objects.all().values_list('unique_id',flat=True))
			cust_unique_id.append("911")
			improper_df_cust_unq=orginal_df[orginal_df['unique_id'].isin(cust_unique_id)]
			lst.append({"same_unique":improper_df_cust_unq['unique_id'].tolist()})


			#print("lstis",lst)#this lst contains unique id's dict of both notnumeric and notlength

			#CREATING PROPER DF
			#if df contains other than numerics
			numerics_lst=lst[0]['notnumericid']
			proper_df_filtering_numerics=orginal_df[~orginal_df['unique_id'].isin(numerics_lst)]

			#if df contains invalid length of numerics
			numerics_lst_1=lst[1]['notlength']
			proper_df_filtering_numerics=proper_df_filtering_numerics[~proper_df_filtering_numerics['unique_id'].isin(numerics_lst_1)]


			#if df contains existing unique id's
			numerics_lst_2=lst[2]['same_unique']
			proper_df_filtering_numerics=proper_df_filtering_numerics[~proper_df_filtering_numerics['unique_id'].isin(numerics_lst_2)]

			ref_id=contactobjs.ref_id
			proper_df_filtering_numerics.to_csv("/var/lib/flexydial/media/upload/"+ref_id+"tmp_file_proper.csv",index=False)
			contactobjs.proper_mcdata='upload/'+ref_id+"tmp_file_proper.csv"	#storing proper csv
			contactobjs.save()


			#CREATING IMPROPER DF
			improper_df_filtering_numerics=orginal_df[orginal_df['unique_id'].isin(numerics_lst)]
			improper_df_filtering_numerics['msg1']="must contains only numerics"

			improper_df_filtering_numerics_1=orginal_df[orginal_df['unique_id'].isin(numerics_lst_1)]
			improper_df_filtering_numerics_1['msg2']="must contain in numbers rnage of 6 to 10"

			improper_df_filtering_numerics_2=orginal_df[orginal_df['unique_id'].isin(numerics_lst_2)]
			improper_df_filtering_numerics_2['msg3']="must contain different unique id's"


			# # learn append, merge, concat
			improper_df=pd.concat([improper_df_filtering_numerics,improper_df_filtering_numerics_1,improper_df_filtering_numerics_2])
			aggregation_functions = {'numeric':'first','unique_id':'first','customer_raw_data':'first','msg1': 'sum', 'msg2': 'sum', 'msg3': 'sum'}

			improper_df = improper_df.groupby(improper_df['unique_id']).aggregate(aggregation_functions)

			improper_df.to_csv("/var/lib/flexydial/media/upload/"+ref_id+"tmp_file_improper.csv",index=False)
			contactobjs.improper_mcdata='upload/'+ref_id+"tmp_file_improper.csv"	#storing improper csv
			contactobjs.save()

			df_to_dict=proper_df_filtering_numerics.to_dict('records')
			contactobjs.status='dbsaving'
			contactobjs.save()
			contactser=MasterContactSerializer(data=df_to_dict,many=True)
			if contactser.is_valid():
				contactser.save()
				contactobjs.status='finished'
				contactobjs.save()
				print("saved in main contact table")

			else:
				print("errors in contact serializer saving",contactser.errors())

			# contactobjs.status='scheduled'
			# contactobjs.save()

			"""
			#this is the autodial code for master contact css execution
			latest_push_ids=[]
			for x in contactser.data:
				id=dict(x)
				id=id['id']
				latest_push_ids.append(id)
			print("latest ids is",latest_push_ids)

			master_css_all=MasterCSS.objects.all()
			contacts_list=[]
			for each_query in master_css_all:
				x=MasterContact.objects.filter(id__in=latest_push_ids).raw(each_query.raw_query)
				print("x is",str(x),'type is',type(x))
				for p in x:
					if not Contact.objects.filter(numeric=p.numeric,campaign=each_query.campaign).exists():
						contacts_list.append(Contact(numeric=p.numeric,campaign=each_query.campaign,contact_id=p))
			Contact.objects.bulk_create(contacts_list)"""

		else:
			print("no scheduled moving are there")
	except Exception as e:
		print("exception in code errors",str(e))



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
	sched.add_job(MasterContactAutodial,'interval', seconds=10, start_date=execution_time,
					id='MasterContactAutodial', jobstore='list')
	if sched.state == 0:
		sched.start()
if __name__ == '__main__':
	exec_autodial()
