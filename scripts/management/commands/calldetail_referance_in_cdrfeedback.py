from django.core.management.base import BaseCommand
from callcenter.models import CallDetail, CdrFeedbck

class Command(BaseCommand):

	help = "Update calldetail referance in cdrfeedbck model"

	def handle(self, **options):
		calldetail = CallDetail.objects.all().exclude(session_uuid=None).order_by('id')
		for cdr in calldetail:
			cdrfeedback = CdrFeedbck.objects.filter(session_uuid=cdr.session_uuid, calldetail=None).order_by('id')
			if cdrfeedback.exists():
				feedback = cdrfeedback.first()
				feedback.calldetail = cdr
				feedback.save()
		print('++++++ cdrfeedbck updated with calldetail referance ++++++++++')