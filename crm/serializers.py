import datetime
from rest_framework import serializers
from .models import (Phonebook, CrmField, TempContactInfo, Contact, LeadListPriority, DownloadReports, LeadBucket, AlternateContact)
from callcenter.models import CSS, CdrFeedbck, User,CallDetail

class PhoneBookSerializer(serializers.ModelSerializer):
	""" This serializer is used for phonebook display """
	class Meta:
		model = Phonebook
		fields = ('name', 'slug', 'description', 'campaign', 'priority',
			'caller_id', 'status', 'expire_date', 'order_by', 'duplicate_check')

class CrmFieldSerializer(serializers.ModelSerializer):
	""" This serializer is used for crmfields display """
	class Meta:
		model = CrmField
		fields = ('name', 'crm_fields','unique_fields')

class CrmFieldPaginationSerializer(serializers.ModelSerializer):
	""" This serializer is used for crm fields pagination  display """
	campaign_name = serializers.ReadOnlyField()
	class Meta:
		model = CrmField
		fields = ('name','id','campaign_name','created_by')


class AgentCrmFieldSerializer(serializers.ModelSerializer):
	""" This serializer is used for agent side crm fields  display """
	class Meta:
		model = CrmField
		fields = ('crm_fields','unique_fields')

class TempContactInfoSerializer(serializers.ModelSerializer):
	""" This serializer is used for Temp contact saving """
	class Meta:
		model = TempContactInfo
		fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
	""" This serializer is used for contact serializer display """
	contact_info = serializers.ReadOnlyField()
	last_verified_by = serializers.SerializerMethodField()
	alt_numeric = serializers.SerializerMethodField()
	class Meta:
		model = Contact
		fields = ('id','user', 'numeric', 'alt_numeric', 'first_name',
			'last_name', 'email', 'status', 'phonebook', 'campaign', 'contact_info', 'uniqueid','last_verified_by')
	def get_last_verified_by(self,obj):
		if obj.leadbucket_set.all():
			return obj.leadbucket_set.all().values('last_verified_by','created_by').first()
		else:
			return {'last_verified_by':'','created_by':''}

	def get_alt_numeric(self, obj):
		alt_number = {}
		alt_number_val = None
		if obj.uniqueid:
			alt_number_val = AlternateContact.objects.filter(uniqueid=obj.uniqueid).values('alt_numeric').first()
		if not alt_number_val:
			alt_number_val = AlternateContact.objects.filter(numeric=obj.numeric).values('alt_numeric').first()
		if alt_number_val:
			alt_number = alt_number_val['alt_numeric']
		return alt_number

class SetContactSerializer(serializers.ModelSerializer):
	""" This serializer is used for set contact serializer  display """
	class Meta:
		model = Contact
		fields = ('numeric', 'first_name','last_name', 'email', 'status', 'phonebook', 'campaign')

class DownloadContactSerializer(serializers.ModelSerializer):
	""" This serializer is used for download contact information """
	contact_info = serializers.ReadOnlyField()
	alt_numeric = serializers.SerializerMethodField()
	class Meta:
		model = Contact
		fields = ('id','user', 'numeric', 'alt_numeric', 'first_name',
			'last_name', 'email', 'status', 'phonebook', 'campaign', 'contact_info')

	def get_alt_numeric(self, obj):
		alt_number = {}
		alt_number_val = None
		if obj.uniqueid:
			alt_number_val = AlternateContact.objects.filter(uniqueid=obj.uniqueid).values('alt_numeric').first()
		if not alt_number_val:
			alt_number_val = AlternateContact.objects.filter(numeric=obj.numeric).values('alt_numeric').first()
		if alt_number_val:
			alt_number = alt_number_val['alt_numeric']
		return ','.join(alt_number.values())

class CssContactSerializer(serializers.ModelSerializer):
	""" This serializer is used for csscontact information """
	class Meta:
		model = Contact
		fields = ('id','user','numeric','status','phonebook','campaign')
		
class TempContactInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = TempContactInfo
		fields = '__all__'

class ContactListSerializer(serializers.ModelSerializer):
	""" This serializer is used for contactlist """
	phonebook = serializers.StringRelatedField()
	contact_info = serializers.ReadOnlyField()
	alt_numeric = serializers.SerializerMethodField()
	last_dialed_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	verified_to = serializers.SerializerMethodField()
	class Meta:
		model = Contact
		fields = '__all__'

	def get_alt_numeric(self, obj):
		alt_number = {}
		alt_number_val = None
		if obj.uniqueid:
			alt_number_val = AlternateContact.objects.filter(uniqueid=obj.uniqueid).values('alt_numeric').first()
		if not alt_number_val:
			alt_number_val = AlternateContact.objects.filter(numeric=obj.numeric).values('alt_numeric').first()
		if alt_number_val:
			alt_number = alt_number_val['alt_numeric']
		return ','.join(alt_number.values())
		
	def get_verified_to(self, obj):
		if obj.leadbucket_set.all():
			return obj.leadbucket_set.all().first().verified_to
		else:
			return ''

