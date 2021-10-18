from django.core.management.base import BaseCommand
from callcenter.models import CallDetail, CdrFeedbck, DiallerEventLog
import random 
from datetime import datetime, timedelta
from flexydial import settings
class Command(BaseCommand):

	help = "create call details andcdrfeedback "

	def handle(self, **options):
		number_list = ['9032303477','8466993388']
		unique_id = []
		user_id =['3','4','5','6']
		dispo=['NC','Connected','PIP','NCP','SIP','TCP','UDP']
		comment =['dummy for testing', "dummy for testing 11 ","dummy for testing 123","dummy for testing 3456",
		"dummy for testing4789","dummy for testing 14563"]

		def random_datetime():
			start_date = datetime(2020, 12, 1)
			end_date = datetime(2020, 12, 10)
			time_between_dates = end_date - start_date
			days_between_dates = time_between_dates.days
			random_number_of_days = random.randrange(days_between_dates)
			random_date = start_date + timedelta(days=random_number_of_days)
			return random_date

		for u in range(100,1000):
			unique_id.append(u)

		for i in range(1,50):
			CallDetail.objects.create(id=i,site_id=1,customer_cid=random.choice(number_list), 
				contact_id=i, uniqueid=random.choice(unique_id), user_id=random.choice(user_id),
				init_time=random_datetime(),session_uuid=settings.URL_PARAMETER, created=random_datetime())
			DiallerEventLog.objects.create(id=i,site_id=1,customer_cid=random.choice(number_list), 
				contact_id=i, uniqueid=random.choice(unique_id), user_id=random.choice(user_id),
				init_time=random_datetime(), session_uuid=settings.URL_PARAMETER, created=random_datetime())
			CdrFeedbck.objects.create(id=i,contact_id=i,primary_dispo=random.choice(dispo),
			 	feedback={},calldetail_id=i,comment=random.choice(comment), relation_tag={})
			if (i % 10000 == 0):
				print(i, 'CallDetail and dialler eventlog and cdr  updated')