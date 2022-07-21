from django.core.management.base import BaseCommand
from django.conf import settings 
from callcenter.models import AudioFile

class Command(BaseCommand):

	help = "Upload Audio into Call Server"

	def handle(self, **options):
			bob_p=settings.R_SERVER.pubsub()
			bob_p.subscribe('audiofile_callserver')
			for message in bob_p.listen():
				if message and message['type']!='subscribe':
					try:
						audio = AudioFile.objects.filter(
							id=message['data'].decode("utf-8") ).first()
						if audio.audio_file:
							audiofile = audio.audio_file.read()
							if audiofile:
								print(audio.audio_file.name)
								with open(settings.MEDIA_ROOT+"/"+audio.audio_file.name, 'wb') as f:
									f.write(audiofile)
					except Exception as e:
						print(e)
