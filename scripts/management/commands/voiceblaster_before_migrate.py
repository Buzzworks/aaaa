from django.core.management.base import BaseCommand
from callcenter.models import Campaign
from xlwt import *

class Command(BaseCommand):

	help = "Phonebook bucket campaign create"
	def handle(self, **options):
		campaign = Campaign.objects.all()
		wb = Workbook()
		sheet1 = wb.add_sheet('Sheet 1')
		sheet1.write(0,0, 'id')
		sheet1.write(0,1, 'name')
		sheet1.write(0,2, 'voice_blaster')
		sheet1.write(0,3, 'vb_mode')
		sheet1.write(0,4, 'vb_audio')
		sheet1.write(0,5, 'vb_data')
		for index, camp in enumerate(campaign):
			if camp.voice_blaster == True:
				sheet1.write(index, 0, camp.id)
				sheet1.write(index, 1, camp.name)
				sheet1.write(index, 2, camp.voice_blaster)
				sheet1.write(index, 3, camp.vb_mode)
				if camp.vb_audio:
					sheet1.write(index,	4, camp.vb_audio.id)
				else:
					sheet1.write(index,	4, '')
				sheet1.write(index, 5, str(camp.vb_data))
		wb.save('voice_blaster.xls')
		print("Saved the data----------------")