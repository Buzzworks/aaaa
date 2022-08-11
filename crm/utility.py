import os,sys
import re
import json
import pandas as pd
from datetime import datetime, date,timedelta
from django.apps import apps
from django.conf import settings
from django.core.files import File
from .models import (Contact, CrmField, ContactInfo, Phonebook, CampaignInfo, LeadListPriority, TempContactInfo, AlternateContact)
from callcenter.models import Campaign, User ,DNC, DataUploadLog,PhonebookBucketCampaign, Disposition
from callcenter.utility import(get_model_data)
from flexydial.views import (data_for_pagination, get_paginated_object)
from django.http import HttpResponse
from django.db import transaction, connections
import csv
import pickle
from django.db.models import Q
from dateutil.parser import parse
cwd = os.path.join(settings.BASE_DIR, 'static/')

def get_crm_fields(campaign_name,temp=False):
	""" This is used to get the crm fields """ 
	column_list = []
	crm_section_fields = {}
	if Campaign.objects.filter(name=campaign_name).exists():
		campaign = Campaign.objects.get(name=campaign_name)
		crm_fields = CrmField.objects.filter(campaign__name=campaign_name)
		for crm_field in crm_fields:
			# sections = json.loads(crm_field.crm_fields)
			sections = crm_field.crm_fields
			for section in sections:
				crm_section_fields[section['db_section_name']]={}
				section_fields = section["section_fields"]
				for section_field in section_fields:
					if temp:
						crm_section_fields[section['db_section_name']][section_field['db_field']]=""
					else:
						column_list.append(section_field["db_field"])
	if temp and crm_section_fields:
		return crm_section_fields
	return column_list

def get_customizable_crm_fields(campaign_name):
	""" This is used to get the crm customizable fields """
	column_list = []
	if Campaign.objects.filter(name=campaign_name).exists():
		campaign = Campaign.objects.get(name=campaign_name)
		crm_fields = CrmField.objects.filter(campaign__name=campaign_name)
		for crm_field in crm_fields:
			sections = sorted(crm_field.crm_fields, key = lambda i: i['section_priority'])
			for section in sections:
				section_name = section["db_section_name"]
				section_fields = sorted(section["section_fields"], key = lambda f: f['priority'])
				for section_field in section_fields:
					column_list.append(section_name+":"+section_field["db_field"])
	return column_list


def crm_field_value_schema(campaign_name):
	""" This is used to get the crm value schemas fields """
	schema = {}
	if Campaign.objects.filter(name=campaign_name).exists():
		campaign = Campaign.objects.get(name=campaign_name)
		crm_fields = CrmField.objects.filter(campaign__name=campaign_name)
		for crm_field in crm_fields:
			sections = crm_field.crm_fields
			for section in sections:
				section_name = section["db_section_name"]
				section_fields = section["section_fields"]
				for section_field in section_fields:
					if section_name not in schema:
						schema[section_name] = {}
					if section_field["field_type"] == 'multicheckbox' or section_field["field_type"] == 'multiselect':
						schema[section_name][section_field["db_field"]] = []
					else:
						schema[section_name][section_field["db_field"]] = None
	return schema

def get_customizable_crm_fields_with_datatype(campaign_name):
	""" This is used to get the crm customizable with the datatypes fields """
	column_list = []
	if Campaign.objects.filter(name=campaign_name).exists():
		campaign = Campaign.objects.get(name=campaign_name)
		crm_fields = CrmField.objects.filter(campaign__name=campaign_name)
		for crm_field in crm_fields:
			sections = sorted(crm_field.crm_fields, key = lambda i: i['section_priority'])
			for section in sections:
				section_name = section["db_section_name"]
				section_fields = sorted(section["section_fields"], key = lambda f: f['priority'])
				for section_field in section_fields:
					section_field_dict = {}
					section_field_dict["field_name"] = section_name+":"+section_field["db_field"]
					section_field_dict["field_type"] = section_field["field_type"]
					section_field_dict["size"] = section_field["size"]
					column_list.append(section_field_dict)
	return column_list

def crm_field_datatype_validation(check_field, row, data_dict, field):
	""" This is used to get the crm datatype validation fields """
	if type(row.get(check_field, '')) is pd.Timestamp:
		row[check_field] = str(row.get(check_field,""))
	if field["field_type"] in ["textarea", "text", "integer"] and row.get(check_field, '') and field["size"] and len(str(row.get(check_field, ''))) > int(field["size"]):
		data_dict[check_field] = "Expected length is {}".format(field["size"])
	if str(row.get(check_field, '')) and field["field_type"] in ["integer"]:
		try:
			int(row.get(check_field, ''))
		except Exception as e:
			data_dict[check_field] = "Expected  {} in {} format".format(row.get(check_field, ''), field["field_type"])
	elif str(row.get(check_field, '')) and field["field_type"] in ["float"]:
		try:
			float(row.get(check_field, ''))
		except Exception as e:
			data_dict[check_field] = "Expected  {} in {} format".format(row.get(check_field, ''), field["field_type"])
	elif str(row.get(check_field, '')) and field["field_type"] in ["datefield","datetimefield"]:
		try:
			date_string = parse(row.get(check_field, ''))
			if field["field_type"] == "datefield":
				row[check_field] = date_string.strftime('%Y-%m-%d')
			else:
				row[check_field] = date_string.strftime('%Y-%m-%d %H:%M:%S')
		except Exception as e:
			data_dict[check_field] = "Expected  {} in {} format".format(row.get(check_field, ''), field["field_type"])
	elif str(row.get(check_field, '')) and field["field_type"] in ["timefield"]:
		try:
			datetime.strptime(row.get(check_field, ''), "%H:%M:%S")
		except Exception as e:
			data_dict[check_field] = "Expected  {} in {} format".format(row.get(check_field, ''), field["field_type"])
	return data_dict, row

