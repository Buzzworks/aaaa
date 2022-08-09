import os,re
import pickle
import os.path
from functools import reduce
from os import path
from django.apps import apps
from django.conf import settings
cwd = os.path.join(settings.BASE_DIR, 'static/')
from django.shortcuts import render
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse, JsonResponse
from django.db.models import Q, F
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from rest_framework_xml.parsers import XMLParser
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, AllowAny,IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics
from scripts.pagination import DatatablesPageNumberPagination
from scripts.renderers import DatatablesRenderer
from crm.s3_fileoperations import *

from io import BytesIO
import pandas as pd
import numpy as np
import json
import louie
import copy

from .models import (Status, Contact, Phonebook, CrmField,
	Contact, ContactInfo, CampaignInfo, TempContactInfo, LeadListPriority, DownloadReports, TrashContact, PhoneBookUpload, AlternateContact,ScheduleMasterContact)
from callcenter.models import (AdminLogEntry,Campaign,User, CallDetail, CSS,Disposition, DataUploadLog,PhonebookBucketCampaign, StickyAgent, UserVariable)
from flexydial.constants import (Status, CONTACT_STATUS, FIELD_CHOICES, ORDER_BY, SEARCH_TYPE)

from .serializers import (PhoneBookSerializer, CrmFieldSerializer, SetContactSerializer,
		AgentCrmFieldSerializer,ContactListSerializer, PhonebookRefreshSerializer,CrmFieldCustomSerializer,
		CrmFieldPaginationSerializer, LeadListPrioritySerializer, DownloadReportsSerializer,ContactSerializer, EditContactListSerializer,ScheduleMasterContactSerializer)
from callcenter.serializers import DispositionSerializer
# from flexydial.views import check_permission

from .utility import (save_contact, validate_uploaded_phonebook, truncate_file,
	connected_contact_status, get_crm_fields, get_customizable_crm_fields,
	get_customize_customer_data, get_user_crm_data, upload_crm, validate_uploaded_crm,download_contactinfo_csv,
	download_crmfields_csv, crm_field_value_schema,get_customizable_crm_fields_with_datatype,crm_field_datatype_validation)
from callcenter.utility import (get_object, create_agentactivity, get_formatted_agent_activities,
	get_model_data,set_agentReddis,get_report_visible_column, get_campaign_users, check_non_admin_user,get_agent_status,set_agent_status,get_all_keys_data)
from callcenter.decorators import (check_read_permission,
		check_create_permission, check_update_permission,
		)
from .decorators import (crm_field_validation,phonebook_validation)

from flexydial.views import (csvDownload, data_for_pagination,data_for_vue_pagination, get_paginated_object, get_active_campaign, create_admin_log_entry,user_hierarchy_func)
from crm.models import Phonebook
from datetime import datetime
import dateutil.parser
from callcenter.signals import (
	aps_phonebook_upload
	)
import csv

def check_data_with_uniue_id(uniqueid):
	""" Check the Data is present with the crm uniqueid"""
	section_name = uniqueid.split(":")[0]
	field_name = uniqueid.split(":")[1]
	query_string = "customer_raw_data__"+section_name+"__"+field_name
	none_query_dict = blank_query_dict = {}
	none_query_dict[query_string] = None
	blank_query_dict[query_string] = ""
	contact_count = ContactInfo.objects.filter(~Q(**none_query_dict)|~Q(**blank_query_dict)).count()
	unique_field_exist = "false"
	if contact_count > 0:
		unique_field_exist = "true"
	return unique_field_exist

class Echo(object):
	def write(self, value):
		return value

@method_decorator(check_read_permission, name='get')
class CrmListApiView(LoginRequiredMixin, generics.ListAPIView):
	"""
	This view is used to display list of phonebook
	"""
	renderer_classes = [TemplateHTMLRenderer]
	template_name    = "phonebook/phonebook.html"
	login_url = '/'

	def get(self,request, **kwargs):
		page_info = data_for_pagination(request)
		refresh_cell = request.GET.get("refresh_cell", "")
		queryset = Phonebook.objects.all()
		if check_non_admin_user(request.user):
			user_campaigns = Campaign.objects.filter(Q(users=request.user)|Q(group__in=request.user.group.all())|Q(created_by=request.user)).distinct().values_list('id',flat=True)
			queryset = queryset.filter(campaign__in=list(user_campaigns))
		if page_info["search_by"] and page_info["column_name"]:
			if page_info["column_name"] == "campaign":
				campaign = Campaign.objects.filter(
					name__istartswith=page_info["search_by"]).values_list("id", flat=True)
				if campaign:
					queryset = queryset.filter(
						**{page_info["column_name"]+"__in": list(campaign)})
				else:
					queryset =Phonebook.objects.none()
			else:
				queryset = queryset.filter(**{page_info["column_name"]+"__istartswith": page_info["search_by"]})
		phonebook_ids = list(queryset.values_list("id", flat=True))
		queryset = get_paginated_object(queryset, page_info["page"], page_info["paginate_by"])
		pagination_dict = data_for_vue_pagination(queryset)
		paginate_by_columns = (('name', 'Phonebook Name'),
			('campaign', 'Campaign'),
			)
		camp_name, active_camp, noti_count = get_active_campaign(request)
		context = { "id_list": phonebook_ids, "paginate_by_columns":paginate_by_columns,
		"noti_count":noti_count,'web_socket_host':settings.WEB_SOCKET_HOST}
		context = {**context, **kwargs['permissions'], **page_info, **pagination_dict}
		if request.is_ajax():
			result = list(PhonebookRefreshSerializer(queryset, many=True).data)
			pagination_dict["table_data"] = result
			context = {**context, **kwargs['permissions'], **pagination_dict}
			return JsonResponse(context)
		else:
			context = {**context, **kwargs['permissions'], **pagination_dict}
			context['request']: request
			return Response(context)


