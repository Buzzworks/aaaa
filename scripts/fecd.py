import ESL
import louie
import json
import uuid
import time
from django.conf import settings
def run_task():
	""" esl connection for freeswitch"""
	con = ESL.ESLconnection(settings.FREESWITCH_IP_ADDRESS, '8021', 'ClueCon')
	while True:
		if con.connected():
			try:
				con.events('json','all')
				e = con.recvEvent()
				if e:
					event= json.loads(e.serialize("json"))
					if (event.get('Event-Name', 'UNKNOWN').upper() == 'CUSTOM'):
						signal = event.get('Event-Subclass', 'UNKNOWN')
					else:
						signal = event.get('Event-Name', 'UNKNOWN')
					try:
						sender = uuid.UUID(event.get('Core-UUID', None))
					except TypeError:
						sender = louie.sender.Anonymous
					louie.send(signal=signal.upper(), sender=sender, **event)
			except Exception as e:
				print(e)
				pass
		else:
			print("esl is not connected to freeswitch, Kindly check freeswitch status")
			time.sleep(2)
			con = ESL.ESLconnection(settings.FREESWITCH_IP_ADDRESS, '8021', 'ClueCon')

from scripts import fsevents
from scripts import fsagentlive
from scripts import custevents
from scripts import inbound_channel
if __name__ == "__main__":
	run_task()