from django.core.management.base import BaseCommand
import requests, os, subprocess
from django.conf import settings

class Command(BaseCommand):

	help = "Create directory xml file"

	def handle(self, **options):
		try:
			if not os.path.exists('/usr/local/src/flexydial/static/fs_config'):
				os.mkdir('/usr/local/src/flexydial/static/fs_config', 0o777)
			response = requests.get('https://'+str(settings.IP_ADDRESS)+'/api/config/directory/call_server/', verify=False) 
			if response.status_code == 200:
				print("directory xml")
				with open("/usr/local/src/flexydial/static/fs_config/directory.xml", "wb") as f:
					f.write(response.text.encode())
			if response.status_code == 200:
				print("callcenter.xml")
				response = requests.get('https://'+str(settings.IP_ADDRESS)+'/api/config/callcenter/call_server/', verify=False) 
				with open("/usr/local/src/flexydial/static/fs_config/callcenter.xml", "wb") as f:
					f.write(response.text.encode())
			subprocess.call(['chmod', '-R', '777', '/usr/local/src/flexydial/static/fs_config'])
		except Exception as e:
			print(e)
			return "Something went wrong:"