@method_decorator(check_create_permission, name='get')
@method_decorator(phonebook_validation,name='post')
class CrmCreatePhonebookApiView(LoginRequiredMixin, APIView):
	'''
	This api is used to display a create phonebook page
	and create phonebook page
	'''
	renderer_classes = [TemplateHTMLRenderer]
	template_name    = "phonebook/phonebook_create.html"
	serializer       = PhoneBookSerializer
	login_url = '/'

	def get(self, request, format=None, **kwargs):
		campaign = Campaign.objects.values("id", "name", "portifolio")
		if check_non_admin_user(request.user):
			campaign = campaign.filter(Q(users=request.user)|Q(group__in=request.user.group.all())|Q(created_by=request.user)).distinct()
		context = {'request':request, 'campaign':campaign, 'auto_churn_status':Status, 'campaign_status':Status, 'order_by':ORDER_BY, 'search_type':SEARCH_TYPE}
		context = {**context, **kwargs['permissions']}
		return Response(context)

	def post(self, request, pk=""):
		cwd = settings.BASE_DIR
		if self.kwargs.get("pk", ""):
			phonebook = get_object(pk, "crm", "Phonebook")
			phonebook_serializer = self.serializer(phonebook, data=request.data)
			PHONEBOOK_STATUS = {}
			PHONEBOOK_STATUS = pickle.loads(settings.R_SERVER.get("phonebook") or pickle.dumps(PHONEBOOK_STATUS))
			if PHONEBOOK_STATUS:
				if str(phonebook.id) in PHONEBOOK_STATUS:
					return JsonResponse({"errors":"Data Uploading For This Process Is Going On. You Can Not Update The Phonebook In This Time"}, status=500)
		else:
			phonebook_serializer = self.serializer(data=request.data)
		phonebook_name = request.data.get("name", "")
		expire_date = request.data.get("expire_date","")
		update_camp = False
		phone_inst = Phonebook.objects.filter(name=phonebook_name)
		ex_camp = 0
		if phonebook_serializer.is_valid():
			if phone_inst.exists():
				ex_camp = phone_inst.first().campaign
				if  request.POST.get("campaign", "") != phone_inst.first().campaign:
					update_camp = True
					camp_name = Campaign.objects.get(id=request.POST.get("campaign", "")).name
				if update_camp or not str(request.POST.get("order_by", "")) == str(phone_inst.first().order_by) or not str(request.POST.get("priority", "")) == str(phone_inst.first().priority):
					if update_camp:
						Contact.objects.filter(phonebook_id=phone_inst.first().id).update(campaign=camp_name)
					if TempContactInfo.objects.filter(phonebook_id=phone_inst.first().id).exists():
						tempcontcat = TempContactInfo.objects.filter(phonebook_id=phone_inst.first().id, status='NotDialed')
						for temp in tempcontcat:
							Contact.objects.filter(id=temp.contact_id, phonebook_id=phone_inst.first().id).update(status=temp.previous_status)
						tempcontcat.delete()
			PhonebookBucketCampaign.objects.filter(id=request.POST.get("campaign", "")).update(is_contact=True)
			uploaded_file = request.FILES.get("uploaded_file", "")
			if uploaded_file:
				phonebook_columns = ['numeric', 'first_name']
				duplicate_check = request.POST.get("duplicate_check", "")
				action_type = request.POST.get("action_type","")
				search_type = request.POST.get("search_type","")
				campaign = request.POST.get("campaign", None)
				if uploaded_file.name.endswith('.csv'):
					data = pd.read_csv(uploaded_file, na_filter=False, encoding = "unicode_escape", escapechar='\\',
						dtype = {"numeric" : "str", "alt_numeric": "str","customer_info:loan_account_number": "str"},)
				else:
					data = pd.read_excel(uploaded_file, encoding = "unicode_escape",
						converters={'numeric': str,'customer_info:loan_account_number':str})
					data = data.replace(np.NaN, "")
				column_names = data.columns.tolist()
				if action_type == 'update':
					valid = True if duplicate_check in column_names else False
				else:
					valid = all(elem in column_names for elem in phonebook_columns)
				if valid:
					if not data.empty:
						if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, 'upload/')):
							os.makedirs(settings.MEDIA_ROOT+'/upload')
						if os.access(os.path.join(settings.MEDIA_ROOT, 'upload/'),os.W_OK | os.X_OK) == True:
							if phone_inst.exists():
								if not request.POST.get("campaign", "") == phone_inst.first().campaign:
									update_camp = True
							phone_inst = phonebook_serializer.save(created_by=request.user.username)
							camp_name = Campaign.objects.get(id=request.POST.get("campaign", "")).name
							if update_camp:
								Contact.objects.filter(phonebook=phone_inst).update(campaign=camp_name)
							PhoneBookUpload.objects.create(phone_inst=phone_inst, duplicate_check=duplicate_check, action_type=action_type, search_type=search_type, column_names=column_names, created_by=request.user, phonebook_file=uploaded_file)
							job_id = phone_inst.campaign.replace(" ", "")+phone_inst.name.replace(" ", "")+str(phone_inst.id)
							job_id_check = list(set(DataUploadLog.objects.filter(job_id=job_id).values_list('job_id', flat=True)))
							if job_id_check:
								DataUploadLog.objects.filter(job_id__in=job_id_check).delete()
							data_upload_log, _ = DataUploadLog.objects.get_or_create(job_id=job_id)
							total_data = len(data)
							data_upload_log.status = 0
							data_upload_log.save()
							return JsonResponse({"msg":"Data will upload very soon"})
						else:
							response_data = {}
							response_data["errors"] = 'Permission Denied'
							response_data["column_id"] = "#phonebook-err-msg"
							return JsonResponse(response_data, status=500)
					else:
						return JsonResponse({"errors":"File should not be empty"}, status=500)
				else:
					response_data = {}
					if action_type == 'update':
						response_data["errors"] = 'File must contains '+duplicate_check+' column'
					else:
						response_data["errors"] = 'File must contains these '+','.join(phonebook_columns)+' columns'
					response_data["column_id"] = "#phonebook-err-msg"
					return JsonResponse(response_data, status=500)
			else:
				phone_inst = phonebook_serializer.save(created_by=request.user.username)
				if update_camp:
					phonebook_ext_contact = Contact.objects.filter(campaign=Campaign.objects.get(id=ex_camp)).count()
					if phonebook_ext_contact == 0:
						PhonebookBucketCampaign.objects.filter(id=ex_camp).update(is_contact=False)
					phonebook_ext_contact = Contact.objects.filter(campaign=request.POST.get("campaign", "")).count()
					if phonebook_ext_contact == 0:
						PhonebookBucketCampaign.objects.filter(id=request.POST.get("campaign", "")).update(is_contact=True)
			if phone_inst.status == 'Inactive':
				if TempContactInfo.objects.filter(phonebook=phone_inst).exists():
					tempcontact = TempContactInfo.objects.filter(phonebook=phone_inst, status='NotDialed')
					for temp in tempcontact:
						Contact.objects.filter(id=temp.contact_id, phonebook=phone_inst).update(status=temp.previous_status)
					tempcontact.delete()
			if pk:
				create_admin_log_entry(request.user, "phonebook","2",'UPDATED',phone_inst.name)
			else:
				create_admin_log_entry(request.user, "phonebook","1",'CREATED',phone_inst.name)
		return Response()

class BulkTransferContactApiView(APIView):
	""" Transfer the bulk contact to other user """
	def post(self, request, pk, format=None):
		phonebook = get_object(pk, "crm", "Phonebook")
		uploaded_file = request.FILES.get("uploaded_file", "")
		search_type = request.POST.get("search_type","")
		campaign = Campaign.objects.get(id=phonebook.campaign)
		if search_type == '0':
			query = Q(phonebook=phonebook, status='NotDialed')
		elif search_type == '1':
			query = Q(campaign=campaign.name, status='NotDialed')
		else:
			query = Q(status='NotDialed')
		if uploaded_file:
			if uploaded_file.name.endswith('.csv'):
				data = pd.read_csv(uploaded_file, na_filter=False, encoding = "unicode_escape", escapechar='\\')
			else:
				data = pd.read_excel(uploaded_file, encoding = "unicode_escape")
			if not data.empty:
				for index, row in data.iterrows():
					from_agent = row["from_agent"]
					to_agent = row["to_agent"]
					if from_agent and to_agent:
						temp_contacts = TempContactInfo.objects.filter(query, user=from_agent)
						temp_contact_id = list(temp_contacts.values("id", "previous_status"))
						temp_contacts.delete()
						for temp in temp_contact_id:
							Contact.objects.filter(id=temp['id']).update(user=to_agent,status=temp['previous_status'])
						contacts = Contact.objects.filter(query, user=from_agent)
						contacts.update(user=to_agent)
						from_agent = User.objects.get(username=from_agent)
						to_agent = User.objects.get(username=to_agent)
						phonebook_campaign = phonebook.campaign
						StickyAgent.objects.filter(agent=from_agent, campaign__name=phonebook_campaign).update(agent=to_agent)
				phonebook.transfer_contact_file = uploaded_file
				phonebook.save()
				return JsonResponse({"msg":"Contacts transfered successfully"})
		return JsonResponse({"errors":"select file to upload"}, status=500)


class BulkDeleteContactApiView(APIView):
	"""
	This api is used to display detail of particular
	phonebook
	"""
	def post(self, request):
		phonebook_id = request.POST.get("phonebook_id","")
		crmfield = request.POST.get("crm_field_val","")
		summery = request.POST.get("summery","")
		total_contacts = all_contact_count = 0
		alternate_numbers = []
		if summery:
			all_contact_count = Contact.objects.filter(phonebook_id=phonebook_id).count()
		if phonebook_id:
			phonebook = get_object(phonebook_id, "crm", "Phonebook")
			uploaded_file = request.FILES.get("uploaded_file", "")
			if uploaded_file:
				if uploaded_file.name.endswith('.csv'):
					data = pd.read_csv(uploaded_file, na_filter=False, encoding = "unicode_escape", escapechar='\\')
				else:
					data = pd.read_excel(uploaded_file, encoding = "unicode_escape", dtype='object')
				data = data.astype(str)
				# if crmfield in data.columns:
				crmfield = list(data.columns)
				if crmfield:
					crmfield = crmfield[0]
					val_list = data[crmfield].tolist()
					contact_list = ["numeric","status","priority","uniqueid","disposition"]
					if crmfield in contact_list:
						if crmfield == "status":
							val_list = [i for i in val_list]
							contact_delete = Contact.objects.filter(status__in=val_list, phonebook_id=phonebook_id).values_list("id",flat=True)
						elif crmfield == "priority":
							data[crmfield] = pd.to_numeric(data[crmfield],errors='coerce')
							data = data.replace(np.nan, 0, regex=True)
							val_list = data[crmfield].tolist()
							contact_delete = Contact.objects.filter(priority__in=val_list, phonebook_id=phonebook_id).values_list("id",flat=True)
						elif crmfield == "disposition":
							query = reduce(lambda q,value: q|Q(disposition__iexact=value), val_list, Q())
							contact_delete = Contact.objects.filter(query).filter(phonebook_id=phonebook_id).values_list("id",flat=True)
						else:
							dummy_dict = {}
							dummy_dict[crmfield+"__in"]=val_list
							contact_delete = Contact.objects.filter(**dummy_dict).filter(phonebook_id=phonebook_id).values_list("id",flat=True)
					else:
						field_data_type = None
						crmfield = crmfield.replace(":","__")
						crmfield_split = crmfield.split('__',2)
						c_val = CrmField.objects.filter(campaign__name=Campaign.objects.get(id=int(Phonebook.objects.get(id=phonebook_id).campaign))).values('crm_fields')
						for crm in c_val:
							for crm_section in crm['crm_fields']:
								if crm_section['db_section_name'] == crmfield_split[0]:
									for item in crm_section['section_fields']:
										if item['db_field'] == crmfield_split[1]:
											field_data_type = item['field_type']
						dummy_dict = {}
						crm_field_date = "customer_raw_data__"+crmfield+"__icontains"
						crmfield = "customer_raw_data__"+crmfield+"__in"
						dummy_dict[crmfield]=list(val_list)
						dummy_dict["phonebook_id"] = phonebook.id
						if field_data_type in ['datefield', 'datetimefield']:
							try:
								contact_delete= []
								dummy_crm_dict = {}
								for fields in val_list:
									dummy_crm_dict[crm_field_date]=fields
									contact_val = Contact.objects.filter(**dummy_crm_dict).values_list("id", flat=True)
									contact_delete.append(contact_val)
							except Exception as e:
								print(e)
						else:
							contact_delete = Contact.objects.filter(**dummy_dict).values_list("id", flat=True)
					if type(contact_delete) != list:
						if contact_delete.exists() and not summery:
							TempContactInfo.objects.filter(id__in=contact_delete).delete()
							contacts = Contact.objects.filter(id__in=contact_delete)
							numbers = contacts.values_list("numeric",flat=True)
							TrashContact.objects.filter(numeric__in=numbers).delete()
							trash_contacts=[]
							for contact in contacts:
								trash_contacts.append(TrashContact(phonebook=contact.phonebook.name, user=contact.user, numeric=contact.numeric,
									alt_numeric=contact.alt_numeric, first_name=contact.first_name, last_name=contact.last_name, email=contact.email,
									disposition=contact.disposition, status=contact.status, customer_raw_data=contact.customer_raw_data))
								# if contact.alt_numeric:
								# 	alternate_numbers.append(AlternateContact(numeric=contact.numeric, uniqueid=contact.uniqueid, alt_numeric=contact.alt_numeric))
							# AlternateContact.objects.bulk_create(alternate_numbers)
							TrashContact.objects.bulk_create(trash_contacts)
							contacts.delete()
					else:
						if len(contact_delete) >0 and not summery:
							for contact_delete_date in contact_delete:
								TempContactInfo.objects.filter(id__in=contact_delete_date).delete()
								contacts = Contact.objects.filter(id__in=contact_delete_date)
								numbers = contacts.values_list("numeric",flat=True)
								TrashContact.objects.filter(numeric__in=numbers).delete()
								trash_contacts=[]
								for contact in contacts:
									trash_contacts.append(TrashContact(phonebook=contact.phonebook.name, user=contact.user, numeric=contact.numeric,
										alt_numeric=contact.alt_numeric, first_name=contact.first_name, last_name=contact.last_name, email=contact.email,
										disposition=contact.disposition, status=contact.status, customer_raw_data=contact.customer_raw_data))
									# if contact.alt_numeric:
									# 	alternate_numbers.append(AlternateContact(numeric=contact.numeric, uniqueid=contact.uniqueid, alt_numeric=contact.alt_numeric))
								# AlternateContact.objects.bulk_create(alternate_numbers)
								TrashContact.objects.bulk_create(trash_contacts)
								contacts.delete()
					if summery:
						if type(contact_delete) == list:
							total_contacts = len(contact_delete)
						else:
							total_contacts = contact_delete.count()
						return JsonResponse({"total_contacts":total_contacts, "all_contact_count": all_contact_count})
				else:
					return JsonResponse({"msg":"File must contain column"}, status=500)
				phonebook.deleted_contact_file=uploaded_file
				phonebook.save()

		return JsonResponse({"msg":"data deleted"}, status=200)


