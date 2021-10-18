from django.core.management.base import BaseCommand
import boto3, os
from os.path import basename
from datetime import date,datetime
import time
from dateutil import parser
from zipfile import ZipFile
from crm.models import DownloadReports
from django.db.models import Q
from callcenter.serializers import CallDetailReportSerializer
from callcenter.models import CallDetail
from django.conf  import settings
import csv

class Command(BaseCommand):

    help = "S3 push file into the bucket"

    def handle(self, **options):
        convert_to_zip = False
        today_obj = date.today()
        today_str = today_obj.strftime('%d-%m-%Y')
        path = '/var/spool/freeswitch/default/'
        report_path = '/var/lib/flexydial/media/download/'
        def save_file(csv_file):
            file_path = settings.MEDIA_ROOT+"/download/calldetail"+today_str+".csv"
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerows(csv_file)
                file.close()
        def create_report():
            start_date = datetime.strptime('2020-07-20 00:00',"%Y-%m-%d %H:%M").isoformat()
            end_date = datetime.strptime('2020-07-20 23:00',"%Y-%m-%d %H:%M").isoformat()
            # start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            # end_date = datetime.now()
            start_end_date_filter = Q(created__gte=start_date)&Q(created__lte=end_date)
            csv_file = []
            col_list =["campaign_name", "user", "full_name", "phonebook", "customer_cid", "contact_id", "uniqueid", "session_uuid",
             "init_time", "ring_time", "connect_time", "hangup_time", "wait_time", "ring_duration", "hold_time", "callflow", "callmode", "bill_sec", "ivr_duration", "call_duration", "feedback_time", 
             "call_length", "hangup_source", "internal_tc_number", "progressive_time", "preview_time", "predictive_wait_time", "inbound_wait_time", "blended_wait_time", "hangup_cause", "hangup_cause_code", "dialed_status", "primary_dispo", "sms_sent", "sms_message", "comment"]
            queryset = CallDetail.objects.filter(start_end_date_filter)
            if queryset.exists():
                csv_file = []
                if "" in col_list:
                    col_list.remove("")
                csv_file.append(col_list)
                count = 0
                for cdr in queryset:
                    row = []
                    data = CallDetailReportSerializer(cdr).data
                    for field in col_list:
                        if not field in data:
                            if field in data['diallereventlog']:
                                row.append(data['diallereventlog'][field])
                            elif data['cdrfeedback'] and field in data['cdrfeedback']:
                                row.append(data['cdrfeedback'][field])
                            elif data['cdrfeedback'] and data['cdrfeedback']['feedback'] and field in data['cdrfeedback']['feedback']:
                                row.append(data['cdrfeedback']['feedback'][field])
                            elif field in data['smslog']:
                                row.append(data['smslog'][field])
                            else:
                                row.append('')
                        else:
                            row.append(data[field])
                    count += 1
                    csv_file.append(row)
                ####### To save file ###########
                save_file(csv_file)
            # else:
            #     print("no calldetail report data")

        create_report()
        print("report Download finished")
        
        with ZipFile('callrecordings'+today_str+'.zip', 'w') as zipObj2:
            for folderName, subfolders, filenames in os.walk(path):
                for filename in filenames:
                    filedate = parser.parse(time.ctime(os.path.getmtime(path+ filename))).date()
                    # if filedate == today_obj:
                    filePath = os.path.join(folderName, filename)
                    zipObj2.write(filePath,basename(filePath))
                        # convert_to_zip = True
                    # else:
                    #     print("no data to create_zip")
             print("reording  Zip finished")
             print("started uploading to aws..............")
            try:
                s3_resource_bucket = boto3.resource('s3')
                s3_bucket_name = s3_resource_bucket.Bucket('incoming-profiles')
                s3_resource_bucket.meta.client.upload_file('callrecordings'+today_str+'.zip','incoming-profiles','callrecordings'+today_str+'.zip')
                s3_bucket_name.put_object(Key='calldetail_'+today_str+'.csv',Body=open("/var/lib/flexydial/media/download/calldetail"+today_str+".csv", 'rb'))
                print("file uploaded finished**************")
                # os.remove("callrecordings"+today_str+".zip")
            except Exception as e:
                print(e)