class EditContactListSerializer(serializers.ModelSerializer):
	""" This serializer is used for edit contactlist display """
	phonebook = serializers.StringRelatedField()
	contact_info = serializers.ReadOnlyField()
	alt_numeric = serializers.SerializerMethodField()
	last_dialed_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	verified_to = serializers.SerializerMethodField()
	class Meta:
		model = Contact
		fields = '__all__'

	def get_alt_numeric(self, obj):
		alt_number = {}
		alt_number_val = None
		if obj.uniqueid:
			alt_number_val = AlternateContact.objects.filter(uniqueid=obj.uniqueid).values('alt_numeric').first()
		if not alt_number_val:
			alt_number_val = AlternateContact.objects.filter(numeric=obj.numeric).values('alt_numeric').first()
		if alt_number_val:
			alt_number = alt_number_val['alt_numeric']
		return alt_number
		
	def get_verified_to(self, obj):
		if obj.leadbucket_set.all():
			return obj.leadbucket_set.all().first().verified_to
		else:
			return ''

class AssignedContactInfoSerializer(serializers.ModelSerializer):
	""" This serializer is used for to get the assigncontacts display """
	phonebook = serializers.SerializerMethodField('getPhoneBoookName')
	first_name = serializers.SerializerMethodField('getFirstName')
	last_name = serializers.SerializerMethodField('getLastName')
	class Meta:
		model = TempContactInfo
		fields = ('id', 'first_name', 'last_name', 'numeric', 'phonebook', 'campaign', 'status')

	def getPhoneBoookName(self, current_inst):
		if current_inst.phonebook:
			return current_inst.phonebook.name
		return ""

	def getFirstName(self, current_inst):
		if current_inst.contact:
			return current_inst.contact.first_name
		return ""

	def getLastName(self, current_inst):
		if current_inst.contact:
			return current_inst.contact.last_name
		return ""

class CrmFieldCustomSerializer(serializers.ModelSerializer):
	""" This serializer is used for crm fields is custom changes """
	isDisabled = serializers.SerializerMethodField('getisDisabled')
	campaign_name = serializers.ReadOnlyField()

	def getisDisabled(self, current_inst):
		campaigns = current_inst.campaign.all().values_list("name", flat=True)
		isDisabled=1
		for cam in campaigns:
			if CSS.objects.filter(campaign=cam).exists():
				isDisabled=0
		return isDisabled

	class Meta:
		model = CrmField
		fields = ('id', 'name', 'campaign_name', 'created_by', 'isDisabled')

class PhonebookRefreshSerializer(serializers.ModelSerializer):
	""" This serializer is used for leadlist refresh serializing  """
	percentage = serializers.ReadOnlyField()
	improper_file_name = serializers.ReadOnlyField()
	improper_file_path = serializers.ReadOnlyField()
	total_contact_count = serializers.SerializerMethodField()
	class Meta:
		model = Phonebook
		fields = ('name','id', 'campaign_name','percentage', 'improper_file_name', 'improper_file_path',
			'expire_date','created_by', 'status','last_updated_contact_count', 'total_contact_count')

	def get_total_contact_count(self,obj):
		return obj.contacts.count()

class LeadListPrioritySerializer(serializers.ModelSerializer):
	""" This serializer is used for leadlist priority data display """
	campaign = serializers.StringRelatedField()
	class Meta:
		model = LeadListPriority
		fields = ('uniqueid','id','priority','campaign','date')


class DownloadReportsSerializer(serializers.ModelSerializer):
	""" This serializer is used for Downloadreport serializer  """
	percentage = serializers.ReadOnlyField()
	downloaded_file_name = serializers.ReadOnlyField()
	downloaded_file_path = serializers.ReadOnlyField()
	reportstart_date = serializers.ReadOnlyField()
	reportend_date = serializers.ReadOnlyField()
	download_actions = serializers.SerializerMethodField('getActions')
	class Meta:
		model = DownloadReports
		fields = ('id', 'report','reportstart_date','reportend_date','percentage', 'downloaded_file_name', 'downloaded_file_path','download_actions','user')
	def getActions(self, current_inst):
		actions = {"start":False, "delete":True, "stop":False}
		if current_inst.is_start or current_inst.status:
			actions['stop'] = True
		else:
			actions['start'] = True
		return actions

class LeadBucketSerializer(serializers.ModelSerializer):
	""" This serializer is used for leadbucket display"""
	contact = ContactListSerializer()
	class Meta:
		model = LeadBucket
		fields = '__all__'

class AlternateContactSerializer(serializers.ModelSerializer):
	""" This serializer is used for Alternative contact  """
	alt_numeric = serializers.SerializerMethodField()
	created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	class Meta:
		model = AlternateContact
		fields = '__all__'
	def get_alt_numeric(self, obj):
		return ','.join(obj.alt_numeric.values())