@method_decorator(check_update_permission, name='get')
class CrmEditPhonebookApiView(LoginRequiredMixin,APIView):
	"""
	This api is used to display detail of particular
	phonebook
	"""
	login_url = '/'
	renderer_classes = [TemplateHTMLRenderer]
	template_name    = "phonebook/phonebook_edit.html"
	serializer = PhoneBookSerializer

	def get(self, request, pk, format=None, **kwargs):
		phonebook = get_object(pk, "crm", "Phonebook")
		campaign = Campaign.objects.values("id", "name", "portifolio")
		context = {'request':request, 'campaign':campaign, 'is_edit': True,
			'auto_churn_status':Status, 'campaign_status':Status,
			'phonebook': phonebook, 'order_by':ORDER_BY,'search_type':SEARCH_TYPE
			}
		curr_campaign_name = Campaign.objects.filter(id=phonebook.campaign).values_list('name',flat=True).first()
		# AGENTS = get_all_keys_data()
		campaign_pd = pickle.loads(settings.R_SERVER.get("campaign_status") or pickle.dumps({}))
		if curr_campaign_name in campaign_pd and len(campaign_pd[curr_campaign_name])>0:
			context['is_edit'] = False
		# if AGENTS:
		# 	all_agents = list(AGENTS.keys())
		# 	for extension in all_agents:
		# 		if str(extension) in AGENTS and AGENTS[str(extension)]['campaign']==curr_campaign_name:
		# 			context['is_edit'] = False
		# 			break
		context = {**context, **kwargs['permissions']}
		return Response(context)

class CrmPhonebookStatusApiView(APIView):
	"""
	This api is written to get phonebook status
	"""
	def get(self, request):
		PHONEBOOK_STATUS ={}
		PHONEBOOK_STATUS = pickle.loads(settings.R_SERVER.get(request.GET['key']) or pickle.dumps(PHONEBOOK_STATUS))
		if 'is_refresh' in request.GET:
			if request.GET['is_refresh']=='true' and PHONEBOOK_STATUS['is_refresh']:
				PHONEBOOK_STATUS['is_refresh'] = False
				settings.R_SERVER.set(request.GET['key'], pickle.dumps(PHONEBOOK_STATUS))

		return Response(PHONEBOOK_STATUS)

class ValidatePhoneBookUploadApiView(APIView):
	"""
	This api is written to validate bulk contacts upload for phonebook
	"""

	def post(self, request):
		user_file = request.FILES.get("uploaded_file", "")
		phonebook_columns = ['numeric', 'first_name']
		duplicate_check = request.POST.get("duplicate_check", "")
		campaign = request.POST.get("campaign", None)
		is_xls = False
		if user_file:
			if user_file.size <= 1:
				response_data = {}
				response_data["column_err_msg"] = 'File must not be empty'
				response_data["column_id"] = "#phonebook-err-msg"
			else:
				if user_file.name.endswith('.csv'):
					data = pd.read_csv(user_file, na_filter=False,
							dtype = {"numeric" : "str", "alt_numeric": "str"})
				else:
					data = pd.read_excel(user_file, encoding = "unicode_escape",
						converters={'numeric': str})
					is_xls = True
					data = data.replace(np.NaN, "")
				column_names = data.columns.tolist()
				valid = all(elem in column_names for elem in phonebook_columns)
				if valid:
					if os.access(os.path.join(settings.MEDIA_ROOT, 'upload/'),os.W_OK | os.X_OK) == True:
						response_data = validate_uploaded_phonebook(data=data, campaign=campaign, duplicate_check=duplicate_check, is_xls=is_xls)
					else:
						response_data = {}
						response_data["errors"] = 'Permission Denied For Media Folder'
						response_data["column_id"] = "#phonebook-err-msg"
						return JsonResponse(response_data, status=500)
				else:
					response_data = {}
					response_data["column_err_msg"] = 'File must contains these '+','.join(phonebook_columns)+' columns'
					response_data["column_id"] = "#phonebook-err-msg"

		return Response(response_data)


class GetSamplePhonebookApiView(APIView):
	"""
	This api is written to get sample phonebook file from selected campaign
	"""

	def post(self, request):
		column_list = []
		campaign_name = request.POST.get("campaign", "")
		user_campaign = Campaign.objects.all()
		if user_campaign.filter(name=campaign_name).exists():
			campaign = user_campaign.objects.get(name=campaign_name)
			crm_fields = CrmField.objects.filter(campaign__name=campaign_name, status="Active")
			for crm_field in crm_fields:
				sections = json.loads(crm_field.crm_fields)
				for section in sections:
					section_fields = section["section_fields"]
					for section_field in section_fields:
						column_list.append(section_field["field"])
			cols = ['numeric','alt_number','first_name','last_name','email']
			customs_cols = list(set(column_list))
			cols = cols + customs_cols
			if campaign.portifolio:
				file_name = cwd + 'csv_files/sample_phonebook_file_with_user.csv'
				final_file = '/static/csv_files/sample_phonebook_file_with_user.csv'
			else:
				file_name = cwd + 'csv_files/sample_phonebook_file.csv'
				final_file = '/static/csv_files/sample_phonebook_file.csv'
			truncate_file(file_name)
			if campaign.portifolio:
				cols.insert(0, 'user')
			data = pd.read_csv(file_name, na_filter=False, index_col=0, names=cols)
			data.to_csv(file_name)

		return JsonResponse({"file_name":final_file})


class GetDispoAPIView(LoginRequiredMixin, APIView):
	""" Get the dispostion and the values according to the campaign """
	login_url = '/'
	def post(self, request):
		context = {}
		campaign_id = request.POST.getlist("campaign_id[]")
		camp_list =  Campaign.objects.filter(id__in=campaign_id)
		dispo = []
		for camp in camp_list:
			dispo.extend(list(camp.disposition.all().values_list('name',flat=True)))
		context['users'] = list(get_campaign_users(camp_list.values_list('name', flat=True), request.user).values("id", "username"))
		context['dispo_list'] = dispo
		context['phonebook_list'] = list(Phonebook.objects.filter(campaign__in=campaign_id, status='Active').values("id", "name"))
		return Response(context)


