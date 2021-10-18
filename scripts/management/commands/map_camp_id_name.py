from django.core.management.base import BaseCommand
from crm.models import *
from callcenter.models import *

class Command(BaseCommand):

	help = "Update campaign reference with name and id in campaign info"

	def handle(self, **options):
		old_crm_data = []
		old_lead_priority = []
		crm_fields = CrmField.objects.all()
		for crm in crm_fields:
			campaigns = crm.campaign.all().values_list('name',flat=True)
			old_crm_data.append({'id':crm.id,'campaigns':list(campaigns)})
		lead_pri = LeadListPriority.objects.all()
		for lp in lead_pri:
			old_lead_priority.append({'id':lp.id,'campaign':lp.campaign.name})
		print('****************************************')
		print(old_crm_data,'-----------', old_lead_priority)
		print('****************************************')
		CampaignInfo.objects.all().delete()
		campaign_data = Campaign.objects.all()
		for camp in campaign_data:
			CampaignInfo.objects.create(id=camp.id, name=camp.name)
		for crm in old_crm_data:
			crm_field = CrmField.objects.get(id=crm['id'])
			for crm_camp in crm['campaigns']:
				try:
					cpi = CampaignInfo.objects.get(name=crm_camp)
					crm_field.campaign.add(cpi)
				except Exception as e:
					print(crm_camp, 'campaign is not available')
		for lpr in old_lead_priority:
			try:
				cpi = CampaignInfo.objects.get(name=lpr['campaign'])
				LeadListPriority.objects.filter(id=lpr['id']).update(campaign_id=cpi.id)
			except Exception as e:
				print(lpr['campaign'], 'campaign is not available')
			
