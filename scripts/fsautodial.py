#import time
import sys,os
# import the logging library
import logging
import math
import socket
import time
import pycurl
from io import BytesIO
import uuid
from concurrent.futures import ThreadPoolExecutor
import xmlrpc.client
from string import Template
from django.conf import settings
from scripts.contacts import autodial_num_update,autodial_num_fetch
from callcenter.models import DNC,CallDetail,Switch
from crm.models import TempContactInfo, Contact
import pickle
from datetime import datetime,timedelta
from callcenter.utility import get_all_keys_data, trunk_channels_count, set_campaign_channel
from django.db import connections
from django.db import transaction

AGENTS={}
wfh_agents={}
pool = ThreadPoolExecutor(max_workers=20)

# Get an instance of a logger
logger = logging.getLogger(__name__)

def freeswicth_server(switch):
	"""
	This function is defined for creating the freeswitch server connection.
	"""
	rpc_port = Switch.objects.filter(ip_address=switch).first().rpc_port
	SERVER = xmlrpc.client.ServerProxy("http://%s:%s@%s:%s" % (settings.RPC_USERNAME,
			 settings.RPC_PASSWORD,switch,rpc_port))
	return SERVER

def scrub(number):
	""" scrub method to find the NDNC contact through curl """
	try:
		curlout = BytesIO()
		curl = pycurl.Curl()
		curl.setopt(pycurl.URL, settings.NDNC_URL % str(number)[-10:])
		curl.setopt(pycurl.WRITEFUNCTION, curlout.write)
		curl.perform()
		if curlout.getvalue().decode('UTF-8') == '1':
			return True
		if curlout.getvalue().decode('UTF-8') == '0':
			return False
		else:
			print("Problem in fetching data")
			return False
	except Exception as e:
		print(e)
		return False

