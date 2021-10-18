"""
Receiving signals for events.
"""
import louie
import pickle
from django.conf  import settings
from callcenter.models import DialTrunk
from concurrent.futures import ThreadPoolExecutor
dispo_pool = ThreadPoolExecutor(max_workers=10)

def inbound_channel(signal, sender, **kwargs):
	""" 
	Inbound call channel dial str trunk count reduce and increase 
	based on the inbound calls
	"""
	dialed_string = kwargs.get('variable_channel_name',kwargs.get('Channel-Name'))
	destination_number = kwargs.get('Caller-Caller-ID-Number',kwargs.get('Caller-Orig-Caller-ID-Numberv'))
	dial_string1 = str(dialed_string).replace('internal/'+str(destination_number),'external/${destination_number}')
	dial_trunk = DialTrunk.objects.filter(dial_string=dial_string1)
	TRUNK = pickle.loads(settings.R_SERVER.get("trunk_status") or pickle.dumps({}))
	if dial_trunk.exists():
		for trunk in dial_trunk:
			if trunk.status=='Active' and str(trunk.id) in TRUNK:
				TRUNK[str(trunk.id)]  += 1
				settings.R_SERVER.set("trunk_status", pickle.dumps(TRUNK))
				break
			else:
				TRUNK[str(trunk.id)] = 1
				settings.R_SERVER.set("trunk_status", pickle.dumps(TRUNK))
				break					
for sig in ['CUSTOM::INBOUND_CALL']:
	louie.connect(inbound_channel, signal=sig)
