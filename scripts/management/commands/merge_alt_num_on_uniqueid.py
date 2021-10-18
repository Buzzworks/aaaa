from django.core.management.base import BaseCommand
from django.db.models import Count
from crm.models import AlternateContact, Contact

class Command(BaseCommand):

	help = "Remove recurrent data from alternate number table from uniqueid"

	def handle(self, **options):
		uniqueids = list(AlternateContact.objects.values('uniqueid').exclude(uniqueid=None).annotate(Count('uniqueid')).order_by('uniqueid').filter(uniqueid__count__gt=1).values_list('uniqueid',flat=True))
		for index, uniqueid in enumerate(uniqueids):
			alternate_numbers = AlternateContact.objects.filter(uniqueid=uniqueid).values_list('alt_numeric',flat=True).order_by('id')
			alt_num_dict = {}
			for alt_num in alternate_numbers:
				for alt_name_key, alt_name_val in alt_num.items():
					if alt_name_val.strip() not in alt_num_dict.values():
						if alt_name_key.strip() in alt_num_dict:
							key_count = 1
							temp_alt_name_key = alt_name_key.strip()+'_'+str(key_count)
							while temp_alt_name_key in alt_num_dict.keys():
								key_count +=1
								temp_alt_name_key = alt_name_key.strip()+'_'+str(key_count)
							alt_num_dict[temp_alt_name_key] = alt_name_val.strip()
						else:
							alt_num_dict[alt_name_key.strip()] = alt_name_val.strip()
			alt_num_obj = AlternateContact.objects.filter(uniqueid=uniqueid).order_by('id').first()
			alt_num_obj.alt_numeric = alt_num_dict
			alt_num_obj.save()
			AlternateContact.objects.filter(uniqueid=uniqueid).exclude(id=alt_num_obj.id).delete()
			if (index+1 % 1000 == 0):
				print(index, 'alternate number merged base on uniqueid')
		print('======',len(uniqueids), 'alternate number merged base on uniqueid =====')
		
		contacts = Contact.objects.exclude(uniqueid='').exclude(uniqueid=None).exclude(alt_numeric={}).values('uniqueid','alt_numeric','numeric')
		for index, contact in enumerate(contacts):
			alt_obj = AlternateContact.objects.filter(uniqueid=contact['uniqueid'])
			if alt_obj.exists():
				alt_obj = alt_obj.first()
				alt_num_dict = alt_obj.alt_numeric.copy()
				for alt_name_key, alt_name_val in contact['alt_numeric'].items():
					if alt_name_val.strip() not in alt_num_dict.values():
						if alt_name_key.strip() in alt_num_dict:
							key_count = 1
							temp_alt_name_key = alt_name_key.strip()+'_'+str(key_count)
							while temp_alt_name_key in alt_num_dict.keys():
								key_count +=1
								temp_alt_name_key = alt_name_key.strip()+'_'+str(key_count)
							alt_num_dict[temp_alt_name_key] = alt_name_val.strip()
						else:
							alt_num_dict[alt_name_key.strip()] = alt_name_val.strip()
				alt_obj.alt_numeric = alt_num_dict
				alt_obj.save()
			else:
				AlternateContact.objects.create(numeric=contact['numeric'], uniqueid=contact['uniqueid'], alt_numeric=contact['alt_numeric'])
			if (index+1 % 1000 == 0):
				print(index, 'alternate number updated base on uniqueid from contact')
		print('======',len(contacts), 'alternate number updated base on uniqueid from contact =====')



