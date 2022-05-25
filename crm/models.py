from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.postgres.fields import JSONField, HStoreField
from datetime import datetime
from django.db.models import signals
import os
import json
import uuid
from callcenter.models import (Campaign,DataUploadLog, CALLBACK_MODE)
from flexydial.constants import (Status, CONTACT_STATUS, ORDER_BY)
from crm.s3_fileoperations import fileTransferToCloudStorage, cloudStoragefileDownloadToServer

# Create your models here.
short_uuid = str(uuid.uuid4())[:8]

class Phonebook(models.Model):
	"""
	This model is for storing the crm data file.
	"""
	site = models.ForeignKey(Site, default=settings.SITE_ID, editable=False,
			on_delete=models.CASCADE,null=True)
	name = models.CharField(max_length=100,db_index=True)
	slug = models.SlugField(max_length=100)
	description = models.TextField(default='')
	contact_file = models.FileField(upload_to='upload', blank=True,
			help_text='Csv fields: number, alt number, state, first name,'\
			'last name, email, description')
	campaign = models.CharField(max_length=100,db_index=True)
	priority = models.IntegerField(default=0)
	caller_id = models.BigIntegerField(default=0)
	status = models.CharField(default='Active',choices=Status,db_index=True,max_length=10)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	expire_date = models.DateTimeField(null=True, blank=True)
	order_by = models.CharField(default=ORDER_BY[0][0], choices=ORDER_BY, max_length=10)
	duplicate_check = models.CharField(max_length=100, blank=True, null=True)
	deleted_contact_file = models.FileField(upload_to='upload', blank=True)
	transfer_contact_file = models.FileField(upload_to='upload', blank=True)
	last_updated_contact_count = models.IntegerField(default=0)
	created_by = models.CharField(max_length=100, blank=True, null=True)
	class Meta:
		ordering = ['-modified_date']
		unique_together = (
				('name', 'slug'),
				)
		verbose_name = 'Lead List'
		verbose_name_plural = 'Lead List'
	def __str__(self):
		return str(self.name)

	@property
	def contact_file_name(self):
		if self.contact_file:
			return os.path.basename(self.contact_file.name)

	@property
	def campaign_name(self):
		if self.campaign:
			try:
				return Campaign.objects.get(id=self.campaign).name
			except:
				None

	@property
	def percentage(self):
		job_id = self.campaign.replace(" ", "")+self.name.replace(" ", "")+str(self.id)
		data_upload_inst = DataUploadLog.objects.filter(job_id=job_id)
		completed_percentage = 0
		if data_upload_inst.exists():
			completed_percentage = data_upload_inst.first().completed_percentage
		return completed_percentage

	@property
	def improper_file_name(self):
		job_id = self.campaign.replace(" ", "")+self.name.replace(" ", "")+str(self.id)
		data_upload_inst = DataUploadLog.objects.filter(job_id=job_id)
		improper_file = ""
		if data_upload_inst.exists() and data_upload_inst.first().improper_file:
			improper_file = data_upload_inst.first().improper_file.name
			improper_file = os.path.basename(improper_file)
		return improper_file

	@property
	def improper_file_path(self):
		job_id = self.campaign.replace(" ", "")+self.name.replace(" ", "")+str(self.id)
		data_upload_inst = DataUploadLog.objects.filter(job_id=job_id)
		improper_file = ""
		if data_upload_inst.exists() and data_upload_inst.first().improper_file:
			improper_file = data_upload_inst.first().improper_file.path
		return improper_file

	@property
	def deleted_contact_file_name(self):
		if self.deleted_contact_file:
			return os.path.basename(self.deleted_contact_file.name)

	@property
	def transfer_contact_file_name(self):
		if self.transfer_contact_file:
			return os.path.basename(self.transfer_contact_file.name)
		  
class Contact(models.Model):
	"""
	This model is for storing the customer contact data for dialler dialling purpose.
	"""
	site = models.ForeignKey(Site, default=settings.SITE_ID, editable=False,
			on_delete=models.SET_NULL,null=True)
	phonebook = models.ForeignKey(Phonebook, related_name="contacts", null=True,
		on_delete=models.CASCADE, blank=True,db_index=True, verbose_name="Lead List")
	campaign = models.CharField(max_length=100,null=True,blank=True,db_index=True)
	user = models.CharField(max_length=100,null=True,blank=True)
	numeric  = models.CharField(default='', max_length=50,null=True, db_index=True)
	alt_numeric = HStoreField(default=dict)
	first_name	= models.CharField(default='', max_length=100)
	last_name	= models.CharField(default='', max_length=100)
	email	= models.EmailField(max_length=100, db_index=True, null=True, blank=True)
	disposition = models.CharField(max_length=100,null=True,blank=True)
	churncount = models.IntegerField(default=0)
	priority = models.IntegerField(default=None,blank=True, null=True)
	uniqueid  = models.CharField(max_length =30, blank=True, null=True)
	status  = models.CharField(default=CONTACT_STATUS[0][0],choices=CONTACT_STATUS,db_index=True,max_length=30)
	dial_count = models.IntegerField(default=0,blank=True, null=True)
	customer_raw_data = JSONField(default=dict)
	last_dialed_date = models.DateTimeField(auto_now_add=True,null=True,blank=True,db_index=True)
	last_connected_user = models.CharField(max_length=100,null=True,blank=True)
	created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True,db_index=True,)
	modified_date = models.DateTimeField(auto_now=True,null=True,blank=True,db_index=True,)
	@property
	def contact_info(self):
		return self.customer_raw_data
		
	def __str__(self):
		return str(self.numeric)


