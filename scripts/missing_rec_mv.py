import os
import sys
from flexydial import settings
from callcenter.models import DiallerEventLog
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from datetime import datetime, timedelta
from django.db import connection, connections
from django.db import transaction
from django.core.files import File
from os import listdir
ENABLE = False

job_defaults = {
	'coalesce': True,
	'max_instances': 15
}
sched = BlockingScheduler()
sched.configure(job_defaults=job_defaults)


print("hiiiii from missing rec fileee")


def recording_file_transfer():
	"""
	this function to insert recording file into bucket
	"""
	
	count_rec = 0
	print("recording file transferrr function started")
	
	if settings.AWS_STORAGE_BUCKET_NAME or settings.GS_BUCKET_NAME: #to check if there is any bucket name available for AWS or GCP
		try:
			push_rec_status = settings.R_SERVER.get("push_rec_status") #getting push_rec_status key from redis server and storing into a variable
			if not push_rec_status or push_rec_status.decode('utf-8') == 'False': #condition satisfies if key value is False
				dialereventlog_emty_rec = DiallerEventLog.objects.filter(recording_file="",created__date__gte='2022-08-01',callserver=settings.FS_INTERNAL_IP).exclude(occurence_counter=3).order_by('created') #excludes the recordings if the occurence_counter value is three
				print(dialereventlog_emty_rec,"emty_rec")
				if dialereventlog_emty_rec:

					print('rec_mv_started')
					settings.R_SERVER.set("push_rec_status", True) #setting push_rec_status key as True in redis
					for dialereventlog in dialereventlog_emty_rec: #iterating through dialereventlog_emty_rec
						
						if dialereventlog.session_uuid: #condition satisfies if any rec file is having a session_uuid
							file_path=settings.RECORDING_ROOT+"/"+datetime.strptime(str(dialereventlog.ring_time),"%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y-%H-%M")+"_"+str(dialereventlog.customer_cid)+"_"+str(dialereventlog.session_uuid)+".mp3"
							onlyfiles = [f for f in listdir(settings.RECORDING_ROOT+"/")]
							print(onlyfiles,"only filess")

							ele = "_"+str(dialereventlog.customer_cid)+"_"+str(dialereventlog.session_uuid)+".mp3"
							# print(ele,"elee filess")

							all_rec_files = "~".join(onlyfiles)
							# print(all_rec_files,"all recordings")
							if os.path.isfile(file_path):
								print("it is satisfying isfile")
								
								save_recordings(dialereventlog,file_path)
							elif ele in all_rec_files:
								print("it is satisfying ele in all_rec_files condition")

								ind = all_rec_files.index(ele)
								start = ind - 16 #len("11-04-2022-17-45")
								end = ind+len(ele)
								file_path = settings.RECORDING_ROOT+"/"+all_rec_files[start:end]
								print(file_path,"pathhhhhh")
								save_recordings(dialereventlog,file_path)
							else:
								# if file_path: #if file_path is not available in var/spool/freeswitch/default folder this condition will satisfy
								print('File not exists ::',file_path)
								count_rec +=1 #the counter value increases on basis of number of missed recordings
								print(count_rec,"counttt")
									
								count_val = dialereventlog.occurence_counter #retriving occurence_counter value from the model
								if count_val == None: #if the occurence counter value of a specific recording is None then this condition will satisfy
									count_val=0 #the new value of count_val is assigend as zero
								count_val+=1 #increments count_val value everytime whenever the schedular runs after a period of time. 
								print(count_val,"countt vall")
								updated_dialer_event = DiallerEventLog.objects.filter(id = dialereventlog.id)
								updated_dialer_event.update(occurence_counter = count_val)
								# dialereventlog.occurence_counter = count_val
								# dialereventlog.save(update_fields=['occurence_counter'])
								# DiallerEventLog.objects.update(occurence_counter=count_val) #Updates the occurence_counter value to new count value

								
					settings.R_SERVER.set("push_rec_status", False)	
				print("Recordings Moved to Bucket")

			else:
				print("Status is True")# redis key status is True if it is in else
		except Exception as e:

			settings.R_SERVER.set("push_rec_status", False)	
			print("Exception occures from recording_file_transfer",e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
		finally:
			transaction.commit()
			connections['default'].close()
def save_recordings(dialereventlog,file_path):
	# if (dialereventlog.connect_time or dialereventlog.dialed_status=='Connected'):
	
	f = open(file_path, 'rb')
	dialereventlog.recording_file.save(os.path.basename(f.name), File(f), save=True)
	dialereventlog.save()
	print(dialereventlog.recording_file,"recordinggg")
	f.close()

def missing_recording_transfer():
	"""
	Start APSchedular for autodialing.
	"""
	global ENABLE
	settings.R_SERVER.set("push_rec_status", False)
	sched.add_jobstore(MemoryJobStore(), 'list')
	execution_time = datetime.now() + timedelta(minutes=0.1)

	sched.add_job(recording_file_transfer,'interval',seconds=3600, start_date=execution_time,
						   id='recording_file_transfer', jobstore='list')
	if sched.state == 0:
		sched.start()
if __name__ == '__main__':
	missing_recording_transfer()