def fs_voice_blaster(campaign):
	"""
	Takes campaign as an argument and read freeswitch callcenter
	configuration and then sets dial ratio accordingly. It also
	fetches numbers to dial and update them into database.
	"""
	fs_cust_in_campaign = 0
	fs_cust_in_pd_camapaign = 0
	ftdm_down_count = 0
	initiated_call = 0
	count = 0
	initiated_call = 0
	free_channel = 0
	try:
		if campaign.schedule and campaign.schedule.status == 'Active':
			camp_schedule=campaign.schedule.schedule
			day_now = datetime.today().strftime('%A')
			if day_now in camp_schedule and camp_schedule.get(day_now)['start_time'] != "" and camp_schedule.get(day_now)['stop_time'] != "":
				start_time_obj = datetime.strptime(camp_schedule.get(day_now
					)['start_time'], '%I:%M %p').time()
				stop_time_obj = datetime.strptime(camp_schedule.get(day_now
					)['stop_time'], '%I:%M %p').time()
				if datetime.now().time() > start_time_obj and  datetime.now().time() < stop_time_obj:
					ftdm_down_count , trunkwise_status, trunk_list, allowted_channels,country_code = trunk_channels_count(campaign)
					if trunk_list:
						vb_campaigns = settings.R_SERVER.hget("ad_campaign_status",campaign.name)
						if not vb_campaigns or vb_campaigns.decode('utf-8') == 'True':
							settings.R_SERVER.hset("ad_campaign_status",campaign.name, False)
							try:
								SERVER = freeswicth_server(campaign.switch.ip_address)
								# fs_cust_in_campaign =  trunk_status['chennals'][campaign.name]['c_total_chennals']
								# allowted_channels = campaign.trunk.channel_count
								# ftdm_down_count = allowted_channels - total_cust_in_campaign
								free_channel = allowted_channels - ftdm_down_count	
								camp_settings = campaign.campaign_variable
								camp_vbcampaign = campaign.vbcampaign.first()
							except socket.error as e:
								print("RPC Error %s: Freeswitch RPC module may not be" \
										  " loaded or properly configured" % (e))
								print("FreeTDM Module may not be loaded")
								settings.R_SERVER.hset("ad_campaign_status",campaign.name, True)
								return None
							except:
								free_channel = 0
								print("FreeTDM Module may not be loaded")
								try:
									if campaign.trunk.dial_string.startswith('freetdm'):
										SERVER.freeswitch.api("load", "mod_freetdm")
								except socket.error as e:
									print("RPC Error %s: Freeswitch RPC module may not be" \
										  " loaded or properly configured" %(e))

							print("Campaign:%s || Ratio:%s || Channel:%s || Used:%s || Free:%s " \
												% ( campaign.name,camp_settings.dial_ratio,
												allowted_channels,ftdm_down_count,free_channel,
											)
									)
							numbers = autodial_num_fetch(campaign, free_channel, True)
							ndnc_numbers = []
							not_ndnc = []
							if int(camp_vbcampaign.vb_data['vb_call_after']) != 0:
								max_last_call_date = datetime.now().date() - timedelta(days=int(camp_vbcampaign.vb_data['vb_call_after']))
								last_call = CallDetail.objects.filter(created__date__gte=max_last_call_date, campaign=campaign, dialed_status__in=['Full Audio Played','Not Played Full Audio'])
							else:
								last_call = CallDetail.objects.none()
							for num in numbers:
								if country_code:
									cn_numeric = country_code + num.numeric
								else:
									cn_numeric = num.numeric
								if last_call.filter(customer_cid=num.numeric).exists():
									Contact.objects.filter(id=num.contact_id).update(status="Dialed")
									TempContactInfo.objects.get(id=num.id).delete()
									continue
								if camp_settings.ndnc_scrub:
									response = scrub(num.numeric[-10:])
									if response:
										ndnc_numbers.append(num.contact_id)
										continue
								logger.debug("Call Processing: %s" % cn_numeric)
								ori_uuid = uuid.uuid4()
								try:
									initiated_call, trunkwise_status, trunk, caller_id = set_campaign_channel(trunk_list, trunkwise_status, initiated_call)
									phonebook_name = None
									if num.phonebook:
										phonebook_name = num.phonebook.name
									fs_originate = Template(settings.FS_ORIGINATE).safe_substitute(
										dict(campaign_slug=campaign.slug,
											 phonebook_id=phonebook_name,contact_id=num.id,
											 variables="uniqueid='%s',origination_uuid=%s,origination_caller_id_number=%s,trunk_id=%s,cc_customer=%s,usertype='client',call_mode='voice-blaster',disposition='Invalid Number',voice_blaster=True,"\
													   "details=%s".rstrip().rstrip(',') % (num.uniqueid,ori_uuid,caller_id,trunk['id'],str(num),camp_settings.variables),
														campaign_extension=camp_settings.extension,dial_string=trunk['dial_string']))
									fs_originate_str = Template(fs_originate).safe_substitute(
										dict(destination_number=cn_numeric))
									logger.debug("Call Initiating: %s || TeleEngine: %s" % (cn_numeric,campaign.switch.ip_address))
									SERVER.freeswitch.api("bgapi", fs_originate_str)
									logger.debug("Call Initiated: %s" % cn_numeric)

									not_ndnc.append(num.contact_id)
									# settings.R_SERVER.sadd(campaign_str, ori_uuid)
									if camp_vbcampaign.vb_mode == 1:
										pass
									time.sleep(1/camp_settings.dial_ratio)
								except socket.error as e:
									logger.debug("Call Failed: %s || Reason: SocketFail --%s" % (cn_numeric,e))
									settings.R_SERVER.hset("ad_campaign_status",campaign.name, True)
									return None
								except Exception as e:
									logger.debug("Call Failed: %s || Reason: Unknown --%s" % (cn_numeric,e))
									exc_type, exc_obj, exc_tb = sys.exc_info()
									fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
									print(exc_type, fname, exc_tb.tb_lineno)
							if numbers:
								# not_ndnc = [x.id for x in numbers]
								pool.submit(autodial_num_update,campaign,not_ndnc)
								if ndnc_numbers != []:
									pool.submit(autodial_num_update, campaign, ndnc_numbers, description="NDNC")
							settings.R_SERVER.hset("ad_campaign_status",campaign.name, True)
	except Exception as e:
		print("campaign object error",e)
		# settings.R_SERVER.hset("ad_campaign_status",campaign.name, True)
		settings.R_SERVER.hset("ad_campaign_status",campaign.name, True)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	finally:
		transaction.commit()
		connections["crm"].close()
		connections["default"].close()