class UniqueSerializer(serializers.ModelSerializer):
	cdr_feedback = serializers.SerializerMethodField()
	c_name=serializers.SerializerMethodField()
	pl=serializers.SerializerMethodField()
	customer_cid_count = serializers.SerializerMethodField()
	
	class Meta:
		model = Contact
		fields = ('c_name','pl','numeric','campaign','cdr_feedback','customer_cid_count')

	def get_customer_cid_count(self,obj):
		count=CallDetail.objects.filter(created__lte=datetime.datetime.today(), created__gt=datetime.datetime.today()-datetime.timedelta(days=30),campaign_name=obj['campaign'],customer_cid=obj['numeric']).count()
		return count

	def get_c_name(self,obj):
		full_name = ''
		
		# contact=''
		# if obj and obj.customer_raw_data and 'customer_details' in contact.customer_raw_data:
		# 	if "first_name" in contact.customer_raw_data['customer_details'] and contact.customer_raw_data['customer_details']['first_name'] != None:
		# 		full_name += contact.customer_raw_data['customer_details']['first_name'] + ' '
		# 	if "middle_name" in contact.customer_raw_data['customer_details'] and contact.customer_raw_data['customer_details']['middle_name'] != None:
		# 		full_name += contact.customer_raw_data['customer_details']['middle_name'] + ' '
		# 	if "last_name" in contact.customer_raw_data['customer_details'] and contact.customer_raw_data['customer_details']['last_name'] != None:
		# 		full_name += contact.customer_raw_data['customer_details']['last_name']
		return full_name.strip()

	def get_cdr_feedback(self,obj):
		max_id=CallDetail.objects.filter(customer_cid=obj['numeric'],campaign_name=obj['campaign']).order_by("-id").first().id
		cdr_feedback = {"primary_dispo":"","secondary_dispo":""}
		if max_id:
			cdr_obj=CdrFeedbck.objects.filter(calldetail_id=max_id).first()
			if cdr_obj:
				primary_dispo=cdr_obj.primary_dispo
				cdr_fb = cdr_obj.feedback
				if primary_dispo:
					cdr_feedback["primary_dispo"] = primary_dispo
				if cdr_fb and 'sub_dispo' in cdr_fb:
					sub=cdr_fb['sub_dispo']
					if sub:
						cdr_feedback["secondary_dispo"]=cdr_fb[sub]
		return cdr_feedback

	def get_pl(self,obj):
		pl = {'phonenumber':"",'actionid':"",'name':"",'source':"",'flag':"",'last_comp_stage':"",'application_number':"",'reg_date_time':"",'campaign1':"",'filler1':"",'filler2':""}
		if obj and obj['customer_raw_data']:
			if 'pl' in obj['customer_raw_data'] and 'phonenumber' in obj['customer_raw_data']['pl']:
				pl['phonenumber']=obj['customer_raw_data']['pl']['phonenumber']
			if 'pl' in obj['customer_raw_data'] and 'actionid' in obj['customer_raw_data']['pl']:
				pl['actionid']=obj['customer_raw_data']['pl']['actionid']
			if 'pl' in obj['customer_raw_data'] and 'name' in obj['customer_raw_data']['pl']:
				pl['name']=obj['customer_raw_data']['pl']['name']
			if 'pl' in obj['customer_raw_data'] and 'source' in obj['customer_raw_data']['pl']:
				pl['source']=obj['customer_raw_data']['pl']['source']
			if 'pl' in obj['customer_raw_data'] and 'source' in obj['customer_raw_data']['pl']:
				pl['source']=obj['customer_raw_data']['pl']['source']
			if 'pl' in obj['customer_raw_data'] and 'flag' in obj['customer_raw_data']['pl']:
				pl['flag']=obj['customer_raw_data']['pl']['flag']
			if 'pl' in obj['customer_raw_data'] and 'last_comp_stage' in obj['customer_raw_data']['pl']:
				pl['last_comp_stage']=obj['customer_raw_data']['pl']['last_comp_stage']
			if 'pl' in obj['customer_raw_data'] and 'application_number' in obj['customer_raw_data']['pl']:
				pl['application_number']=obj['customer_raw_data']['pl']['application_number']
			if 'pl' in obj['customer_raw_data'] and 'reg_date_time' in obj['customer_raw_data']['pl']:
				pl['reg_date_time']=obj['customer_raw_data']['pl']['reg_date_time']
			if 'pl' in obj['customer_raw_data'] and 'campaign1' in obj['customer_raw_data']['pl']:
				pl['campaign1']=obj['customer_raw_data']['pl']['campaign1']
			if 'pl' in obj['customer_raw_data'] and 'filler1' in obj['customer_raw_data']['pl']:
				pl['filler1']=obj['customer_raw_data']['pl']['filler1']
			if 'pl' in obj['customer_raw_data'] and 'filler2' in obj['customer_raw_data']['pl']:
				pl['filler2']=obj['customer_raw_data']['pl']['filler2']
		return pl
		