@method_decorator(check_read_permission, name='get')
class CustomCrmFieldApiView(LoginRequiredMixin, APIView):
	"""
	This View is used to create custom crm fields
	"""

	renderer_classes = [TemplateHTMLRenderer]
	template_name    = "crm/crm-fields.html"
	login_url = '/'

	def get(self, request, **kwargs):
		page_info = data_for_pagination(request)
		crm_fields = CrmField.objects.all()
		if check_non_admin_user(request.user):
			user_campaigns = list(Campaign.objects.filter(Q(users=request.user)|Q(group__in=request.user.group.all())|Q(created_by=request.user)).distinct().values_list('name',flat=True))
			crm_fields = crm_fields.filter(campaign__name__in=user_campaigns).distinct()
		if page_info["search_by"] and page_info["column_name"]:
			if page_info["column_name"] == "campaign":
				crm_fields = crm_fields.filter(campaign__name__istartswith=page_info["search_by"])
			else:
				crm_fields = crm_fields.filter(**{page_info["column_name"]+"__iexact": page_info["search_by"]})

		crm_fields = crm_fields.order_by('-id')
		crm_field_list = list(crm_fields.values_list("id", flat=True))
		paginate_by_columns = (('name', 'Name'),
			('campaign', 'Campaign'),
			)
		data = {}

		crm_fields = get_paginated_object(crm_fields, page_info["page"], page_info["paginate_by"])
		pagination_dict = data_for_vue_pagination(crm_fields)
		data["id_list"] = crm_field_list
		data["campaign_list"] = list(Campaign.objects.values("id", "name"))
		data["paginate_by_columns"] = paginate_by_columns
		camp_name, active_camp, noti_count = get_active_campaign(request)
		data["noti_count"] = noti_count
		context= {**data, **kwargs['permissions'], **page_info}

		if request.is_ajax():
			result = list(CrmFieldPaginationSerializer(crm_fields, many=True).data)
			pagination_dict["table_data"] = result
			context = {**context, **kwargs['permissions'], **pagination_dict}
			return JsonResponse(context)
		else:
			context = {**context, **kwargs['permissions'], **pagination_dict}
			context['request']: request
			return Response(context)

class CheckCampaignAvailApiView(APIView):
	""" check campaign is assigned to any crm or not """
	def post(self, request):
		campaign = request.POST.get("campaign", "")
		crm_name = request.POST.get("crm_name", "")
		crm_field = CrmField.objects.filter(campaign__name=campaign)
		if crm_field.exists():
			crm_field = crm_field.first()
			if crm_field.name != crm_name:
				return JsonResponse({'camp_exist':'This campaign is already assigned to other crm'})
		return JsonResponse({'msg':'Valid Campaign'})


@method_decorator(check_create_permission, name='get')
@method_decorator(crm_field_validation, name='post')
class CreateCustomCrmFieldApiView(LoginRequiredMixin, APIView):
	"""
	This View is used to create custom crm fields
	"""

	renderer_classes = [TemplateHTMLRenderer]
	template_name    = "crm/create-crm-fields.html"
	login_url = '/'

	def get(self, request, format=None, **kwargs):
		data = {}
		campaigns = Campaign.objects.values("id", "name")
		if check_non_admin_user(request.user):
			campaigns = campaigns.filter(Q(users=request.user)|Q(group__in=request.user.group.all())|Q(created_by=request.user)).distinct()
		data["campaign_list"] = campaigns
		data["field_types"] = FIELD_CHOICES
		data["field_status"] = Status
		data = {**data, **kwargs['permissions']}
		return Response(data)

	def post(self, request):
		campaign_list = request.POST.getlist("campaign")
		crm_field_serializer = CrmFieldSerializer(data=request.POST)
		if crm_field_serializer.is_valid():
			crm_data = crm_field_serializer.save(created_by=request.user.username)
			create_admin_log_entry(request.user, "crm","1",'CREATED',crm_data.name)
			for name in campaign_list:
				camp_info, created = CampaignInfo.objects.get_or_create(name=name.strip())
				crm_data.campaign.add(camp_info)
				crm_data.save()
			return JsonResponse({'msg':'Crm fileds created'})
		else:
			return JsonResponse({'msg':'Pass Valid Data'})

def can_contact_upload(crm_field_section, campaign):
	""" Check the contact can be uploaded or not """
	for section in crm_field_section:
		query_dict = {}
		query_dict[section["section_name"]] = {}
		for field in section["section_fields"]:
			query_dict[section["section_name"]][field["field"]]= None
			none_query = copy.deepcopy(query_dict)
			query_dict[section["section_name"]][field["field"]]= ""
			blank_query = copy.deepcopy(query_dict)
			contact_count = Contact.objects.filter(Q(campaign__in=campaign),~Q(customer_raw_data__contains=none_query)|~Q(customer_raw_data=blank_query)).count()
			if contact_count >0:
				return True
	return False

@method_decorator(crm_field_validation, name='post')
class EditCustomCrmFieldApiView(LoginRequiredMixin, APIView):
	"""
	This View is used to edit custom crm fields
	"""

	renderer_classes = [TemplateHTMLRenderer]
	template_name    = "crm/crm-fields-edit.html"
	login_url = '/'

	def get(self, request, pk, format=None):
		data ={}
		data["field_types"] = FIELD_CHOICES
		data["field_status"] = Status
		data["can_create"] = True
		crm_inst = get_object(pk, "crm", "CrmField")
		data["crmfield"] = crm_inst
		data["crm_fields"] = crm_inst.crm_fields
		uniqueid = crm_inst.unique_fields
		if uniqueid:
			unique_field_exist = check_data_with_uniue_id(uniqueid[0])
			data["unique_field_exist"] = unique_field_exist
		data["section_priority"] = [field["section_priority"] for field in data["crm_fields"] if 'section_priority' in field]
		data["unique_fields_count"] = len(crm_inst.unique_fields)
		crmfield_campaign = list(crm_inst.campaign.all().values_list("name", flat=True))
		check_list = []
		for camp in crmfield_campaign:
			css_inst = CSS.objects.filter(campaign=camp)
			if css_inst.exists():
				for query in css_inst.first().raw_query:
					for fields in query['css_fields']:
						if fields['table_column'] not in check_list:
							check_list.append(fields['table_column'])
		campaign = Campaign.objects.values("id", "name")
		if check_non_admin_user(request.user):
			campaign = campaign.filter(Q(users=request.user)|Q(group__in=request.user.group.all())|Q(created_by=request.user)).distinct()
			non_user_campaigns = crm_inst.campaign.exclude(name__in=list(campaign.values_list('name',flat=True)))
			data['non_user_campaigns'] = list(non_user_campaigns.values_list('name',flat=True))
			data["campaign_list"] = list(campaign) + list(non_user_campaigns.values("id","name"))
		else:
			data["campaign_list"] = campaign
			data['non_user_campaigns'] = []
		data["check_list"] = check_list
		data["status"] = str(can_contact_upload(crm_inst.crm_fields, list(campaign))).lower()
		return Response(data)

	def post(self, request, pk, format=None):
		crm_field_inst = get_object(pk, "crm", "CrmField")
		campaign_list = request.POST.getlist("campaign")
		crm_field_serializer = CrmFieldSerializer(crm_field_inst, data=request.POST)
		if crm_field_serializer.is_valid():
			crm_data = crm_field_serializer.save()
			create_admin_log_entry(request.user, "crm","2",'UPDATED',crm_data.name)
			crm_data.campaign.clear()
			for name in campaign_list:
				camp_info, created = CampaignInfo.objects.get_or_create(name=name.strip())
				crm_data.campaign.add(camp_info)
				crm_data.save()
			return JsonResponse({'msg':'Crm fileds updated'})
		else:
			return JsonResponse({'msg':'Pass Valid Data'})

# @method_decorator(crm_field_validation, name='post')
class UploadCremFieldApiView(APIView):
	"""
	This view is used to upload crm fields in crmfield model
	"""
	def post(self, request, format=None):

		upload_crm(request)

		return JsonResponse({"msg": "file removed successfully"})

class ValidateUploadedCrmField(APIView):

	"""
	This view is used to validate uploaded crm before submitting
	"""

	def post(self, request, format=None):
		crm_file = request.FILES.get("crmField_file", "")
		crm_name = request.POST.get("name", "")
		if crm_file.size <= 1:
			response_data = {}
			response_data["column_err_msg"] = 'File must not be empty'
		else:
			if crm_file.name.endswith('.csv'):
				data = pd.read_csv(crm_file, na_filter=False,  dtype = {"section_priority" : "str", "field_size": "str",
					"field_priority":"str"})
			else:
				data = pd.read_excel(crm_file, dtype = {"section_priority" : "str", "field_size": "str",
					"field_priority":"str"})

			column_list = data.columns.tolist()
			expected_col_list = ["section_name", "section_priority", "field", "field_type", "field_size", "options",
			"editable","field_priority", "field_status" ]
			valid = set(expected_col_list).issubset(set(column_list))
			if valid:
				response_data = validate_uploaded_crm(data, crm_name)
			else:
				response_data = {}
				response_data["column_err_msg"] = 'File must contains these '+','.join(expected_col_list)+' columns'
				response_data["column_id"] = "#crm-err-msg"
		return JsonResponse(response_data)


