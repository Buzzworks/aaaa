from django.core.management.base import BaseCommand
from callcenter.models import CallDetail, DiallerEventLog, Campaign, StickyAgent
from django.db.models import Q
class Command(BaseCommand):

	help = "Update calldetail referance in cdrfeedbck model"

	def handle(self, **options):
		campaigns = Campaign.objects.all()
		for camp in campaigns:
			CallDetail.objects.filter(Q(campaign_id = camp.id),Q(campaign_name=None)|Q(campaign_name='')).update(campaign_name=camp.name)
			DiallerEventLog.objects.filter(Q(campaign_id = camp.id),Q(campaign_name=None)|Q(campaign_name='')).update(campaign_name=camp.name)
			StickyAgent.objects.filter(Q(campaign_id = camp.id),Q(campaign_name=None)|Q(campaign_name='')).update(campaign_name=camp.name)
		print('++++++ campaign name updated in CallDetail and DiallerEventLog ++++++++++')