def save_contact(phone_inst, campaign, row, key, c_info, search_type, action_type="insert", crm_field_list=[], unique_field="", alternate_numbers={}):
	""" This is used to get the contacts save"""
	try:
		# crm_field_list = get_customizable_crm_fields(campaign.name)
		crm_field_dict = {}
		data_dict = {}
		uniqueid = None
		contact_col_list = ["numeric","first_name","last_name","user","email", "priority"]
		for field in crm_field_list:
			section_name = field["field_name"].split(':')[0].replace(' ','_').lower()
			field_name = field["field_name"].split(':')[1].replace(' ','_').lower()
			check_field = field["field_name"]
			data_dict, row = crm_field_datatype_validation(check_field, row, data_dict, field)
			if section_name not in crm_field_dict:
				crm_field_dict[section_name] = {}
			crm_field_dict[section_name][field_name] = repr(row.get(check_field, "")).replace("'", "")
			if crm_field_dict[section_name][field_name] =='':
				crm_field_dict[section_name][field_name] = None

		if not data_dict:
			if unique_field:
				uniqueid = row.get(unique_field,None)
				if unique_field in row and key and 'status' in campaign.lead_priotize[key] and campaign.lead_priotize[key]['status']==str('true'):
					value = repr(row.get(uniqueid, "")).replace("'", "")
					if value:
						query_data = LeadListPriority.objects.filter(Q(uniqueid=value),Q(Q(campaign_id=campaign.id)|Q(is_global=True))).first()
						if query_data and 'tap' in campaign.lead_priotize[key]:
							row["priority"] = query_data.priority
							if query_data.campaign_id==campaign.id and not query_data.is_global:
								query_data.delete()	
		if data_dict:
			return data_dict,{},alternate_numbers
		contact_dict = { update_key: str(row[update_key]) for update_key in contact_col_list if update_key in row }		
		contact_dict["campaign"] = campaign.name
		priority = row.get("priority","")
		if "alt_numeric" in row and str(row.get("alt_numeric", "")).strip():
			alternate_numbers = create_alt_num_dict(str(row.get("alt_numeric", "")), alternate_numbers)
		if row.get("priority","") == "":
			priority = None
		else:
			priority = int(priority)
		contact_dict["priority"] = priority
		contact_dict["customer_raw_data"] = crm_field_dict
		contact_dict["phonebook"] = phone_inst
		contact_dict["uniqueid"] = uniqueid
		return {}, contact_dict, alternate_numbers
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print(e, 'Exception in save contact.')	

def update_contact(phone_inst, campaign, row, key, c_info, search_type, action_type="insert", crm_field_list=[], contact_list=[],unique_field="", alt_number_dict={}):
	""" This is used to get the update contacts """
	try:
		crm_field_dict = {}
		customer_raw_data = {}
		data_dict = {}
		uniqueid = None
		contact = []
		if len(c_info)>0:
			for index,contact_data in c_info.iterrows():
				customer_raw_data = contact_data.customer_raw_data
				break
		contact_col_list = ["numeric","first_name","last_name","user","email", "priority", "disposition"]
		for field in crm_field_list:
			section_name = field["field_name"].split(':')[0].replace(' ','_').lower()
			field_name = field["field_name"].split(':')[1].replace(' ','_').lower()
			check_field = field["field_name"]
			if check_field in row:
				data_dict, row = crm_field_datatype_validation(check_field, row, data_dict, field)
				if section_name not in customer_raw_data:
					customer_raw_data[section_name] = {}
				customer_raw_data[section_name][field_name] = repr(row.get(check_field, "")).replace("'", "")
				if customer_raw_data[section_name][field_name] =='':
					customer_raw_data[section_name][field_name] = None

		if not data_dict:
			
			if unique_field:
				uniqueid = row.get(unique_field,None)
				if unique_field in row and key and 'status' in campaign.lead_priotize[key] and campaign.lead_priotize[key]['status']==str('true'):
					value = repr(row.get(uniqueid, "")).replace("'", "")
					if value:
						query_data = LeadListPriority.objects.filter(Q(uniqueid=value),Q(Q(campaign_id=campaign.id)|Q(is_global=True))).first()
						if query_data and 'tap' in campaign.lead_priotize[key]:
							row["priority"] = query_data.priority
							if query_data.campaign_id==campaign.id and not query_data.is_global:
								query_data.delete()	
		if data_dict:
			return data_dict,{},contact_list,alt_number_dict
			
		contact_dict = { update_key: str(row[update_key]) for update_key in contact_col_list if update_key in row }
		priority = row.get("priority",None)
		if "alt_numeric" in row and str(row.get("alt_numeric", "")).strip():
			alt_number_dict = create_alt_num_dict(str(row.get("alt_numeric", "")),alt_number_dict)
		if row.get("priority","") == "":
			priority = None
		else:
			priority = int(priority)
		contact_dict["priority"] = priority
		if unique_field and unique_field in row:
			contact_dict["uniqueid"] = uniqueid
		contact_dict['customer_raw_data'] = customer_raw_data
		for index,contact_data in c_info.iterrows():
			[setattr(contact_data,col_name,contact_dict[col_name]) for col_name in contact_dict.keys()]
			setattr(contact_data,'pk',contact_data.id)
			contact_list.append(contact_data)
		return {}, contact_dict, contact_list, alt_number_dict
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print(e, 'Exception in update contact.')

def save_csv(file_name, list):
	""" This is used to the save the csv file """
	try:
		with open(file_name, 'w+', encoding='utf-8') as file:
			for row in list:
				row.to_csv(file, index=False, header=file.tell() == 0,encoding='utf-8')
	except Exception as e:
		print(e)


def save_xls(file_name, list_val):
	""" This is used to save the xls file"""
	try:
		writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
		df = pd.concat(list_val)
		df.to_excel(writer, sheet_name='Sheet1', index=False)
		writer.save()
	except Exception as e:
		print(e)