class ContactInfo(models.Model):
	"""
	This model is for storing the customer raw data for agent communication purpose.
	"""
	contact = models.ForeignKey(Contact, related_name="contacts", db_index=True,null=True,
		on_delete=models.CASCADE, blank=True)
	customer_raw_data = JSONField()
	class Meta:
		get_latest_by = 'id'
		ordering = ['-id']		
	def __str__(self):
		return str(self.contact)	

class CampaignInfo(models.Model):
	name = models.CharField(max_length=100) 
	
	def __str__(self):
		return str(self.name)

class CrmField(models.Model):
	"""
	This model is used to add custom fields to phonebook contact
	"""
	name = models.CharField(max_length=100,db_index=True)
	campaign = models.ManyToManyField(CampaignInfo, related_name="campaign_info",
		blank=True, null=True)
	crm_fields = JSONField(blank=True, null=True)
	unique_fields = JSONField(default=list)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	created_by = models.CharField(max_length=100, blank=True, null=True)

	class Meta:
		get_latest_by = '-id'
		ordering = ['-id']	
		
	@property
	def campaign_name(self):
		if self.campaign:
			campaign_list = self.campaign.all().values_list("name", flat=True)
			return ', '.join(campaign_list)

	@property
	def campaign_list(self):
		if self.campaign_name:
			return self.campaign_name.replace(' ', '').split(",")
	
		
	def __str__(self):
		return str(self.name)

class TempContactInfoModelManager(models.Manager):
	def bulk_create(self, objs, **kwargs):
		pre_count = TempContactInfo.objects.filter(campaign=objs[0].campaign).count()
		if pre_count == 0: 
			settings.R_SERVER.publish('lead-details',message=json.dumps({'campaign':objs[0].campaign}))	
		super().bulk_create(objs,**kwargs)

    	
class TempContactInfo(models.Model):
	"""
	This model is for storing the customer contact data for dialler dialling purpose.
	"""
	site = models.ForeignKey(Site, default=settings.SITE_ID, editable=False,
			on_delete=models.CASCADE,null=True)
	contact = models.ForeignKey(Contact, editable=False,
			on_delete=models.CASCADE,null=True)
	campaign = models.CharField(max_length=100,null=True, blank=True) 
	phonebook = models.ForeignKey(Phonebook, related_name="tempcontacts", null=True,
		on_delete=models.CASCADE, blank=True,db_index=True)
	user = models.CharField(max_length=100,null=True)
	numeric  = models.CharField(default='', max_length=50,null=True, db_index=True)
	alt_numeric = HStoreField(default=dict)
	priority = models.IntegerField(default=None, blank=True, null=True)
	uniqueid  = models.CharField(max_length =30, blank=True, null=True)
	email	= models.EmailField(max_length=100, db_index=True, null=True, blank=True)
	status  = models.CharField(default=CONTACT_STATUS[0][0],choices=CONTACT_STATUS,db_index=True,max_length=15)
	previous_status = models.CharField(default=CONTACT_STATUS[0][0],choices=CONTACT_STATUS,db_index=True,max_length=15)
	created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	modified_date = models.DateTimeField(auto_now=True,null=True,blank=True)	
	objects = TempContactInfoModelManager()
	def __str__(self):
		return str(self.numeric)
	


class TrashContact(models.Model):
	"""
	This model is for storing the customer contact data when reffernce phonebook deleted
	"""
	site = models.ForeignKey(Site, default=settings.SITE_ID, editable=False,
			on_delete=models.SET_NULL,null=True)
	phonebook = models.CharField(max_length=100, null=True, blank=True)
	user = models.CharField(max_length=100,null=True,blank=True)
	numeric  = models.CharField(default='', max_length=50,null=True, db_index=True)
	alt_numeric = HStoreField(default=dict)
	first_name	= models.CharField(default='', max_length=50)
	last_name	= models.CharField(default='', max_length=50)
	email	= models.EmailField(max_length=100, db_index=True, null=True, blank=True)
	disposition = models.CharField(max_length=100,null=True,blank=True)
	status  = models.CharField(default=CONTACT_STATUS[0][0],choices=CONTACT_STATUS,db_index=True,max_length=30)
	customer_raw_data = JSONField()
	created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
				
	def __str__(self):
		return str(self.numeric)

