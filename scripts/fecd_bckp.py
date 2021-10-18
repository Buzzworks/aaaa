"""
FreeSWITCH Event Collection Daemon.
This daemon collects ZMQ events from FreeSWITCH and
sends them to interested subscribers.
"""
import louie
import uuid
import zmq
def run_task(host='127.0.0.1', port=5556):
	try:
		context = zmq.Context()
		socket = context.socket(zmq.SUB)
		socket.connect('tcp://%s:%s' % (host, port))
		socket.setsockopt(zmq.SUBSCRIBE,b"")	
		while True:
			try:
				event = socket.recv_json()
				print(event)
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
				print(e,"Inside loop")
	except Exception as e:
		print(e,"Outside loop")
# For CDR
from scripts import fsevents
from scripts import fsagentlive  
if __name__ == "__main__":
	run_task()