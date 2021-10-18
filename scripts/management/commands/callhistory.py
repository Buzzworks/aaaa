from django.core.management.base import BaseCommand
from django.conf import settings 
from callcenter.models import * 
from crm.models import *
import datetime
import pandas as pd
import math


class Command(BaseCommand):

	help = "Update Calldetails record from the cdr details on 2019-09-14"

	def handle(self, **options):

		call_detail_data = pd.read_csv('/usr/local/src/flexydial/scripts/management/commands/crmcalls_archive.csv',
			na_filter=False)
		campaign = Campaign.objects.first()
		phonebook = Phonebook.objects.first()
		for index, row in call_detail_data.iterrows():
			session_uuid = uuid.uuid4()
			call_detail_dict = {}
			if Contact.objects.filter(numeric=int(row["number"])).exists():
				call_detail_dict["contact_id"] = Contact.objects.filter(numeric=int(row["number"])).first().id
			call_detail_dict["campaign"] = campaign
			call_detail_dict["phonebook"] = phonebook.name
			call_detail_dict["user"] = None
			call_detail_dict["customer_cid"] = row["number"]
			call_detail_dict["callflow"] = "outbound"
			call_detail_dict["callmode"] = row["type"]
			call_detail_dict["destination_extension"] = None
			call_detail_dict["dialed_status"]="Dialed"
			call_detail_dict["session_uuid"] = session_uuid
			call_detail_dict["a_leg_uuid"] = uuid.uuid4()
			call_detail_dict["b_leg_uuid"] = uuid.uuid4()
			call_detail_dict["predictive_time"] = "0:0:0"
			call_detail_dict["progressive_time"] = "0:0:0"
			call_detail_dict["preview_time"] = "0:0:0"
			if row["ts_Wait"]:
				call_detail_dict["init_time"] = datetime.datetime.fromtimestamp(row["ts_Wait"]/1000)
			if row["ts_Call"]:
				call_detail_dict["ring_time"] = datetime.datetime.fromtimestamp(row["ts_Call"]/1000)
			if row["ts_Talk"]:
				call_detail_dict["connect_time"] = datetime.datetime.fromtimestamp(row["ts_Talk"]/1000)
			if row["waitSec"]:
				call_detail_dict["wait_time"] = ':'.join(str(datetime.timedelta(seconds=round(row["waitSec"]/1000))).split(':')[:3])
			call_detail_dict["predictive_wait_time"] = str(datetime.timedelta(seconds=0))
			call_detail_dict["hold_time"] = str(datetime.timedelta(seconds=0))
			call_detail_dict["media_time"] = str(datetime.timedelta(seconds=0))
			if row["talkSec"]:
				call_detail_dict["bill_sec"] =  ':'.join(str(datetime.timedelta(seconds=round(row["talkSec"]/1000))).split(':')[:3])
			if row["callSec"]:
				call_detail_dict["call_duration"] = ':'.join(str(datetime.timedelta(seconds=round(row["callSec"]/1000))).split(':')[:3])
			if row["dispoSec"]:
				call_detail_dict["feedback_time"] =  ':'.join(str(datetime.timedelta(seconds=round(row["dispoSec"]/1000))).split(':')[:3]) 
			call_detail_dict["cfc_number"] = None
			call_detail_dict["internal_tc_number"] = None
			call_detail_dict["external_tc_number"] = None
			if row["ts_Dispo"]:
				call_detail_dict["hangup_time"] = datetime.datetime.fromtimestamp(row["ts_Dispo"]/1000)
			if row["hsource"] == 'Telecaller':
				source = "Agent"
			else:
				source = row["hsource"]
			call_detail_dict["hangup_source"] = source
			call_detail_dict["hangup_cause"] = row["status"]
			call_detail_dict["hangup_cause_code"] = row["statuscode"]
			call_detail_dict["inbound_time"]=str(datetime.timedelta(seconds=0))
			call_detail_dict["inbound_wait_time"]=str(datetime.timedelta(seconds=0))
			call_detail_dict["blended_time"]=str(datetime.timedelta(seconds=0))
			call_detail_dict["blended_wait_time"]=str(datetime.timedelta(seconds=0))
			call_detail_dict["created"]=row["created_at"]
			call_detail_dict["updated"]=row["updated_at"]

			cdr = CallDetail.objects.create(**call_detail_dict)
			remove_keys = ['predictive_time', 'progressive_time','preview_time','predictive_wait_time','feedback_time','cfc_number',
			'internal_tc_number','external_tc_number','hangup_source','inbound_time','inbound_wait_time','blended_time',
			'blended_wait_time']
			for delete_key in remove_keys:
				if delete_key in call_detail_dict:
					del call_detail_dict[delete_key]

			DiallerEventLog.objects.create(**call_detail_dict)

			feedback_dict = {'usersubstatus':row["usersubstatus"], 'usercallback':row["usercallback"],
			"action_code":row["action_code"], "resultcode":row["resultCode"], "nextactioncode":row["nextActionCode"],
			"nextactiondatetime":row["nextActionDateTime"], "rfd":row["rfd"], "userdata":row["userdata"], 
			"pu_tcfr":row["pu_tcfr"], "agency_code":row["agency_code"], "payment_mode":row["payment_mode"],
			"receipt_no":row["receipt_no"], "collection_amount": row["collection_date"], "collection_date": row["collection_date"],
			"cheque_no":row["cheque_no"], "transaction_no":row["transaction_no"], "pickup_contact_person_name":row["pickup_contact_person_name"],
			"pickup_contact_person_mobile":row["pickup_contact_person_mobile"], "pickup_emi_amount":row["pickup_emi_amount"],
			"pickup_bnp_amount":row["pickup_bnp_amount"], "pickup_address_type":row["pickup_address_type"], "pickup_address":row["pickup_address"],
			"pickup_payment_mode":row["pickup_payment_mode"],"pickup_collection_date":row["pickup_collection_date"],
			}


			CdrFeedbck.objects.create(primary_dispo=row["userstatus"], feedback=feedback_dict, comment=row["userremarks"],
				relation_tag={}, session_uuid=session_uuid, calldetail=cdr)
			print(index," row number")

		print("*********************************************************")
		print("!!!!!!!!!!  Call Detail Updated Completely  !!!!!!!!!!")
		print("*********************************************************")
