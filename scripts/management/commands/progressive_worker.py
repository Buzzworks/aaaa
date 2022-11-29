import json
import sys
from django.core.management.base import BaseCommand
from django.conf import settings 
import os
from crm.models import TempContactInfo
import pika
from django.db import transaction, connections
import datetime as dt
import time

class Command(BaseCommand):

	help = "Progressive Call Worker"
	def handle(self, **options):
		try:
			connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
			channel = connection.channel()

			channel.queue_declare(queue='task_queue', durable=True)
			print(' [*] Waiting for messages. To exit press CTRL+C')
			def callback(ch, method, properties, body):
				try:
					print(" [x] Received %r" % json.loads(body))
					temp_id = None
					data = json.loads(body)
					campaign= data['campaign']
					user = data['user']
					modified_date = dt.datetime.now()
					print("start :: user :: ",user,"camp :: ",campaign,"start ::",modified_date)
					crm_conn = connections['crm']
					with crm_conn.cursor() as cursor:
						cursor.execute(
							f'''    update crm_tempcontactinfo
									set status = 'Locked' ,modified_date = '{modified_date}',"user"='{user}'
									where id  = (select id FROM crm_tempcontactinfo
									where campaign = '{campaign}'
									and status = 'NotDialed'
									order by priority,modified_date limit 1 FOR UPDATE SKIP LOCKED)
									RETURNING id;
							''')
						temp_tup = cursor.fetchone()
						if temp_tup:
							temp_id = temp_tup[0]
						if temp_id:
							temp_contact = TempContactInfo.objects.filter(id=temp_id).first()
							print(temp_contact.id,temp_contact.numeric,temp_contact.contact)
					print("End Time :: ",dt.datetime.now())
				except Exception as e:
					print("Exception occures from Progressive Call Worker inside callback :: ",e)
					exc_type, exc_obj, exc_tb = sys.exc_info()
					fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					print(exc_type, fname, exc_tb.tb_lineno)
				finally:
					ch.basic_ack(delivery_tag=method.delivery_tag)
					transaction.commit()
					connections["crm"].close()
					connections["default"].close()
			channel.basic_qos(prefetch_count=1)
			channel.basic_consume(queue='task_queue', on_message_callback=callback)

			channel.start_consuming()
		except Exception as e:
			print("Exception occures from Progressive Call Worker outside callback :: ",e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
		finally:
			transaction.commit()
			connections["crm"].close()
			connections["default"].close()