def validate_uploaded_phonebook(**kwarg):
	"""
	This method is used to validate phone book file.
	It will check phonebook with given info already exists
	or not
	"""
	try:
		correct_count = 0
		incorrect_count = 0
		correct_list = []
		contact_list = []
		incorrect_list = []
		update_alt_numeric_list = []
		created_alt_numeric_list = []
		duplicate_list = pd.DataFrame()
		data = kwarg["data"]
		duplicate_check = kwarg["duplicate_check"]
		action_type = kwarg["action_type"]
		search_type = kwarg["search_type"]
		unique_field = ""
		file_extension = kwarg['file_extension']
		if not action_type:
			action_type="insert"
		phone_inst = kwarg["phone_inst"]
		if not data.empty:
			PHONEBOOK_STATUS = {}
			PHONEBOOK_STATUS = pickle.loads(settings.R_SERVER.get("phonebook") or pickle.dumps(PHONEBOOK_STATUS))
			PHONEBOOK_STATUS[''+str(phone_inst.id)+''] = 0
			settings.R_SERVER.set("phonebook", pickle.dumps(PHONEBOOK_STATUS))
			######## Check Duplicates in CSV File ###########
			if duplicate_check and duplicate_check in data.columns:
				dummy_df = data[(data[duplicate_check] != '')]
				duplicate_list = dummy_df[dummy_df.duplicated(
					[duplicate_check], keep='first')]
				frame = [duplicate_list]
				duplicate_list = pd.concat(frame)
				index_list = duplicate_list.index.tolist()
				data = data.drop(index_list)

				duplicate_list['description'] = 'This row is duplicated in file'
				incorrect_count = len(duplicate_list)
				incorrect_list.append(duplicate_list)
			campaign = Campaign.objects.get(id=phone_inst.campaign)
			camp_name = campaign.name
			campaign_id = campaign.id
			settings.R_SERVER.hset("pb_campaign_status",campaign.id, False)
			job_id = phone_inst.campaign.replace(" ", "")+phone_inst.name.replace(" ", "")+str(phone_inst.id)

			job_id_check = list(set(DataUploadLog.objects.filter(job_id=job_id).values_list('job_id', flat=True)))
			if job_id_check:
				DataUploadLog.objects.filter(job_id__in=job_id_check).delete()

			data_upload_log, _ = DataUploadLog.objects.get_or_create(job_id=job_id)
			total_data = len(data)
			data_upload_log.status = 0
			data_upload_log.save()
			updated_index = 0
			raw_query = ''
			already_exist_type = 'campaigns'
			if search_type == '0':
				raw_query = """ where phonebook_id = """+str(phone_inst.id)
				already_exist_type = 'phonebook'
			elif search_type == '1':
				raw_query = " where campaign = '"+str(camp_name)+"'"
				already_exist_type = 'campaign'
			key = ''
			if campaign.lead_priotize:
				for keys in campaign.lead_priotize.keys():
					key = str(keys)
			if duplicate_check:
				if duplicate_check == "numeric":
					error_msg = duplicate_check
					query_str = """ SELECT * FROM crm_contact """
				else:
					error_msg = ' '.join(duplicate_check.split(':')[1].split('_'))
					query_str = """ SELECT *,customer_raw_data ->'%s'->'%s' as duplicate_check from crm_contact """ % (str(duplicate_check).split(':')[0], str(duplicate_check).split(':')[1])
				query_str += raw_query
				contacts_data = pd.read_sql_query(query_str, connections['crm'])
			alt_num_data = pd.read_sql_query('select * from crm_alternatecontact', connections['crm'])
			crm_field_list = get_customizable_crm_fields_with_datatype(campaign.name)
			crm_field_obj = CrmField.objects.filter(campaign__name=campaign.name)
			if crm_field_obj.exists():
				unique_field = crm_field_obj.values("unique_fields")[0]["unique_fields"][0]
			for index, row in data.iterrows():
				updated_index += 1
				data_dict = {}
				priority = str(row.get("priority", ""))
				numeric = str(row.get("numeric", ""))
				alt_numeric = str(row.get("alt_numeric", ""))
				email = str(row.get("email", ""))
				user = str(row.get("user",""))
				ext_contact_id = []
				c_info = None
				########### Check Duplicate value in Contact infor raw_data ############
				if duplicate_check and str(duplicate_check) in row and row[str(duplicate_check)]:
					if duplicate_check == "numeric":
						c_info = contacts_data.loc[contacts_data.numeric==str(row.get(""+str(duplicate_check)+"",""))]
					else:
						c_info = contacts_data.loc[contacts_data.duplicate_check==str(row.get(""+str(duplicate_check)+"",""))]
					if len(c_info)>0:
						already_exist_type_value = ','.join(c_info.campaign.tolist())
						if already_exist_type == 'phonebook':
							already_exist_type_value = phone_inst.name
						elif already_exist_type == 'campaign':
							already_exist_type_value = camp_name
						data_dict["duplicate_check"] = "contact with this {} value is already exist in {} {}".format(error_msg, already_exist_type_value, already_exist_type)
				if numeric:
					if not numeric.isdigit():
						data_dict["number"] = "Enter Valid Number"
					else:
						if DNC.objects.filter(numeric=numeric[-10:],status='Active',global_dnc=True).exists():
							data_dict["number"] = "This number is blocked globally"
						elif DNC.objects.filter(numeric=numeric[-10:],status='Active',campaign=campaign).exists():
							data_dict["number"] = "This number is blocked in this campaign"
				if priority:
					if not priority.isdigit():
						data_dict["priority"] = "Enter Valid priority"
					elif len(str(priority)) > 9:
						data_dict["priority"] = "Priority value should be less than 9 digit"
				if not numeric and action_type != 'update':
					data_dict["number"] = "Enter Number"
				if alt_numeric:
					if len(alt_numeric.split(",")) >= 4:
						data_dict["alt_numeric"] = "More than 5 alternate numbers are not allowed"
				if email:
					if not re.findall('\S+@\S+', email):
						data_dict["email"] = "Enter Valid Email Address"
				if user:
					if not User.objects.filter(username=user).exists():
						data_dict["user"] = "This user is not present in our database"

				if data_dict:
					incorrect_count = incorrect_count + 1
					row["description"] = json.dumps(data_dict)
					incorrect_data = pd.DataFrame(row).T.applymap(str)
					incorrect_list.append(pd.DataFrame(row).T.applymap(str))
				else:
					alternate_numbers = pd.DataFrame()
					alt_number_dict = {}
					if not alt_num_data.empty:
						if unique_field and str(unique_field) in row and row[str(unique_field)]:
							alternate_numbers = alt_num_data.loc[alt_num_data.uniqueid==str(row.get(""+str(unique_field)+"",""))]
						elif "numeric" in row:
							alternate_numbers = alt_num_data.loc[alt_num_data.numeric==str(row.get(""+str("numeric")+"",""))]
						if not alternate_numbers.empty:
							alt_number_dict = alternate_numbers.alt_numeric.to_list()[0]
					error_dict, contact_obj, alt_number_dict = save_contact(phone_inst, campaign, row, key, c_info, search_type, action_type, crm_field_list, unique_field, alt_number_dict)
					if error_dict:
						incorrect_count = incorrect_count + 1
						row["description"] = json.dumps(error_dict)
						incorrect_list.append(pd.DataFrame(row).T.applymap(str))
					else:
						correct_count = correct_count + 1
						correct_list.append(pd.DataFrame(row).T.applymap(str))
						contact_list.append(Contact(**contact_obj))
						if "alt_numeric" in row and str(row.get("alt_numeric", "")).strip():
							if not alternate_numbers.empty:
								for index, alt_info in alternate_numbers.iterrows():
									setattr(alt_info, 'alt_numeric', alt_number_dict)
									setattr(alt_info, 'pk', alt_info.id)
									update_alt_numeric_list.append(alt_info)
							else:
								created_alt_numeric_list.append(AlternateContact(numeric=contact_obj['numeric'], uniqueid=contact_obj['uniqueid'], alt_numeric=alt_number_dict))
				# calculate how much percentage is completed
				get_percentage = ((updated_index)/len(data.index)) * 100
				data_upload_log.completed_percentage = get_percentage
				if get_percentage in [100.0,100]:
					data_upload_log.status = 1
					PHONEBOOK_STATUS = pickle.loads(settings.R_SERVER.get("phonebook") or pickle.dumps(PHONEBOOK_STATUS))
					del PHONEBOOK_STATUS[''+str(phone_inst.id)+'']
					data_upload_log.completed_percentage = 100
				else:
					PHONEBOOK_STATUS = pickle.loads(settings.R_SERVER.get("phonebook") or pickle.dumps(PHONEBOOK_STATUS))
					PHONEBOOK_STATUS[''+str(phone_inst.id)+''] = round(get_percentage,2)
				if PHONEBOOK_STATUS:
					settings.R_SERVER.set("phonebook", pickle.dumps(PHONEBOOK_STATUS))
				data_upload_log.save()
			data = {}
			if correct_count:
				PhonebookBucketCampaign.objects.filter(id=campaign.id).update(is_contact=True)
				try:
					Contact.objects.bulk_create(contact_list)
					if update_alt_numeric_list:
						AlternateContact.objects.bulk_update(update_alt_numeric_list,['alt_numeric'],batch_size=100)
					if created_alt_numeric_list:
						AlternateContact.objects.bulk_create(created_alt_numeric_list)
					if file_extension == '.csv':
						save_csv(cwd+"csv_files/proper_data"+file_extension, correct_list)
					else:
						save_xls(cwd+"csv_files/proper_data"+file_extension, correct_list)
					correct_file_path = "/csv_files/proper_data"+file_extension
					f = open(cwd+correct_file_path, 'rb')
					save_file_as = phone_inst.name+'-'+str(phone_inst.id)+"_"+"contact_file"+file_extension
					phone_inst.contact_file.save(save_file_as, File(f), save=True)
					phone_inst.last_updated_contact_count = correct_count
					phone_inst.save()
					f.close()
				except Exception as e:
					print(e)
			if incorrect_count:
				try:
					if file_extension == '.csv':
						save_csv(cwd+"csv_files/improper_data"+file_extension, incorrect_list)
					else:
						save_xls(cwd+"csv_files/improper_data"+file_extension, incorrect_list)
					incorrect_file_path = "csv_files/improper_data"+file_extension
					f = open(cwd+incorrect_file_path, 'rb')
					save_file_as = phone_inst.name+'-'+str(phone_inst.id)+"_"+"improper_data"+file_extension 				
					data_upload_log.improper_file.save(save_file_as, File(f), save=True)
					data_upload_log.incorrect_count = incorrect_count
					f.close()
				except Exception as e:
					print(e)
			PHONEBOOK_STATUS = {}
			PHONEBOOK_STATUS = pickle.loads(settings.R_SERVER.get("phonebook"))
			PHONEBOOK_STATUS['is_refresh'] = True
			if str(phone_inst.id) in PHONEBOOK_STATUS: 
				del PHONEBOOK_STATUS[''+str(phone_inst.id)+'']
			settings.R_SERVER.set("phonebook", pickle.dumps(PHONEBOOK_STATUS))

			phonebook_ids = list(Phonebook.objects.filter(campaign=campaign.id,status='Active').values_list('id',flat=True))
			phonebook_ids = list(map(str,phonebook_ids))
			if not set(phonebook_ids) & set(PHONEBOOK_STATUS.keys()):
				settings.R_SERVER.hset("pb_campaign_status",campaign.id, True)
			data_upload_log.save()
			transaction.commit()
			connections.close_all()
	except Exception as e:
		print("Exception occures from validate uploade phonebook",e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		settings.R_SERVER.hset("pb_campaign_status",kwarg["phone_inst"].campaign, True)
		return

def validate_updated_phonebook(**kwarg):
	"""
	This method is used to validate phone book file.
	It will check phonebook with given info already exists
	or not
	"""
	try:
		correct_count = 0
		incorrect_count = 0
		correct_list = []
		contact_list = []
		incorrect_list = []
		update_alt_numeric_list = []
		created_alt_numeric_list = []
		duplicate_list = pd.DataFrame()
		data = kwarg["data"]
		duplicate_check = kwarg["duplicate_check"]
		action_type = kwarg["action_type"]
		search_type = kwarg["search_type"]
		unique_field = ""
		file_extension = kwarg['file_extension']
		# if not action_type:
		# 	action_type="insert"
		phone_inst = kwarg["phone_inst"]
		if not data.empty:
			PHONEBOOK_STATUS = {}
			PHONEBOOK_STATUS = pickle.loads(settings.R_SERVER.get("phonebook") or pickle.dumps(PHONEBOOK_STATUS))
			PHONEBOOK_STATUS[''+str(phone_inst.id)+''] = 0
			settings.R_SERVER.set("phonebook", pickle.dumps(PHONEBOOK_STATUS))
			######## Check Duplicates in CSV File ###########	
			if duplicate_check and duplicate_check in data.columns:
				dummy_df = data[(data[duplicate_check] != '')]
				duplicate_list = dummy_df[dummy_df.duplicated(
					[duplicate_check], keep='first')]
				frame = [duplicate_list]
				duplicate_list = pd.concat(frame)
				index_list = duplicate_list.index.tolist()
				data = data.drop(index_list)

				duplicate_list['description'] = 'This row is duplicated in file'
				incorrect_count = len(duplicate_list)
				incorrect_list.append(duplicate_list)
			campaign = Campaign.objects.get(id=phone_inst.campaign)
			camp_name = campaign.name
			campaign_id = campaign.id
			settings.R_SERVER.hset("pb_campaign_status",campaign.id, False)
			job_id = phone_inst.campaign.replace(" ", "")+phone_inst.name.replace(" ", "")+str(phone_inst.id)

			job_id_check = list(set(DataUploadLog.objects.filter(job_id=job_id).values_list('job_id', flat=True)))
			if job_id_check:
				DataUploadLog.objects.filter(job_id__in=job_id_check).delete()

			data_upload_log, _ = DataUploadLog.objects.get_or_create(job_id=job_id)
			total_data = len(data)
			data_upload_log.status = 0
			data_upload_log.save()
			updated_index = 0
			key = ''
			if campaign.lead_priotize:
				for keys in campaign.lead_priotize.keys():
					key = str(keys)
			filter_query = Q()
			raw_query = ''
			dosenot_exist_type = 'application'
			if search_type == '0':
				filter_query = Q(phonebook_id=phone_inst.id)
				raw_query = """ where phonebook_id = """+str(phone_inst.id)
				dosenot_exist_type = 'phonebook'
			elif search_type == '1':
				filter_query = Q(campaign=campaign.name)
				raw_query = " where campaign = '"+str(campaign.name)+"'"
				dosenot_exist_type = 'campaign'
			crm_field_list = get_customizable_crm_fields_with_datatype(campaign.name)
			crm_field_obj = CrmField.objects.filter(campaign__name=campaign.name)
			if crm_field_obj.exists():
				unique_field = crm_field_obj.values("unique_fields")[0]["unique_fields"][0]
			if duplicate_check == "numeric":
				error_msg = duplicate_check
				query_str = """ SELECT * FROM crm_contact """
			else:
				error_msg = ' '.join(duplicate_check.split(':')[1].split('_'))
				query_str = """ SELECT *,customer_raw_data ->'%s'->'%s' as duplicate_check from crm_contact """ % (str(duplicate_check).split(':')[0], str(duplicate_check).split(':')[1])
			query_str += raw_query
			contacts_data = pd.read_sql_query(query_str, connections['crm'])
			alt_num_data = pd.DataFrame()
			if 'alt_numeric' in data.columns:
				alt_num_data = pd.read_sql_query('select * from crm_alternatecontact', connections['crm'])
			for index, row in data.iterrows():
				updated_index += 1
				data_dict = {}
				priority = str(row.get("priority", ""))
				numeric = str(row.get("numeric", ""))
				alt_numeric = str(row.get("alt_numeric", ""))
				email = str(row.get("email", ""))
				user = str(row.get("user",""))
				disposition = str(row.get("disposition",""))
				ext_contact_id = []
				c_info = None
				########### Check Duplicate value in Contact infor raw_data ############
				if duplicate_check and str(duplicate_check) in row and row[str(duplicate_check)]:
					if duplicate_check == "numeric":
						c_info = contacts_data.loc[contacts_data.numeric==str(row.get(""+str(duplicate_check)+"",""))]
					else:
						c_info = contacts_data.loc[contacts_data.duplicate_check==str(row.get(""+str(duplicate_check)+"",""))]
					if len(c_info)<1:
						data_dict["duplicate_check"] = "the {} is not exist in {}, please insert first".format(error_msg, dosenot_exist_type)
					incorrect_list.append(duplicate_list)
				else:
					data_dict["duplicate_check"] = "the {} should not be blank".format(error_msg)
				if numeric:
					if not numeric.isdigit():
						data_dict["number"] = "Enter Valid Number"
				if priority:
					if not priority.isdigit():
						data_dict["priority"] = "Enter Valid priority"
					elif len(str(priority)) > 9:
						data_dict["priority"] = "Priority value should be less than 9 digit"
				if alt_numeric:
					if len(alt_numeric.split(",")) >= 4:
						data_dict["alt_numeric"] = "More than 5 alternate numbers are not allowed"
				if email:
					if not re.findall('\S+@\S+', email):
						data_dict["email"] = "Enter Valid Email Address"
				if user:
					if not User.objects.filter(username=user).exists():
						data_dict["user"] = "This user is not present in our database"
				if disposition:
					if not Disposition.objects.filter(name=disposition).exists():
						data_dict["disposition"] = "This disposition is not present in our database, dispositions are case sensative add same name as created in campaign dispositions"
				if data_dict:
					incorrect_count = incorrect_count + 1
					row["description"] = json.dumps(data_dict)
					incorrect_data = pd.DataFrame(row).T.applymap(str)
					incorrect_list.append(pd.DataFrame(row).T.applymap(str))
				else:
					alternate_numbers = pd.DataFrame()
					alt_number_dict = {}
					if not alt_num_data.empty:
						if duplicate_check and str(duplicate_check) in row and row[str(duplicate_check)]:
							if duplicate_check == "numeric":
								alternate_numbers = alt_num_data.loc[alt_num_data.numeric==str(row.get(""+str(duplicate_check)+"",""))]
							else:
								alternate_numbers = alt_num_data.loc[alt_num_data.uniqueid==str(row.get(""+str(duplicate_check)+"",""))]
							if not alternate_numbers.empty:
								alt_number_dict = alternate_numbers.alt_numeric.to_list()[0]
					error_dict, contact_obj, contact_list, alt_number_dict = update_contact(phone_inst, campaign, row, key, c_info, search_type, action_type, crm_field_list,contact_list,unique_field, alt_number_dict)
					if error_dict:
						incorrect_count = incorrect_count + 1
						row["description"] = json.dumps(error_dict)
						incorrect_list.append(pd.DataFrame(row).T.applymap(str))
					else:
						correct_count = correct_count + 1
						correct_list.append(pd.DataFrame(row).T.applymap(str))
						if "alt_numeric" in row and str(row.get("alt_numeric", "")).strip():
							if not alternate_numbers.empty:
								for index, alt_info in alternate_numbers.iterrows():
									setattr(alt_info, 'alt_numeric', alt_number_dict)
									setattr(alt_info, 'pk', alt_info.id)
									update_alt_numeric_list.append(alt_info)
							else:
								if duplicate_check == "numeric":
									created_alt_numeric_list.append(AlternateContact(numeric=contact_obj['numeric'], alt_numeric=alt_number_dict))
								else:
									created_alt_numeric_list.append(AlternateContact(uniqueid=contact_obj['uniqueid'], alt_numeric=alt_number_dict))
						
				# calculate how much percentage is completed
				get_percentage = ((updated_index)/len(data.index)) * 100
				data_upload_log.completed_percentage = get_percentage
				if get_percentage in [100.0,100]:
					data_upload_log.status = 1
					PHONEBOOK_STATUS = pickle.loads(settings.R_SERVER.get("phonebook") or pickle.dumps(PHONEBOOK_STATUS))
					del PHONEBOOK_STATUS[''+str(phone_inst.id)+'']
					data_upload_log.completed_percentage = 100
				else:
					PHONEBOOK_STATUS = pickle.loads(settings.R_SERVER.get("phonebook") or pickle.dumps(PHONEBOOK_STATUS))
					PHONEBOOK_STATUS[''+str(phone_inst.id)+''] = round(get_percentage,2)
				if PHONEBOOK_STATUS:
					settings.R_SERVER.set("phonebook", pickle.dumps(PHONEBOOK_STATUS))
				data_upload_log.save()
			data = {}
			if correct_count:
				PhonebookBucketCampaign.objects.filter(id=campaign.id).update(is_contact=True)
				try:
					Contact.objects.bulk_update(contact_list,list(contact_obj.keys()),batch_size=100)
					temp_contacts = TempContactInfo.objects.filter(filter_query).distinct('previous_status').values('previous_status')
					for temp in temp_contacts:
						contact_id = list(TempContactInfo.objects.filter(filter_query).filter(previous_status=temp['previous_status']).values_list("contact_id",flat=True))
						Contact.objects.filter(id__in=contact_id).update(status=temp['previous_status'], modified_date=datetime.now())
						TempContactInfo.objects.filter(contact_id__in=contact_id).delete()
					if update_alt_numeric_list:
						AlternateContact.objects.bulk_update(update_alt_numeric_list,['alt_numeric'],batch_size=100)
					if created_alt_numeric_list:
						AlternateContact.objects.bulk_create(created_alt_numeric_list)
					if file_extension == '.csv':
						save_csv(cwd+"csv_files/proper_data"+file_extension, correct_list)
					else:
						save_xls(cwd+"csv_files/proper_data"+file_extension, correct_list)
					correct_file_path = "/csv_files/proper_data"+file_extension
					f = open(cwd+correct_file_path, 'rb')
					save_file_as = phone_inst.name+'-'+str(phone_inst.id)+"_"+"contact_file"+file_extension
					phone_inst.contact_file.save(save_file_as, File(f), save=True)
					phone_inst.last_updated_contact_count = correct_count
					phone_inst.save()
					f.close()
				except Exception as e:
					exc_type, exc_obj, exc_tb = sys.exc_info()
					fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					print(exc_type, fname, exc_tb.tb_lineno)
					print(e)
			if incorrect_count:
				try:
					if file_extension == '.csv':
						save_csv(cwd+"csv_files/improper_data"+file_extension, incorrect_list)
					else:
						save_xls(cwd+"csv_files/improper_data"+file_extension, incorrect_list)
					incorrect_file_path = "csv_files/improper_data"+file_extension   
					f = open(cwd+incorrect_file_path, 'rb')
					save_file_as = phone_inst.name+'-'+str(phone_inst.id)+"_"+"improper_data"+file_extension 				
					data_upload_log.improper_file.save(save_file_as, File(f), save=True)
					data_upload_log.incorrect_count = incorrect_count
					f.close()
				except Exception as e:
					print(e)
			PHONEBOOK_STATUS = {}
			PHONEBOOK_STATUS = pickle.loads(settings.R_SERVER.get("phonebook"))
			PHONEBOOK_STATUS['is_refresh'] = True
			if str(phone_inst.id) in PHONEBOOK_STATUS: 
				del PHONEBOOK_STATUS[''+str(phone_inst.id)+'']
			settings.R_SERVER.set("phonebook", pickle.dumps(PHONEBOOK_STATUS))

			phonebook_ids = list(Phonebook.objects.filter(campaign=campaign.id,status='Active').values_list('id',flat=True))
			phonebook_ids = list(map(str,phonebook_ids))
			if not set(phonebook_ids) & set(PHONEBOOK_STATUS.keys()):
				settings.R_SERVER.hset("pb_campaign_status",campaign.id, True)
			data_upload_log.save()
			transaction.commit()
			connections.close_all()
	except Exception as e:
		print("Exception occures from validate uploade phonebook",e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		settings.R_SERVER.hset("pb_campaign_status",kwarg["phone_inst"].campaign, True)
		return

def validate_uploaded_crm(data, crm_name):
	""" This is used to validate the uploaded crm data  """
	response_dict = {}
	if not data.empty:
		section_list = data.section_name.unique()
		incorrect_count = 0
		correct_count = 0
		incorrect_list = []
		correct_list = []
		duplicate_list = pd.DataFrame()
		wrong_section = pd.DataFrame()
		empty_section_priority_list = pd.DataFrame()
		non_numeric_section_list = pd.DataFrame()
		section_unique_field = []
		for section in section_list:
			if not ":" in section:
				section_data = data.loc[data['section_name'].isin([section])]
			   
				empty_section_priority = section_data[(section_data['section_priority'] != '' )].empty
				if empty_section_priority:
					empty_section_row = section_data[(section_data['section_priority'] == '' )]
					if len(section_data) == len(empty_section_row):
						empty_section_row["description"] = "Section priority is required"
						empty_section_priority_list = empty_section_priority_list.append(empty_section_row)
						section_pri_index_list = empty_section_row.index.tolist()
						section_data = section_data.drop(section_pri_index_list)

				non_numeric_section = section_data[~section_data['section_priority'].astype(str).str.isdigit()]
				if not non_numeric_section.empty and len(section_data) == len(non_numeric_section):
					non_numeric_section["description"] = "Section priority must be numeric"
					non_numeric_section_list = non_numeric_section_list.append(non_numeric_section)
					non_numeric_sec_list = non_numeric_section.index.tolist()
					section_data = section_data.drop(non_numeric_sec_list)      
				crmfield_dict = {}
				section_fields = []
				# sort data by field priority
				section_data = section_data.sort_values(by=['field_priority'])

				dummy_df = section_data[(section_data['field'] != '')]
				dup_dataframe = dummy_df[dummy_df.duplicated(
					['field'], keep='first')]
				duplicate_list = duplicate_list.append(dup_dataframe, sort=False)
				duplicate_list["description"] = "Field name is already exist"
				index_list = dup_dataframe.index.tolist()
				section_data = section_data.drop(index_list)

				crm_field = CrmField.objects.filter(name=crm_name.strip())
				ext_section = False
				if crm_field.exists():
					crm_field = crm_field.first()
					crm_fields = crm_field.crm_fields
					ext_section = next(
						(item["section_fields"] for item in crm_fields if item["section_name"] == section), False)

				for index, row in section_data.iterrows():
					field_name = row.get("field", "")
					field_exist = True
					error_dict = {}
					if ext_section != False:
						field_exist = next((item for item in ext_section if item["field"] == field_name), False)

					if field_exist not in [True, False]:
						error_dict["field_name"] = "This field is already exists in this crm"
										
					field_type = row.get("field_type", "")
					field_priority = row.get("field_priority", "")
					field_size = row.get("field_size", "")
					field_status = row.get("field_status", 'Active')
					editable = str(row.get("editable", "false"))
					unique_field=str(row.get("unique_field", "false"))
					if unique_field.lower() not in ['true', 'false']:
						error_dict["unique_field"] = "Unique field value should be true or false"
					elif unique_field and str(unique_field).lower() == "true" :
						if unique_field not in section_unique_field:
							section_unique_field.append(unique_field)
						else:
							error_dict["unique_field"] = "Only one uniqueid can be selected"	
					elif unique_field =="":
						error_dict["unique_field"] = "Unique field value must be true or false"

					if field_type.lower() in ["dropdown", "multiselect", "multicheckbox", "radio"]:
						options = row.get("options", "")
						if not options:
							error_dict["field_options"] = field_type + " required options"

					if field_priority.isdigit() == False:
						error_dict["field_priority"] = "It should be number"

					if ":" in field_name:
						error_dict["field_name"] = ": is not allowed in field name"

					if field_status.lower() not in ['active', 'inactive']:
						error_dict["field_status"] = "Field status should be active or inactive"

					if editable.lower() not in ['true', 'false']:
						error_dict["editable"] = "Editable value should be true or false"

					field_type_list = ['text', 'textarea', 'dropdown', 'multiselect', 'checkbox', 'multicheckbox',
									   'radio', 'integer', 'datefield', 'datetimefield', 'timefield','float']

					if field_type.lower() not in field_type_list:
						error_dict["field_type"] = "Field type should be from " + \
							", ".join(field_type_list)
					if field_type in ['text','textarea','integer']:
						if field_size and int(field_size) == 0:
							error_dict["field_size"] = "Size should not be 0"

					required_field_list = [
						field_name, field_type, field_priority]
					if not all(required_field_list):
						error_dict["field_error"] = "Missing field field name or field type or field priority or field size"

					if error_dict:
						incorrect_count = incorrect_count + 1
						row["description"] = json.dumps(error_dict)
						incorrect_data = pd.DataFrame(row).T
						incorrect_list.append(pd.DataFrame(row).T)
					else:
						correct_count = correct_count + 1
						correct_list.append(pd.DataFrame(row).T)
			else:
				wrong_sec = data.loc[data['section_name'] == section]
				wrong_section = wrong_section.append(wrong_sec)
		wrong_section["description"] = ": is not allowed in section name"
		incorrect_count = incorrect_count + len(wrong_section) + len(
			empty_section_priority_list) +len(non_numeric_section_list) +len(duplicate_list)
		if correct_count:
			with open(cwd+"csv_files/proper_data.csv", 'w', encoding='utf-8') as proper_file:
				for correct_row in correct_list:
					correct_row.to_csv(
						proper_file, index=False, header=proper_file.tell() == 0, encoding='utf-8')

			correct_file_path = "/static/csv_files/proper_data.csv"
			response_dict["correct_file"] = correct_file_path
			response_dict["correct_count"] = correct_count
		if incorrect_count:
			with open(cwd+"csv_files/improper_data.csv", 'w', encoding='utf-8') as improper_file:
				for incorrect_row in incorrect_list:
					incorrect_row.to_csv(
						improper_file, index=False, header=improper_file.tell() == 0)
				if not wrong_section.empty:
					wrong_section.to_csv(
						improper_file, index=False, header=improper_file.tell() == 0)

				if not empty_section_priority_list.empty:
					empty_section_priority_list.to_csv(
						improper_file, index=False, header=improper_file.tell() == 0)

				if not non_numeric_section_list.empty:
					non_numeric_section_list.to_csv(
						improper_file, index=False, header=improper_file.tell() == 0)
				if not duplicate_list.empty: 
					duplicate_list.to_csv(
						improper_file, index=False, header=improper_file.tell() == 0)
			incorrect_file_path = "/static/csv_files/improper_data.csv"
			response_dict["incorrect_file"] = incorrect_file_path
			response_dict["incorrect_count"] = incorrect_count
	else:
		response_dict["column_err_msg"] = 'File must not be empty'
	return response_dict

def truncate_file(file_name):
	f = open(file_name, "w")
	f.truncate()
	f.close()

def get_user_crm_data(user, app_label, model_name):
	""" this method is used to get the user crm data"""
	model = apps.get_model(app_label=app_label, model_name=model_name)
	if user.is_superuser:
		queryset = model.objects.all()
	else:
		queryset = model.objects.filter(created_by=user.username)
		if user.user_role.access_level.lower() == "admin":
			team = list(User.objects.filter(
				reporting_to=user).values_list("username"))
			queryset = model.objects.filter(created_by__in=team) | queryset
	return queryset

def connected_contact_status(request, add_crm_field):
	""" This is used to conneced contact status """
	contacts = []
	filter_by_phonebook = request.GET.get("phonebook", "")
	filter_by_campaign = request.GET.get("campaign", "")
	selected_columns = request.GET.getlist("selected_columns", [])
	if filter_by_campaign:
		contacts = Contact.objects.all()
	campaign_column = True

	if filter_by_phonebook:
		contacts = contacts.filter(phonebook=filter_by_phonebook)
	if filter_by_campaign:
		contacts = contacts.filter(phonebook__campaign=filter_by_campaign)

	# list of contact fields and crm field which ww have to displayed as selected if use has done some filteration
	if selected_columns:
		fields = [contact_field for contact_field in Contact._meta.get_fields() if contact_field.name not in [
			'contacts', 'id', 'site'] and contact_field.name in selected_columns]
		if add_crm_field:
			crm_fields = []
			for col in selected_columns:
				if col not in ['phonebook', 'user', 'numeric', 'alt_numeric', 'first_name', 'last_name', 'email', 'status']:
					crm_fields.append(col)
	else:
		fields = [contact_field for contact_field in Contact._meta.get_fields() if contact_field.name not in [
			'contacts', 'id', 'site']]
		crm_fields = []
		if add_crm_field and filter_by_campaign:
			campaign = Campaign.objects.get(id=filter_by_campaign).name
			crm_fields = get_customizable_crm_fields(campaign)
			crm_fields.append("campaign")

	# list of columns which user can select for customizing displayed columns list
	columns_list = [contact_field.name for contact_field in Contact._meta.get_fields() if contact_field.name not in [
		'contacts', 'id', 'site']]
	if add_crm_field:
		columns_list = columns_list + crm_fields
	if "campaign" not in crm_fields:
		columns_list.append("campaign")
	
	# list of phonebook and campaign on which we have to filter
	phonebook = list(Phonebook.objects.values(
		"id", "name", "campaign", "status"))
	campaign_list = Campaign.objects.values("name", "id")
	page_info = data_for_pagination(request)
	data = {"request": request, "fields": fields,
			"phonebook_list": phonebook, "campaign_list": campaign_list, "selected_columns": selected_columns,
			"columns_list": set(columns_list), "selected_phonebook": filter_by_phonebook,
			"selected_campaign": filter_by_campaign, "campaign_column": campaign_column, **page_info}
	if add_crm_field:
		data["crm_fields"] = crm_fields
	if contacts:
		data["contact_list"] = list(contacts.values_list("id", flat=True))
	data["contacts"] = contacts
	contacts = get_paginated_object(contacts, page_info["page"], page_info["paginate_by"])
	data["queryset"]= contacts
	return data

def get_customize_customer_data(raw_data):
	"""
	This function is used to customize customer info
	according to section and fields
	"""
	section_list = []
	for key in raw_data.keys():
		section = key
		# section = key.split("-")[0]
		if section not in section_list:
			section_list.append(section)
	section_wise_list = []
	for section in section_list:
		section_dict = {}
		section_dict["section_name"] = section
		section_dict["section"] = section.replace("_", " ")
		section_dict["data"] = []
		for contact_data in raw_data:
			temp_dict = {}
			if section == contact_data.split("-")[0]:
				temp_dict[contact_data.split("-")[1]] = raw_data[contact_data]
			if temp_dict:
				section_dict["data"].append(temp_dict)
		section_wise_list.append(section_dict)
	return section_wise_list

def upload_crm(request_data):
	"""
	This function will upload crm data to crmfield
	"""
	proper_file = request_data.POST.get("proper_file", "")
	improper_file = request_data.POST.get("improper_file", "")
	perform_upload = request_data.POST.get("perform_upload", "")
	cwd = settings.BASE_DIR
	if perform_upload:
		if proper_file.endswith('.csv'):
			data = pd.read_csv(cwd+proper_file, na_filter=False, dtype = {"section_priority" : "str", "field_size": "str",
				"field_priority":"str"})
		else:
			data = pd.read_excel(cwd+proper_file)
			
		crmfield_list = []
		crm_name = request_data.POST.get("name", "")
		campaign = request_data.POST.getlist("campaign[]", "")
		camp_info_list = []
		for camp in campaign:
			camp_info, created = CampaignInfo.objects.get_or_create(
				name=camp.strip())
			camp_info_list.append(camp_info)

		section_list = data.section_name.unique()
		unique_field_list = []
		crm_field_inst, created = CrmField.objects.get_or_create(name=crm_name)
		for section in section_list:
			if not created:
				ext_section = True
				abc = crm_field_inst.crm_fields
				ext_section = next(
					(item for item in abc if item["section_name"] == section), False)
				section_data = data.loc[data['section_name'].isin([section])]
				crmfield_dict = {}
				if ext_section == False:
					crmfield_dict["section_name"] = section
					crmfield_dict["db_section_name"] = re.sub(' +', ' ',section.strip()).replace(" ","_").lower()
					crmfield_dict["section_priority"] = section_data[section_data['section_priority'].astype(
						str).str.isdigit()].iloc[0]["section_priority"]
				else:
					ext_section["section_priority"] = str(
						data.iloc[0].section_priority)
			else:
				section_data = data.loc[data['section_name'].isin([section])]
				crmfield_dict = {}
				crmfield_dict["section_name"] = section
				crmfield_dict["db_section_name"] = re.sub(' +', ' ',section.strip()).replace(" ","_").lower()
				crmfield_dict["section_priority"] = section_data[section_data['section_priority'].astype(
						str).str.isdigit()].iloc[0]["section_priority"]

			section_fields = []
			# sort data by field priority
			section_data = section_data.sort_values(by=['field_priority'])
			for index, row in section_data.iterrows():
				field_name = row.get("field", "")
				db_field = re.sub(' +', ' ',field_name.strip()).replace(" ","_").lower()
				field_type = row.get("field_type", "")
				if field_type:
					field_type = field_type.lower()
				field_priority = str(row.get("field_priority", ""))
				field_size = str(row.get("field_size", ""))
				field_status = row.get("field_status", 'Active')
				editable = row.get("editable", "false")
				#required = row.get("mandatory", "false")
				unique_field=str(row.get("unique_field", "false"))
				unique_field_val = False
				if unique_field.lower() == 'true':
					unique_field_val = True
					unique_field_list.append(crmfield_dict["db_section_name"]+":"+db_field)
				if all([field_name, field_type, field_priority, field_size]):
					section_field = {"field": field_name, "db_field":db_field,
						"field_type": field_type, "size": field_size,"options": row.get("options", ""),
						"editable": editable,"field_status":field_status.title(),"priority": field_priority, "unique":unique_field_val}

					section_fields.append(section_field)
			if not created:
				if ext_section == False:
					crmfield_dict["section_fields"] = section_fields
				else:
					ext_sec_fields = []
					ext_sec_fields = ext_section["section_fields"]
					ext_sec_fields.extend(section_fields)
					ext_section["section_fields"] = ext_sec_fields

					crm_field_inst.crm_fields = abc
					crm_field_inst.save()
			else:
				crmfield_dict["section_fields"] = section_fields

			if crmfield_dict:
				crmfield_list.append(crmfield_dict)
		crmfield_list = crmfield_list

		if created:
			crm_field_inst.crm_fields = crmfield_list
		else:
			inst_crm_fields = crm_field_inst.crm_fields
			inst_crm_fields.extend(crmfield_list)
			crm_field_inst.crm_fields = inst_crm_fields
		crm_field_inst.campaign.add(*camp_info_list)
		crm_field_inst.created_by = request_data.user.username
		crm_field_inst.unique_fields =unique_field_list
		crm_field_inst.save()
	if proper_file:
		os.remove(cwd+proper_file)
	if improper_file:
		os.remove(cwd+improper_file)
	return {"msg": "crm upload functionality"}

def download_contactinfo_csv(queryset, serializer_class, columns_list,columns_title, pseudo_buffer):
	""" This is used to save the contact info into csv file """
	writer = csv.writer(pseudo_buffer)
	yield writer.writerow(columns_title)

	for c_info in queryset.iterator():
		row = []
		data = serializer_class(c_info).data
		for field in columns_list:
			field = field.split('.')
			if len(field) > 1:
				if field[1] in data['contact_info']:
					if field[2] in data['contact_info'][field[1]]: 
						row.append(data['contact_info'][field[1]][field[2]])
					else:
						row.append('')
				else:
					row.append('')
			else:
				row.append(data.get(field[0],''))
		yield writer.writerow(row)

def download_crmfields_csv(request,crm_data):
	""" This is used to get the sample crm fields file and fields """
	response = HttpResponse(content_type='text/force-download')
	response['Content-Disposition'] = 'attachment; filename="crm-fields.csv"'
	writer = csv.writer(response)
	writer.writerow(('section_name','section_priority','field_size','field','options','editable',
		'field_priority','field_type','field_status','unique_field'))
	for crm in crm_data:
		for columns in crm['section_fields']:
			data=[]
			data.append(crm['section_name'])
			data.append(crm['section_priority'])
			data.append(columns['size'])
			data.append(columns['field'])
			data.append(columns['options'])
			data.append(columns['editable'])
			data.append(columns['priority'])
			data.append(columns['field_type'])
			data.append(columns['field_status'])
			data.append(columns['unique'])
			writer.writerow(data)
	return response

def create_alt_num_dict(alt_numeric, existing_alt_num):
	""" This is used to create and alternative number dict to store"""
	try:
		alt_numeric = alt_numeric.split(',')
		alt_num_dict = existing_alt_num.copy()
		for index, num in enumerate(alt_numeric):
			num_data = num.split(':')
			if len(num_data) > 1:
				if num_data[1].strip().isdigit():
					if num_data[1].strip() not in alt_num_dict.values():
						if num_data[0].strip() not in alt_num_dict.keys():
							alt_num_dict[num_data[0].strip()] = num_data[1].strip()
						else:
							key_count = 1
							temp_alt_name_key = num_data[0].strip()+'_'+str(key_count)
							while temp_alt_name_key in alt_num_dict.keys():
								key_count +=1
								temp_alt_name_key = num_data[0].strip()+'_'+str(key_count)
							alt_num_dict[temp_alt_name_key] = num_data[1].strip()
					else:
						position = list(alt_num_dict.values()).index(num_data[1].strip())
						del_key = list(alt_num_dict.keys())[position]
						del alt_num_dict[del_key]
						if num_data[0].strip() not in alt_num_dict.keys():
							alt_num_dict[num_data[0].strip()] = num_data[1].strip()
						else:
							key_count = 1
							temp_alt_name_key = num_data[0].strip()+'_'+str(key_count)
							while temp_alt_name_key in alt_num_dict.keys():
								key_count +=1
								temp_alt_name_key = num_data[0].strip()+'_'+str(key_count)
							alt_num_dict[temp_alt_name_key] = num_data[1].strip()
			elif len(num_data) and len(num_data)==1:
				if num.strip().isdigit() and num.strip() not in alt_num_dict.values():
					key_count = len(alt_num_dict.keys())
					temp_alt_name_key = 'alt_num_'+str(key_count)
					while temp_alt_name_key in alt_num_dict.keys():
						key_count +=1
						temp_alt_name_key = 'alt_num_'+str(key_count)
					alt_num_dict[temp_alt_name_key] = num.strip()
		return alt_num_dict
	except Exception as e:
		print('Error in create_alt_num_dict: ',e)
		return existing_alt_num


def get_customizable_crm_fields_for_template(campaign_name):
	""" This is used to get the crm fields for the template """
	column_list = []
	if Campaign.objects.filter(name=campaign_name).exists():
		campaign = Campaign.objects.get(name=campaign_name)
		crm_fields = CrmField.objects.filter(campaign__name=campaign_name)
		for crm_field in crm_fields:
			sections = sorted(crm_field.crm_fields, key = lambda i: i['section_priority'])
			for section in sections:
				section_name = section["db_section_name"]
				section_fields = sorted(section["section_fields"], key = lambda f: f['priority'])
				for section_field in section_fields:
					column_list.append("${"+section_name+":"+section_field["db_field"]+"}")
	return column_list