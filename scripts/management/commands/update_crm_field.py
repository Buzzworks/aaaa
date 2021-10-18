from django.core.management.base import BaseCommand
from crm.models import CrmField,Contact
from callcenter.models import Campaign
import re


class Command(BaseCommand):
	help = "Update crm field"
	def handle(self, **options):
		old_crm_fields=[]
		old_contact_fields=[]
		contact_section_list = []
		crm_queryset = None
		contact_queryset = None
		campaign_name = input("Enter the Campaign Name : ")
		camp_obj = Campaign.objects.filter(slug=campaign_name)
		if camp_obj.exists():
			crm_queryset = CrmField.objects.filter(campaign__name=campaign_name)
			contact_queryset = Contact.objects.filter(campaign=campaign_name)
		if crm_queryset:
			#To get old_crm_fields
			for i in crm_queryset:
				sections_data=i.crm_fields
				for section_data in sections_data:
					section_fields = section_data['section_fields']
					for fields in section_fields:
						field=fields['field']
						if field not in old_crm_fields:
							old_crm_fields.append(field)
			print("**********************************************************")
			print("!!!!!!!! AVALIABLE CRM FIELDS IN THE APPLICATION  !!!!!!!!")
			print("**********************************************************")			
			print(old_crm_fields)
		if contact_queryset:
			#To get old_contact_fields 
			for i in contact_queryset:
				cust_raw_data = i.customer_raw_data
				sections = cust_raw_data.keys()
				for section in sections:
					#fields_in_section = list(cust_raw_data[section].keys())
					for field in list(cust_raw_data[section].keys()):
						if field not in old_contact_fields:
							old_contact_fields.append(field)
			print("**************************************************************")
			print("!!!!!!!! AVALIABLE CONTACT FIELDS IN THE APPLICATION  !!!!!!!!")
			print("**************************************************************")
			print(old_contact_fields)

		regex = "[^a-zA-Z0-9_]+"
		p=re.compile(regex)
		old_field = input("Enter old crm field to update : ")
		new_field = input("Enter new crm field           : ")
		if contact_queryset and crm_queryset and old_field in old_crm_fields and old_field.lower().replace(' ','_') in old_contact_fields:
			crm_field_update(crm_queryset,old_field,new_field,p)
			contact_update(contact_queryset,old_field,new_field,p)
		elif crm_queryset and old_field in old_crm_fields:
			crm_field_update(crm_queryset,old_field,new_field,p)
		elif contact_queryset and old_field.lower().replace(' ','_') in old_contact_fields:
			contact_update(contact_queryset,old_field,new_field,p)
		else:
			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			print(f"***** Entered {old_field} Field not available in Contact and CRM ****")
			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		



def crm_field_update(crm_queryset,old_field,new_field,p):
	try:
		if not(re.search(p, new_field)):
			update_crm=input(f"Do you want to update {old_field} in CRM,(yes/no) : ")
			if update_crm in ("yes","y"):
				crm_count = 0
				for i in crm_queryset:
					sections_data=i.crm_fields
					for section_data in sections_data:
						section_fields = section_data['section_fields']
						for fields in section_fields:
							field=fields['field'] 
							if fields['field']==old_field:
								fields['field']=new_field
								fields['db_field']=new_field.lower().replace(' ','_')
								i.save()
								crm_count += 1
					if crm_count % 2 == 0:
						print(crm_count," has been updated")
				print("********************************************************")
				print(f"!!!!!!!! {crm_count} CRM UPDATED SUCCESSFULLY  !!!!!!!!")
				print("********************************************************")
			else:
				pass
		else:
			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			print("***** Special Characters are not allowed except '_' ,kindly enter proper new_field ****")
			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	except Exception as e:
		print(e)

def contact_update(contact_queryset,old_field,new_field,p):
	try:
		if not(re.search(p, new_field)):
			update_contact=input(f"Do you want to update {old_field} in Contact ,(yes/no) : ")
			if update_contact in ("yes","y"):
				contact_old_field = old_field.lower().replace(' ','_')
				count = 0 
				for i in contact_queryset:
					cust_raw_data = i.customer_raw_data
					sections = cust_raw_data.keys()
					for section in sections:
						fields_in_section = list(cust_raw_data[section].keys())
						for field in fields_in_section:
							if field==contact_old_field:
								db_field = new_field.lower().replace(' ','_')
								cust_raw_data[section][db_field]=cust_raw_data[section][field]
								del cust_raw_data[section][field] 
								i.save()
								count += 1
					if count % 100 == 0:
						print(count," has been updated")
				print("*******************************************************")
				print(f"!!!!!!!! {count} CONTACT UPDATED SUCCESSFULLY  !!!!!!!!")
				print("*******************************************************")
			else:
				pass
		else:
			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			print("***** Special Characters are not allowed except '_' ,kindly enter proper new_field ****")
			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")		
	except Exception as e:
		print(e)