@method_decorator(check_read_permission, name='get')
class ContactInfoApiView(LoginRequiredMixin, APIView):
	"""
	This view is used to show all contacts and cntact information
	and do some filteration by columns, campaign and phonebook
	"""

	login_url = '/'
	renderer_classes = [TemplateHTMLRenderer,DatatablesRenderer]
	template_name    = "contacts/contact_info.html"
	serializer_class = ContactListSerializer
	paginator = DatatablesPageNumberPagination

	def get(self, request, **kwargs):
		add_crm_field = True
		# campaign_list = Campaign.objects.values("name", "id")
		campaign_list = Campaign.objects.filter(Q(users__id__in=user_hierarchy_func(request.user.id))).distinct().values("name", "id")
		phonebook = list(Phonebook.objects.values(
		"id", "name", "campaign", "status"))
		disposition = list(Disposition.objects.values("id","name"))
		context = {"request":request,"campaign_list":campaign_list,"phonebook_list":phonebook,
			"disposition":disposition}
		camp_name, active_camp, noti_count = get_active_campaign(request)
		context["noti_count"] = noti_count
		context = {**context, **kwargs['permissions']}
		if request.is_ajax():
			report_visible_cols = get_report_visible_column("10",request.user)
			filter_by_phonebook = request.GET.get("phonebook", "")
			filter_by_campaign = request.GET.get("campaign", "")
			crm_fields = []
			if add_crm_field and filter_by_campaign:
				campaign = Campaign.objects.get(id=filter_by_campaign).name
				crm_fields = get_customizable_crm_fields(campaign)
			columns_list = ['campaign','phonebook','user','numeric','alt_numeric','first_name','last_name','email',
			'disposition','churncount','status','dial_count','last_dialed_date','last_connected_user','uniqueid']
			data = {"columns_list": columns_list}
			data['report_visible_cols'] = report_visible_cols
			data["crm_fields"] = list(set(crm_fields))
			data = {**data, **kwargs['permissions']}
			return JsonResponse(data)
		return Response(context)

	def post(self,request):

		download_csv = request.POST.get('contact_info_download', '')
		if download_csv:
			col_list = request.POST.get('col_name_list',[])
			if col_list:
				col_list = col_list.split(',')
			filters = request.POST.dict()
			filters['phonebook'] = request.POST.getlist("phonebook", [])
			filters['campaign'] = request.POST.getlist("campaign", [])
			filters['user'] = request.POST.getlist("user", [])
			filters['disposition'] = request.POST.getlist("disposition", [])
			filters['download_type'] = request.POST.get('contact_info_download_type','csv')
			DownloadReports.objects.create(report='Contact Info',filters=filters, user=request.user.id, serializers=self.serializer_class, col_list=col_list, status=True)
			return JsonResponse({"message":"Your Download request is created, will notify in download notification once completed."})
		contacts = Contact.objects.none()
		paginator = self.paginator()
		filter_by_phonebook = request.POST.getlist("phonebook[]", "")
		filter_by_campaign = request.POST.getlist("campaign[]", "")
		filter_by_user = request.POST.getlist("user[]", [])
		start_date = request.POST.get('start_date','')
		end_date = request.POST.get('end_date','')
		disposition = request.POST.getlist('disposition[]','')
		numeric = request.POST.get('numeric','')
		uniqueid = request.POST.get('uniqueid','')

		if request.POST.get('format', None) == 'datatables':
			paginator.is_datatable_request = True
		else:
			paginator.is_datatable_request = False

		if filter_by_campaign:
			filter_by_campaign = list(Campaign.objects.filter(id__in=filter_by_campaign).values_list("name", flat=True))
			contacts = Contact.objects.filter(campaign__in=filter_by_campaign,
					created_date__date__gte=start_date, created_date__date__lte=end_date)
			campaign_column = True
			if filter_by_phonebook:
				contacts = contacts.filter(phonebook__id__in=filter_by_phonebook)
			if filter_by_user:
				contacts = contacts.filter(user__in=filter_by_user)
			if numeric:
				contacts = contacts.filter(numeric=numeric)
			if disposition:
				contacts = contacts.filter(disposition__in=disposition)
			if uniqueid:
				contacts = contacts.filter(uniqueid=uniqueid)
			page = self.paginate_queryset(contacts, paginator)
			if page is not None:
				serializer = self.serializer_class(page, many=True)
				return self.get_paginated_response(serializer.data, paginator)
			serializer = self.serializer_class(contacts, many=True)
			return Response(serializer.data)
		return Response({'error':'Select atleast one campaign'})

	def filter_queryset(self, queryset):
		for backend in list(self.filter_backends):
			queryset = backend().filter_queryset(self.request, queryset, self)
		return queryset

	def paginate_queryset(self, queryset, paginator):
		if self.paginator is None:
			return None
		return self.paginator.paginate_queryset(queryset=queryset, request=self.request, self=paginator)

	def get_paginated_response(self, data, paginator):
		assert self.paginator is not None
		return self.paginator.get_paginated_response(paginator, data)

@method_decorator(check_update_permission, name='get')
class ContactInfoEditApiView(LoginRequiredMixin, APIView):
	"""
	This view is used to edit contact detail and customer info
	"""

	renderer_classes = [TemplateHTMLRenderer]
	template_name    = "contacts/contact_info_edit.html"
	login_url = '/'

	def get(self, request, pk, format=None, **kwargs):
		data = {}
		contact = get_object(pk, "crm", "Contact")
		data["phonebook_list"] = get_user_crm_data(request.user, "crm", "Phonebook").filter(status="Active")
		data["contact_status"] = CONTACT_STATUS
		data["contact"] = contact
		if CrmField.objects.filter(campaign__name=contact.campaign).exists():
			crm_fields = CrmField.objects.get(campaign__name=contact.campaign)
			data['crm_fields'] = crm_fields.crm_fields
		else:
			data['crm_fields'] = []
		raw_data = contact.customer_raw_data
		data["crm_data"] = raw_data
		data = {**data, **kwargs['permissions']}
		return Response(data)

	def post(self, request, pk, format=None):
		contact = get_object(pk, "crm", "Contact")
		contact_serializer = SetContactSerializer(contact, data=request.POST)
		if contact_serializer.is_valid():
			customer_raw_data = json.loads(request.POST.get("customer_raw_data", "{}"))
			customer_raw_data = {sec_name :{field_name:(None if field_value=='' else field_value) for field_name,field_value in sec_value.items()} for sec_name,sec_value in customer_raw_data.items()}
			contact = contact_serializer.save(user=request.POST.get("user",""), customer_raw_data=customer_raw_data)
			if contact.uniqueid and AlternateContact.objects.filter(uniqueid=contact.uniqueid).exists():
				AlternateContact.objects.filter(uniqueid=contact.uniqueid).update(alt_numeric=json.loads(request.POST.get("alt_numeric","{}")))
			elif AlternateContact.objects.filter(numeric=contact.numeric).exists():
				AlternateContact.objects.filter(numeric=contact.numeric).update(alt_numeric=json.loads(request.POST.get("alt_numeric","{}")))
			else:
				if contact.uniqueid:
					AlternateContact.objects.create(numeric=contact.numeric, alt_numeric=json.loads(request.POST.get("alt_numeric","{}")), uniqueid=contact.uniqueid)
				else:
					AlternateContact.objects.create(numeric=contact.numeric, alt_numeric=json.loads(request.POST.get("alt_numeric","{}")))
			temp_contact = TempContactInfo.objects.filter(id=pk)
			if temp_contact.exists():
				temp_contact.update(user=contact.user, numeric=contact.numeric, alt_numeric=contact.alt_numeric,
						email=contact.email)
		else:
			print(contact_serializer.errors)
		return JsonResponse({"msg":"Contact Detail Saved Successfully"}, status=200)



@method_decorator(check_read_permission, name='get')
class ConnectedCallStatusApiView(LoginRequiredMixin, APIView):
	"""
	This view is used to show all contacts and do some
	filteration by columns, campaign and phonebook
	"""

	renderer_classes = [TemplateHTMLRenderer]
	template_name    = "contacts/call_contact_status.html"
	login_url = '/'

	def get(self, request, **kwargs):
		data = connected_contact_status(request, False)
		context = {**data, **kwargs['permissions']}
		return Response(context)


class DownloadSamplePhoneBookCsv(APIView):
	""" Download sample phonebook csv """
	def get(self, request, campaign, file_type, format=None):
		campaign_inst = Campaign.objects.get(name=campaign)
		column_list = get_customizable_crm_fields(campaign_inst.name)
		cols = ['numeric','alt_numeric','first_name','last_name','email','priority']
		cols = cols + column_list
		if campaign_inst.portifolio:
			cols.insert(0, 'user')
		return csvDownload(cols, "phonebook", file_type)

class DownloadSampleUpdatePhonebookCsv(APIView):
	""" Download sample update phonebook csv """
	def get(self, request, format=None):
		col_list = request.GET.get('col_list','all')
		if col_list != 'all':
			cols = col_list.split(',')
			if '' in cols:
				cols.remove('')
			cols.insert(0,request.GET.get('duplicate_check_col',''))
		else:
			campaign_inst = Campaign.objects.get(name=request.GET.get('campaign',''))
			column_list = get_customizable_crm_fields(campaign_inst.name)
			cols = ['numeric','alt_numeric','first_name','last_name','email','priority','disposition']
			cols = cols + column_list
			if campaign_inst.portifolio:
				cols.insert(0, 'user')
		return csvDownload(cols, "phonebook", request.GET.get('file_type','csv'))

class DownloadPhonebook(LoginRequiredMixin, APIView):
	""" Download phonebook data  """
	login_url = '/'
	def post(self,request,format=None):
		pk=request.POST.get("selected_entry",'')
		phonebook_inst = Phonebook.objects.filter(id=pk).first()
		if phonebook_inst.contacts.exists():
			campaign_name=Campaign.objects.filter(id=phonebook_inst.campaign).first().name
			crm_fields=get_customizable_crm_fields(campaign_name)
			columns_list = ['user','numeric','first_name','last_name','email','priority']
			col_name = columns_list + crm_fields
			filters = {}
			filters['phonebook_id'] = pk
			filters['phonebook_name'] = phonebook_inst.name
			DownloadReports.objects.create(report=phonebook_inst.name+' Lead List',filters=filters, user=request.user.id, col_list=col_name, status=True)
			return JsonResponse({"message":"Your Download request is created, will notify in download notification once completed."})
		return JsonResponse({"error":"Contact data not available for this phonebook"}, status=400)