class LeadListPriority(models.Model):
	"""
	This model is for storing the Lead List Priority
	"""
	site = models.ForeignKey(Site, default=settings.SITE_ID, editable=False,
			on_delete=models.SET_NULL,null=True)
	uniqueid  = models.CharField(max_length =30)
	priority = models.IntegerField(default=None,blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	campaign = models.ForeignKey(CampaignInfo,on_delete=models.SET_NULL, null=True, blank=True)
	is_global = models.BooleanField(default=False)
	class Meta:
		unique_together = (('uniqueid', 'campaign'),)
	@property
	def date(self):
		return self.created_date.strftime("%d-%m-%Y %H:%M:%S")

def get_upload_path(instance, filename):
	return  'download/{0}/{1}/{2}'.format(datetime.now().strftime("%m.%d.%Y"),str(instance.user), filename)


class DownloadReports(models.Model):
	"""
	This model is for storing the Download Report in background with scheduled task
	"""
	site = models.ForeignKey(Site, default=settings.SITE_ID, editable=False,
			on_delete=models.SET_NULL,null=True)
	report = models.CharField(max_length=100,null=True,blank=True)
	serializers = models.CharField(max_length=100,null=True,blank=True)
	col_list = JSONField(default=dict, blank=True, null=True)
	filters = JSONField(default=dict, blank=True, null=True)
	arguments = JSONField(default=dict, blank=True, null=True)
	user = models.IntegerField(default=None,blank=True, null=True)
	status = models.BooleanField(default=False)
	view = models.BooleanField(default=False)
	is_start = models.BooleanField(default=False)
	downloaded_file = models.FileField(upload_to=get_upload_path, blank=True, help_text='Click to downlad file')
	start_date = models.DateTimeField(auto_now_add=True,null=True,blank=True,db_index=True,)
	end_date = models.DateTimeField(auto_now=True,null=True,blank=True,db_index=True,)

	@property
	def downloaded_file_name(self):
		improper_file = ''
		if self.downloaded_file:
			improper_file = os.path.basename(self.downloaded_file.name)
		return improper_file
	@property
	def downloaded_file_path(self):
		improper_file = ''
		if self.downloaded_file:
			improper_file = self.downloaded_file.url
		return improper_file
	@property
	def percentage(self):
		completed_percentage = 0
		if not self.downloaded_file:
			if not self.is_start and not self.status:
				completed_percentage = 'File not created / Data not available'
			else:
				completed_percentage = 'In Progress'
		else:
			completed_percentage = 100
		return completed_percentage
	@property
	def reportstart_date(self):
		start_date = '-'
		if 'start_date' in self.filters:
			start_date = self.filters['start_date']
		return start_date
	@property
	def reportend_date(self):
		end_date = '-'
		if 'end_date' in self.filters:
			end_date = self.filters['end_date']
		return end_date


class LeadBucket(models.Model):
	"""
	This table contain higher level lead refrence
	"""
	site = models.ForeignKey(Site, default=settings.SITE_ID, editable=False,
			on_delete=models.SET_NULL,null=True)
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, db_index=True)
	created_by = models.CharField(max_length=100,null=True,blank=True)
	last_verified_by = models.CharField(max_length=100,null=True,blank=True)
	verified_to = models.CharField(max_length=100,null=True,blank=True)
	reverify_lead = models.BooleanField(default=False)

class FIleModelField(models.FileField):
	def pre_save(self, model_instance, add,**kwargs):
		file = super().pre_save(model_instance, add)
		if file and not file._committed:
			# Commit the file to storage prior to saving the model
			file.save(file.name, file.file, save=False)
		try:
			if settings.S3_PHONEBOOK_BUCKET_NAME or settings.S3_GCLOUD_BUCKET_NAME:
				if add:
					fileTransferToCloudStorage(self,file.name,file.name)
				else:
					cloudStoragefileDownloadToServer(self,file.name,file.name)
		except Exception as e:
			print("Error :: File Upload/Download in Cloud Server",e)
		return file
class PhoneBookUpload(models.Model):
	""" This model is used to the phonebook upload status"""
	site = models.ForeignKey(Site, default=settings.SITE_ID, editable=False,
			on_delete=models.SET_NULL,null=True)	
	phonebook_file = models.FileField(upload_to='upload', blank=True)
	phone_inst = models.ForeignKey(Phonebook, related_name="phonebook_upload", null=True,
		on_delete=models.CASCADE, blank=True)
	duplicate_check = models.CharField(max_length=100,null=True,blank=True)
	action_type = models.CharField(max_length=100,null=True,blank=True)
	search_type = models.CharField(max_length=100,null=True,blank=True)
	column_names = JSONField(default=list)
	created_date = models.DateTimeField(auto_now_add=True)
	created_by = models.CharField(max_length=100,null=True)
	is_start = models.BooleanField(default=False)



class AlternateContact(models.Model):
	""" 
	This model is used to store alternate contacts
	"""
	numeric = models.CharField(default='', max_length=50,null=True)
	uniqueid  = models.CharField(max_length =30, blank=True, null=True)
	alt_numeric = HStoreField(default=dict)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['id']