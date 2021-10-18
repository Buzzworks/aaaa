from django.core.management.base import BaseCommand
from callcenter.models import Campaign, PhonebookBucketCampaign

class Command(BaseCommand):

	help = "Phonebook bucket campaign create"
	def handle(self, **options):
		campaign = Campaign.objects.values_list('id',flat=True)
		for camp in campaign:
			if PhonebookBucketCampaign.objects.filter(id=camp).exists():
				PhonebookBucketCampaign.objects.filter(id=camp).update(is_contact=True)
			else:
				PhonebookBucketCampaign.objects.create(id=camp, is_contact=True)

		print('!!!!!!! PhonebookBucketCampaign created with campaign and priority !!!!!!!')