class GetDuplicateListForPhonebook(APIView):
	""" this class same crm fields in the phonebook or not """
	def post(self, request, format=None):
		phonebook_id = request.POST.get("phonebook_id", "")
		contact_list = []
		if phonebook_id:
			contact_list = ["numeric","status","priority","uniqueid","disposition"]
			ext_camp_col_list =[]
			existing_camp = Phonebook.objects.get(id=phonebook_id).campaign
			camp = Campaign.objects.filter(id=existing_camp)
			if camp.exists():
				ext_camp_col_list = get_customizable_crm_fields(camp[0].name)
			column_list = get_customizable_crm_fields(request.POST.get("campaign", ""))
			if column_list != ext_camp_col_list:
				return JsonResponse({"field_error": "Crm fields not same in this campaign", "campaign_name":existing_camp}, status=500)
		else:
			column_list = get_customizable_crm_fields(request.POST.get("campaign", ""))
		return JsonResponse({"columns": column_list, "contact_list":contact_list}, status=200)


class SaveAgentBreakApiView(LoginRequiredMixin, APIView):
	"""
	This View is used to save agent breaks
	"""
	login_url = '/'

	def post(self, request, format=None):
		from dialer.dialersession import on_break, start_sip_session

		activity_dict = get_formatted_agent_activities(request.POST)
		activity_dict["user"] = request.user
		activity_dict["campaign_name"] = request.POST.get("campaign_name", "")
		predictive_time = request.POST.get("predictive_time", "00:00:00")
		activity_dict["predictive_time"] = datetime.strptime(predictive_time, '%H:%M:%S').time()
		predictive_wait_time = request.POST.get("predictive_wait_time", "00:00:00")
		activity_dict["predictive_wait_time"] = datetime.strptime(predictive_wait_time, '%H:%M:%S').time()
		event = request.POST.get("event", "")
		if event:
			activity_dict["event"] = event
			activity_dict["event_time"] = datetime.now()
		else:
			activity_dict["event"] = "LOGIN"
			login_time = request.session.get('login_time', '')
			login_time = dateutil.parser.parse(login_time)
			activity_dict["event_time"] =login_time

		AGENTS = get_agent_status(request.user.extension)
		if request.user.extension not in AGENTS:
			AGENTS[request.user.extension]={}
		if request.POST.get("break_name", ""):
			AGENTS[request.user.extension]['status'] = request.POST.get("break_name")
			if request.POST["break_name"] not in ["Ready","NotReady"]:
				AGENTS[request.user.extension]['state'] = 'onBreak'
			else:
				if request.POST["break_name"] == "Ready":
					AGENTS[request.user.extension]['state'] = 'Idle'
				else:
					AGENTS[request.user.extension]['state'] = ''
			AGENTS[request.user.extension]['event_time'] = datetime.now().strftime('%H:%M:%S')
		else:
			if event == 'Window Reload':
				set_agentReddis(AGENTS,request.user)
		status = {'ori_uuid':'','status':True}
		if 'event' in request.POST:
			if request.POST.get('event')=='Start Break' and 'uuid' in request.POST and request.POST.get('uuid'):
				on_break(request.POST.get('sip_ip'),uuid=request.POST.get('uuid'))

			if request.POST.get('event')=='End Break' and 'extension' in request.POST and request.POST.get('extension'):
					status = start_sip_session(request.POST.get('sip_ip'), extension=request.POST.get('extension',''), call_type=request.POST.get('call_type',''),
						campaign_name=request.POST.get("campaign_name", ""))
					if 'ori_uuid' not in status or status['ori_uuid']=='':
						status['ori_uuid'] = ''
						status['status'] = False
		set_agent_status(request.user.extension,AGENTS[request.user.extension])

		if request.POST.get("break_time", "") :
			activity_dict["break_type"] = request.POST.get("break_type")
			activity_dict["break_time"] =  datetime.strptime(request.POST.get("break_time"), '%H:%M:%S').time()
		else:
			activity_dict["break_type"] = request.POST.get("break_type",'')
			activity_dict["break_time"] =  datetime.strptime("00:00:00", '%H:%M:%S').time()
		create_agentactivity(activity_dict)
		return JsonResponse({'msg':'agent breaks saved','uuid':status['ori_uuid']})

class LeadListChurnAPI(LoginRequiredMixin, APIView):
	""" churning the lead list for dialing the data """
	login_url = '/'

	def get(self, request, pk=""):
		str_dispo=""
		dispo_list=[]
		if pk:
			campaign = Campaign.objects.get(name = Phonebook.objects.get(id=pk).campaign_name)
			str_dispo = campaign.dispo_list
			dispo_list=[i.lstrip() for i in str_dispo.split(',')]
			user_list = list(campaign.users.all().values_list("id", flat=True))
			group_users = campaign.group.all()
			group_user_list = list(User.objects.filter(group__in=group_users).values_list("id", flat=True))
			user_list = user_list + group_user_list
			camp_all_users = list(User.objects.filter(id__in=user_list).values_list("username", flat=True))
			if campaign.wfh:
				dispo_list = dispo_list + list(campaign.wfh_dispo.values())
			if campaign.vbcampaign.exists():
				if campaign.vbcampaign.first().voice_blaster and 'vb_dtmf' in campaign.vbcampaign.first().vb_data:
					dispo_list = dispo_list + list(campaign.vbcampaign.first().vb_data['vb_dtmf'].values())
		return JsonResponse({"dispo_list":dispo_list, "camp_all_users":camp_all_users},status=200)

	def post(self, request, pk=""):
		churn_count = request.POST.get("leadchurn-count","")
		churn_list = request.POST.getlist("leadchurn",list)
		contact = Contact.objects.filter(phonebook=pk, modified_date__gte=request.POST.get("start_date",""),
			modified_date__lte=request.POST.get("end_date",""))
		campaign_obj = Campaign.objects.get(name = Phonebook.objects.get(id=pk).campaign_name)
		users = list(UserVariable.objects.filter(user__username__in=request.POST.getlist("user","")).values_list("extension", flat=True))
		final_count = 0
		if churn_count == 'leadchurn-count-click':
			if contact and churn_list:
				for dispo in churn_list:
					if dispo not in ['Drop','Abandonedcall','NC','Invalid Number','AutoFeedback','CBR']:
						contact_data = contact.filter(disposition=dispo, status="Dialed")
					else:
						contact_data = contact.filter(status=dispo)
					if users:
						contact_data = contact_data.filter(last_connected_user__in=users)
					contact_count = contact_data.count()
					final_count = final_count + contact_count
			return JsonResponse({'final_count':final_count},status=200)
		else:
			if contact and churn_list:

				model='phonebook'
				action_type="2"     #in constants it's updated
				event_type="UPDATED"
				name=Phonebook.objects.get(id=pk).name
				if request.user.is_superuser:
					role='admin'
				else:
					role=request.user.user_role
				msg=request.user.username+' with role '+role+'  has '+" churned "+name+" in "+model+' model'

				for dispo in churn_list:
					if dispo not in ['Drop','Abandonedcall','NC','Invalid Number','AutoFeedback','CBR']:
						if users:
							contact_query = Q(disposition=dispo, status="Dialed", last_connected_user__in=users)
						else:
							contact_query = Q(disposition=dispo, status="Dialed")
						contact_count = contact.filter(contact_query).count()
						contact.filter(contact_query).update(status='NotDialed', churncount=F('churncount')+1,modified_date=datetime.now())

						admin_log_obj=AdminLogEntry(created_by=request.user,change_message=msg,action_name=action_type,event_type=event_type)
						admin_log_obj.save()

					else:
						if users:
							contact_query = Q(status=dispo, last_connected_user__in=users)
						else:
							contact_query = Q(status=dispo)
						contact_count = contact.filter(contact_query).count()
						contact.filter(status=dispo).update(status='NotDialed', churncount=F('churncount')+1,modified_date=datetime.now())

						admin_log_obj=AdminLogEntry(created_by=request.user,change_message=msg,action_name=action_type,event_type=event_type)
						admin_log_obj.save()

					final_count = final_count + contact_count
				if final_count > 0:
					PhonebookBucketCampaign.objects.filter(id=campaign_obj.id).update(is_contact=True)
			return JsonResponse({'updated_count':final_count},status=200)

def DownloadCrmFields(request,pk,format=None):
	""" crm fields download data which is created"""
	crm_field_inst = get_object(pk, "crm", "CrmField")
	crm_fields_data = crm_field_inst.crm_fields
	result = download_crmfields_csv(request,crm_fields_data)
	return result

class GetContactInfoAPIView(APIView):
	""" get the contact info data """
	def get(self, request, pk):
		contact_info = {}
		contact = Contact.objects.filter(id=pk)
		if contact.exists():
			contact_info = ContactSerializer(contact.first()).data
		return JsonResponse(contact_info,status=200)