def fsdial(campaign):
	"""
	Takes campaign as an argument and read freeswitch callcenter
	configuration and then sets dial ratio accordingly. It also
	fetches numbers to dial and update them into database.
	"""
	fs_cust_in_campaign = 0
	fs_cust_in_pd_camapaign = 0
	ftdm_down_count = 0
	count = 0
	free_channel = 0
	trunkwise_status = {}
	trunk_list = []
	allowted_channels = 0
	initiated_call = 0
	try:
		# Retrieve Total Used channel count, trunk status, list, max channel, country code
		ftdm_down_count , trunkwise_status, trunk_list, allowted_channels, country_code = trunk_channels_count(campaign)
		camp_settings = campaign.campaign_variable
		# If trunk_list exists then go further else skip autodial
		if trunk_list:
			pd_campaigns = settings.R_SERVER.hget("ad_campaign_status",campaign.name) # Get Campaign Status from Redis
			if not pd_campaigns or pd_campaigns.decode('utf-8') == 'True': #If Campaign doesn't exist in redis or value is true then execute
				settings.R_SERVER.hset("ad_campaign_status",campaign.name, False) # Immediately make it false on redis server
				try:
					#trunk_status = pickle.loads(settings.R_SERVER.get("trunk_status") or pickle.dumps({})) # Need to check whether used or not
					SERVER = freeswicth_server(campaign.switch.ip_address) #Get XML RPC based URL for freeswitch through campaign switch ip

					#Retrieving Available agent from Freeswitch server for the campaign
					fs_agent_available1 = SERVER.freeswitch.api("callcenter_config",
																"queue list agents '%s' 'Available (On Demand)'" % campaign.slug)
					fs_agent_available2 = SERVER.freeswitch.api("callcenter_config",
																"queue list agents '%s' 'Available'" % campaign.slug)
					# allowted_channels = campaign.trunk.channel_count
					free_channel = allowted_channels - ftdm_down_count
				except socket.error as e:
					print("RPC Error %s: Freeswitch RPC module may not be" \
							  " loaded or properly configured" % (e))
					settings.R_SERVER.hset("ad_campaign_status",campaign.name, True)
					return None
				except Exception as e:
					ftdm_down_count = 0
					exc_type, exc_obj, exc_tb = sys.exc_info()
					fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					print(exc_type, fname, exc_tb.tb_lineno)
					print("FreeTDM Module may not be loaded")
					try:
						for trunk_obj in trunk_list:
							if trunk_obj['dial_string'].startswith('freetdm'):
								SERVER.freeswitch.api("load", "mod_freetdm")
					except socket.error as e:
						print("RPC Error %s: Freeswitch RPC module may not be" \
							  " loaded or properly configured" %(e))

				agent_available = fs_agent_available1.splitlines()
				agent_available[1:1] = fs_agent_available2.splitlines()[1:-1]

				##Calculate Waiting users on campaign from Freeswitch Engine
				agent_count = 0
				for i in agent_available[1:]:
					if i.find('Waiting') > 0:
						agent_count += 1

				# Number of Call supposed to dial as per ratio
				wait_count = int(math.ceil(agent_count * camp_settings.dial_ratio))

				#Getting count of Predictive Mode Users who are all not in Idle Mode.
				total_pd_agents = 0
				AGENTS = get_all_keys_data()
				for i in AGENTS:
					if AGENTS[i]['call_type'] in ['predictive','blended'] and AGENTS[i]['state'] not in ['Idle']:
						if AGENTS[i]['campaign'] == campaign.name:
							total_pd_agents += 1

				#Number of Call supposed to dialed as per InCall Users with ratio calculation.
				total_dial_count = int(math.ceil(total_pd_agents * camp_settings.dial_ratio - ftdm_down_count))

				#Calculating exact number of call supposed to initiate as new call
				if total_dial_count < 0:
					if free_channel >= wait_count:
						count = wait_count
					else:
						count = free_channel
				elif wait_count > total_dial_count:
					if free_channel >= wait_count:
						count = wait_count
					else:
						count = free_channel
				elif wait_count <= total_dial_count:
					if free_channel >= wait_count:
						count = wait_count
					else:
						count = free_channel
				else:
					pass

				count = int(math.floor(abs(count)))

				if count < 0:
					count = 0

				#print("%s campaign | dial_ratio : %s | agents_wait : %s | \
				#	Diled_numbers : %s | next_dial_count : %s" % (campaign.name,campaign.campaign_variable.dial_ratio,agent_count,fs_cust_in_pd_camapaign,count))
				print("Campaign:%s || Ratio:%s || Channel:%s || Used:%s || Free:%s || Wait:%s || InCall:%s || Queue: %s" \
										% ( campaign.name,camp_settings.dial_ratio,
												allowted_channels,ftdm_down_count,free_channel,
												agent_count,total_pd_agents,count
											)
									)
				# Retrieving the number of records from DB.
				numbers = autodial_num_fetch(campaign, count,False)

				ndnc_numbers = []
				not_ndnc = []
				for num in numbers:

					if country_code:
						cn_numeric = country_code + num.numeric
					else:
						cn_numeric = num.numeric

					logger.debug("Call Processing: %s" % cn_numeric)

					# Checking NDNC Scrubbing Solution
					if camp_settings.ndnc_scrub: # Checking whether NDNC Scrubbing Enabled or not
						response = scrub(num.numeric[-10:])
						if response:
							ndnc_numbers.append(num.contact_id)
							logger.debug("Call Skipping: %s || Reason: NDNC" % cn_numeric)
							continue

					# Checking System DNC and Campaign DNC
					if DNC.objects.filter(numeric=num.numeric[-10:],status='Active',global_dnc=True).exists():
						Contact.objects.filter(numeric=num.numeric).update(status = 'Dnc')
						TempContactInfo.objects.filter(numeric=num.numeric).delete()
						logger.debug("Call Skipping: %s || Reason: GlobalDNC" % cn_numeric)
						continue

					elif DNC.objects.filter(numeric=num.numeric[-10:],status='Active',campaign=campaign).exists():
						Contact.objects.filter(numeric = num.numeric).update(status = 'Dnc')
						TempContactInfo.objects.filter(numeric = num.numeric).delete()
						logger.debug("Call Skipping: %s || Reason: CampaignDNC" % cn_numeric)
						continue

					else: # Ready to Dial Number
						ori_uuid = uuid.uuid4()
						try:

							initiated_call, trunkwise_status, trunk, caller_id = set_campaign_channel(trunk_list, trunkwise_status, initiated_call)

							if 'id' in trunk and trunk['id']:

								phonebook_name = None
								if num.phonebook:
									phonebook_name = num.phonebook.name

								fs_originate = Template(settings.FS_ORIGINATE).safe_substitute(
									dict(campaign_slug=campaign.slug,
										 phonebook_id=phonebook_name,contact_id=num.contact_id,
										 variables="uniqueid='%s',origination_uuid=%s,voice_blaster=False,origination_caller_id_number=%s,trunk_id=%s,cc_customer=%s,usertype='client',call_mode='predictive',disposition='Invalid Number'," \
												   "details=%s".rstrip().rstrip(',') % (num.uniqueid,ori_uuid,caller_id,trunk['id'],str(num),camp_settings.variables),
													campaign_extension=camp_settings.extension,dial_string=trunk['dial_string']))
								fs_originate_str = Template(fs_originate).safe_substitute(
									dict(destination_number=cn_numeric))

								logger.debug("Call Initiating: %s || TeleEngine: %s" % (cn_numeric,campaign.switch.ip_address))
								SERVER.freeswitch.api("bgapi", fs_originate_str)
								logger.debug("Call Initiated: %s " % cn_numeric)

								# settings.R_SERVER.sadd(campaign_str, ori_uuid)
								not_ndnc.append(num.contact_id)

								#Check whether WFH Campaign or not.
								if campaign.wfh:
									contact_obj = Contact.objects.get(id=num.id)
									wfh_agents = pickle.loads(settings.R_SERVER.get("wfh_agents") or pickle.dumps({}))
									if wfh_agents:
										wfh_agents[str(ori_uuid)]={"c_num":contact_obj.numeric,'c_username':contact_obj.first_name +''+contact_obj.last_name}
									else:
										wfh_agents={str(ori_uuid):{"c_num":contact_obj.numeric,'c_username':contact_obj.first_name +''+contact_obj.last_name}}
									settings.R_SERVER.set("wfh_agents",pickle.dumps(wfh_agents))


							else:
								logger.debug("Call Failed: %s || Reason: TrunkUnavailable" % cn_numeric)
								settings.R_SERVER.hset("ad_campaign_status",campaign.name, True)
						except socket.error as e:
							logger.debug("Call Failed: %s || Reason: SocketFail --%s" % (cn_numeric,e))
							settings.R_SERVER.hset("ad_campaign_status",campaign.name, True)
							return None
						except Exception as e:
							logger.debug("Call Failed: %s || Reason: Unknown --%s" % (cn_numeric,e))
				if numbers:
					# not_ndnc = [x.id for x in numbers]
					pool.submit(autodial_num_update,campaign,not_ndnc)
					if ndnc_numbers != []:
						pool.submit(autodial_num_update, campaign, ndnc_numbers, description="NDNC")
				settings.R_SERVER.hset("ad_campaign_status",campaign.name, True)

	except Exception as e:
		logger.debug("Unable to Retrieve Campaign Information")
		settings.R_SERVER.hset("ad_campaign_status",campaign.name, True)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	finally:
		transaction.commit()
		connections["crm"].close()
		connections["default"].close()