@method_decorator(check_read_permission, name='get')
@method_decorator(check_update_permission, name='post')
@method_decorator(check_create_permission, name='post')
class LeadPriorityListAPIView(LoginRequiredMixin, APIView):
	"""
	This view is used to show list of ndnc
	"""
	login_url = '/'
	renderer_classes = [TemplateHTMLRenderer]
	template_name = "crm/lead-priority-data.html"

	def get(self, request, **kwargs):
		page_info = data_for_pagination(request)
		context= {}
		data = {}
		page = int(request.GET.get('page' ,1))
		paginate_by = int(request.GET.get('paginate_by', 10))
		if page_info["search_by"] and page_info["column_name"]:
			query = {str(page_info["column_name"]):page_info["search_by"]}
			queryset = LeadListPriority.objects.filter(**query)
		else:
			queryset = LeadListPriority.objects.all()
		data['id_list'] = list(queryset.values_list("id", flat=True))
		queryset = get_paginated_object(queryset, page_info["page"], page_info["paginate_by"])
		pagination_dict = data_for_vue_pagination(queryset)
		paginate_by_columns = (('uniqueid', 'Uniqueid'),
			('priority', 'Priority'),
			)
		data["paginate_by_columns"] = paginate_by_columns
		data['campaign_list'] = list(Campaign.objects.values("id", "name", "portifolio"))
		context= {**data, **page_info}
		if request.is_ajax():
			result = list(LeadListPrioritySerializer(queryset, many=True).data)
			pagination_dict["table_data"] = result
			context = {**context, **kwargs['permissions'], **pagination_dict}
			return JsonResponse(context)
		else:
			context = {**context, **kwargs['permissions'], **pagination_dict}
			context['request']: request
			return Response(context)

		return JsonResponse({**pagination_dict})

	def post(self, request, **kwargs):
		uploaded_file = request.FILES.get("delta_file", "")
		campaign_id = request.POST.get('campaign')
		error = []
		if uploaded_file:
			campaign  = Campaign.objects.filter(id=campaign_id).first()
			table_columns = []
			if campaign.lead_priotize:
				key = ''
				value = []
				for keys in campaign.lead_priotize.keys():
					key = str(keys)
				if uploaded_file.name.endswith('.csv'):
					data = pd.read_csv(uploaded_file, na_filter=False, encoding = "unicode_escape", escapechar='\\',dtype = {str(key):"str","priority": "str","global":"str"},)
				else:
					data = pd.read_excel(uploaded_file, encoding = "unicode_escape",
						converters={str(key):str,'priority': str,'global':str})
					data = data.replace(np.NaN, "")
				column_names = data.columns.tolist()
				table_columns = [key,'priority','global']
				if key and 'status' in campaign.lead_priotize[key] and campaign.lead_priotize[key]['status']==str('true'):
					valid = all(elem in column_names for elem in table_columns)
					if valid:
						value = key.split(':')
						number = 0
						for index, row in data.iterrows():
							number +=1
							# query = {'customer_raw_data__'+value[0]+'__'+value[1]:str(row.get(key))}
							contact_ids = list(Contact.objects.filter(uniqueid=str(row.get(key))).values_list("id", flat=True))
							priority = None if row.get("priority")=='' else row.get("priority")
							if len(contact_ids)>0:
								if Contact.objects.filter(id__in=contact_ids).exists():
									Contact.objects.filter(id__in=contact_ids).update(priority = priority, uniqueid=str(row.get(key)))
									if 'tap' in campaign.lead_priotize[key]:
										continue
									else:
										try:
											LeadListPriority.objects.create(uniqueid=row.get(key), priority=priority, campaign_id=campaign.id, is_global=True if str(row.get('global','')).lower()=='true' else False)
										except Exception as e:
											print(e, 'Exception in lead list priority uniqueid')
											LeadListPriority.objects.filter(uniqueid=row.get(key), campaign_id=campaign.id).update(priority=priority, is_global=True if str(row.get('global','')).lower()=='true' else False)
							else:
								try:
									LeadListPriority.objects.create(uniqueid=row.get(key), priority=priority, campaign_id=campaign.id, is_global=True if str(row.get('global','')).lower()=='true' else False)
								except Exception as e:
									print(e, 'Exception in lead list priority uniqueid')
									LeadListPriority.objects.filter(uniqueid=row.get(key), campaign_id=campaign.id).update(priority=priority, is_global=True if str(row.get('global','')).lower()=='true' else False)
						temp_ids = TempContactInfo.objects.filter(campaign=campaign.name, status="NotDialed")
						for temp in temp_ids:
							Contact.objects.filter(id=temp.contact_id).update(status=temp.previous_status)
						temp_ids.delete()
					else:
						return JsonResponse({"msg":"Lead priority column mismatch"},status=500)
				else:
					return JsonResponse({"msg":"Status of priority is inactive in campaign"},status=500)
			else:
				return JsonResponse({"msg":"Lead priority column is not found"},status=500)
		if error:
			return JsonResponse({"msg":error},status=500)
		return Response({"msg":"lead priority uploaded"})

class LeadPriorityCsvAPIView(LoginRequiredMixin, APIView):
	"""
	This view is used to show list of ndnc
	"""
	login_url = '/'
	def get(self, request):
		campaign_id = request.GET.get("campaign_id", "")
		campaign  = Campaign.objects.filter(id=campaign_id).first()
		if campaign.lead_priotize:
			key = ''
			for keys in campaign.lead_priotize.keys():
				key = str(keys)
				table_columns = [keys,'priority','global']
				break
			if key and 'status' in campaign.lead_priotize[key] and campaign.lead_priotize[key]['status']==str('true'):
				writer = csv.writer(Echo())
				data = writer.writerow(table_columns)
				response = HttpResponse(data,content_type='text/csv',)
				response['Content-Disposition'] = 'attachment;filename=agent_performance_reports.csv'
				return response
			else:
				return Response("Priority for this campaign is not active",status=500)
		else:
			return Response("No columns",status=500)

class DownloadAPIView(LoginRequiredMixin,APIView):
	""" Show the downloaded data """
	login_url = '/'
	renderer_classes = [TemplateHTMLRenderer]
	template_name = "download/download.html"

	def get(self,request, **kwargs):
		page_info = data_for_pagination(request)
		refresh_cell = request.GET.get("refresh_cell", "")
		if page_info["search_by"] and page_info["column_name"]:
			queryset = DownloadReports.objects.filter(**{page_info["column_name"]+"__istartswith": page_info["search_by"]}).filter(user=request.user.id).order_by('-id')
		else:
			queryset = DownloadReports.objects.filter(user=request.user.id).order_by('-id')
		not_view = queryset.filter(view=False)
		if not_view.exists():
			not_view.update(view=True)
		download_ids = list(queryset.values_list("id", flat=True))
		queryset = get_paginated_object(queryset, page_info["page"], page_info["paginate_by"])
		pagination_dict = data_for_vue_pagination(queryset)
		paginate_by_columns = (('report', 'ReportName'),)
		context = { "id_list": download_ids, "paginate_by_columns":paginate_by_columns}
		context = {**context, **page_info, **pagination_dict}
		if request.is_ajax():
			result = list(DownloadReportsSerializer(queryset, many=True).data)
			pagination_dict["table_data"] = result
			context = {**context, **pagination_dict}
			return JsonResponse(context)
		else:
			context = {**context, **pagination_dict}
			context['request']: request
			return Response(context)

class PerformActionOnSelectedEntry(APIView):
	""" Download action perform from the download page """
	def post(self, request):
		app_label = request.POST.get("app_name", "")
		model_name = request.POST.get("model_name", "")
		selected_entry = request.POST.get('selected_entry')
		perform_operation = request.POST.get("perform_operation", "")
		model = apps.get_model(app_label=app_label, model_name=model_name)
		if model:
			data = model.objects.get(id=selected_entry)
			if perform_operation=='Start':
				data.downloaded_file = None
				data.status = True
				data.save()
			if perform_operation=='Stop':
				data.delete()
		return Response({"msg": "Selected entries "+str(perform_operation)+' Successfully'})

class GetEditContactInfoApiView(APIView):
	""" edit the contactinfo get option """
	def get(self, request, pk, format=None):
		data = {}
		contact = get_object(pk, "crm", "Contact")
		data["phonebook_list"] = list(get_user_crm_data(request.user, "crm", "Phonebook").filter(status="Active").values("id","name"))
		data["can_update"] = True
		data["contact_status"] = CONTACT_STATUS
		data["contact"] = EditContactListSerializer(contact, many=False).data
		if CrmField.objects.filter(campaign__name=contact.campaign).exists():
			crm_fields = CrmField.objects.get(campaign__name=contact.campaign)
			data['crm_fields'] = crm_fields.crm_fields
		else:
			data['crm_fields'] = []
		data['crm_fieds_data'] = crm_field_value_schema(contact.campaign)
		raw_data = contact.customer_raw_data
		data["crm_data"] = raw_data
		data["alt_numeric"] = data['contact']['alt_numeric']
		return Response(data)

class ContactUploadDataApiView(APIView):
	if settings.XML_INSERT_KEY!='':
		parser_classes = [XMLParser]
	permission_classes = [AllowAny]
	def post(self, request):
		uniqueid = None
		data_dict = {}
		crm_field_dict = {}
		error_dict ={}
		phonebook_id = None
		action = "insert"
		contact_col_list = ["numeric","alt_numeric","first_name","last_name","user","email", "priority"]
		data = json.dumps(request.data)
		data = re.sub("\{http.*?}",'',data)
		data = json.loads(data)
		data = data.get('Body',data)
		if settings.XML_INSERT_KEY in data:
			action = "insert"
			data = data.get(settings.XML_INSERT_KEY,data)
		elif settings.XML_UPDATE_KEY in data:
			action = "update"
			data = data.get(settings.XML_UPDATE_KEY,data)

		if settings.REPLACE_API_KEY and settings.REPLACE_API_VALUE:
			data =  {k.replace(settings.REPLACE_API_KEY,settings.REPLACE_API_VALUE,1).lower(): v for k, v in data.items()}
		campaign = settings.API_DEST_CAMP if settings.API_DEST_CAMP != "" else data.get(settings.API_CAMPAIGN_FIELD)
		numeric = data.get(settings.API_NUMERIC_FIELD)
		if campaign and numeric:
			campaign = Campaign.objects.filter(name=campaign)
			if campaign.exists():
				campaign = campaign.first()
				if not Phonebook.objects.filter(slug=campaign.name+"_phonebook",campaign=campaign.id).exists():
					if Phonebook.objects.filter(slug=campaign.name+"_phonebook").exists():
						return JsonResponse({"msg":"LeadList is Created, But Assigned to Another Campaign",'status':'error'},status=500)
				phonebook_obj,created = Phonebook.objects.get_or_create(campaign=campaign.id,slug=campaign.name+"_phonebook",defaults={"name":campaign.name+"_phonebook","campaign":campaign.id,"slug":campaign.name+"_phonebook","created_by":'API'})
				if phonebook_obj:
					phonebook_id = phonebook_obj.id
				PhonebookBucketCampaign.objects.filter(id=campaign.id).update(is_contact=True)
				crm_field_list = get_customizable_crm_fields_with_datatype(campaign.name)
				row = data
				api_crm_keys = []
				database_crm_fields =[]
				for key,value in row.items():
					if key.find(":") != -1:
						if crm_field_list:
							for field in crm_field_list:
								section_name = field["field_name"].split(':')[0].replace(' ','_').lower()
								field_name = field["field_name"].split(':')[1].replace(' ','_').lower()
								check_field = field["field_name"]
						if key not in database_crm_fields:
							api_crm_keys.append(key)
						elif crm_field_list == []:
							api_crm_keys.append(key)
					else:
						api_crm_keys.append(key)
				if not data_dict:
					crm_field_obj = CrmField.objects.filter(campaign__name=campaign.name)
					if crm_field_obj.exists():
						unique_field = crm_field_obj.first().unique_fields
						if unique_field:
							unique_field = unique_field[0]
				
				uniqueid = row.get(unique_field,None)
				if uniqueid is not None or settings.XML_INSERT_KEY=='':								
					update_contact = Contact.objects.filter(campaign=campaign.name,uniqueid=uniqueid).first()
					if action == "update":
						if update_contact:
							crm_field_dict = update_contact.customer_raw_data
						else:
							return JsonResponse({"msg":"No matching data found for update.",'status':'error'},status=500)	
					else:
						if update_contact and settings.XML_INSERT_KEY!='':
							return JsonResponse({"msg":"Respected data already present Cant create the New Data,Use Update Structure to update the data",'status':'error'},status=500)
				else:
					return JsonResponse({"msg":"Mandatory unique field is missing",'status':'error'},status=500)
				

				if crm_field_list:
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
				
				if api_crm_keys:
					for custom_fields in api_crm_keys:
						if unique_field == custom_fields:
							uniqueid = row.get(custom_fields,None)
							 
						sep_col_field = custom_fields.split(":")
						if sep_col_field[0].lower() not in crm_field_dict and len(sep_col_field) == 2:
							crm_field_dict[sep_col_field[0].lower()] ={}
						if len(sep_col_field) == 2:
							crm_field_dict[sep_col_field[0].lower()][sep_col_field[1].lower()] = row.get(custom_fields)
						elif len(sep_col_field) == 1 and sep_col_field[0].lower() not in contact_col_list:
							if "extra_information" not in crm_field_dict:
								crm_field_dict["extra_information"] = {}	
							crm_field_dict["extra_information"][sep_col_field[0].lower()] = row.get(custom_fields)

				if data_dict:
					return JsonResponse({"msg": "","status":"error","data":data_dict}, status=500)
				query = ''
				row['numeric'] = numeric
				contact_dict = { update_key: str(row[update_key]) for update_key in contact_col_list if update_key in row }		
				contact_dict["campaign"] = campaign.name
				priority = row.get("priority","")
				if row.get("priority","") == "":
					priority = None
				else:
					priority = int(priority)
				contact_dict["priority"] = priority
				contact_dict["customer_raw_data"] = crm_field_dict
				contact_dict["uniqueid"] = uniqueid
				contact_dict["phonebook_id"] =phonebook_id
				try:
					if action == "insert":
						Contact.objects.create(**contact_dict)
					else:
						update_contact.customer_raw_data = crm_field_dict
						update_contact.numeric = row['numeric']
						update_contact.save()
				except Exception as e:
					return JsonResponse({"msg": str(e),"status":"error","data":{}}, status=500)
				if error_dict:
					return JsonResponse({"msg": "Data successfully created","status":"success","data":contact_dict, 'crm_error':error_dict})
				else:
					msg = "created" if action == "insert" else "updated"
					return JsonResponse({"msg": "Data successfully "+msg,"status":"success","data":contact_dict})
			else:
				return JsonResponse({"msg":"Campaign is not Present",'status':'error'},status=500)		
		else:
			return JsonResponse({"msg":"Missing Mandatory Field Campaign and Numeric","status":"failed","a":request.data})

# class RecordingPlayAPIView(APIView):
# 	def get(self,request,file_name):
# 		s3fileDownloadToServer(file_name,"recordings/"+file_name,"/tmp/")
# 		with open("/tmp/"+file_name, 'rb') as fh:
# 			response = HttpResponse(fh.read(), content_type='audio/mpeg')
# 			response['Content-Disposition'] = 'attachment; filename=/tmp/%s' % file_name
# 			response['Accept-Ranges'] = 'bytes'
# 			response['X-Sendfile'] = file_name
# 			response['Content-Length'] = os.path.getsize("/tmp/"+file_name)
# 		return response
# 	def post(self,request,file_name):
# 		if settings.S3_PHONEBOOK_BUCKET_NAME:
# 			url = s3singedUrl(file_name)
# 			return JsonResponse({"msg":url},status=200)
# 		else:
# 			return JsonResponse({"msg",""},status=500)

class ApiBulkUpload(APIView):
	permission_classes = (IsAuthenticated, )
	def post(self,request):
		try:
			ser=ScheduleMasterContactSerializer(data=request.data,context={"request":request})
			if ser.is_valid():
				ser.save()
				return Response({"msg":"Successfully Scheduled",'ref_id':ser.data['ref_id']})
			else:
				return Response({"msg":"Failed to Schedule","error":str(ser.errors)})
		except Exception as e:
			return Response({"msg":"internal errors","error":str(e)})

class ApiBulkUploadStatus(APIView):
	permission_classes = (IsAuthenticated, )
	def get(self,request):
		try:
			status=ScheduleMasterContact.objects.get(ref_id=request.data['ref_id'])
			orginal_path='media/'+str(status.mcdata)
			orginal_count=pd.read_csv('/var/lib/flexydial/'+orginal_path)
			orginal_count=len(orginal_count.index)## orginal_count=orginal_count['unique_id'].tolist().count()

			if status.proper_mcdata:
				proper_path='media/'+str(status.proper_mcdata)
				proper_count=pd.read_csv('/var/lib/flexydial/'+proper_path)
				proper_count=len(proper_count.index)
			else:
				proper_path=''
				proper_count=''

			if status.improper_mcdata:
				improper_path='media/'+str(status.improper_mcdata)
				improper_count=pd.read_csv('/var/lib/flexydial/'+improper_path)
				improper_count=len(improper_count.index)
			else:
				improper_path=''
				improper_count=''

			return Response({"status is":status.status,'orginal path':str(orginal_path),"orginal_count":orginal_count,"proper path":str(proper_path),"proper count":proper_count,"improper path":str(improper_path),"improper count":improper_count})
			# return Response({"status is":status.status,'orginal path':str(orginal_path),"orginal_count":orginal_count})

		except Exception as e:
			return Response({"msg":"internal errors","error":str(e)})
class DownloadReportApiView(APIView):
	def get(self,request,pk,downloaded_file_name):
		file_name = DownloadReports.objects.filter(id=pk).order_by('-id').first()
		if file_name.downloaded_file.name.endswith('.csv'):
			reader = pd.read_csv(file_name.downloaded_file, low_memory=False, chunksize=10000, index_col=[0], encoding = "unicode_escape", escapechar='\\', na_filter=False)
			data = pd.concat(reader)
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename='+downloaded_file_name
			data.to_csv(path_or_buf=response,sep=',',float_format='%.2f',index=False,decimal=".")	
		else:
			with BytesIO() as b:
				data = pd.read_excel(file_name.downloaded_file)
				with pd.ExcelWriter(b) as writer:
					data.to_excel(writer, sheet_name="Data", index=False)
				response = HttpResponse(b.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
				response['Content-Disposition'] = 'attachment; filename='+downloaded_file_name
		return response
