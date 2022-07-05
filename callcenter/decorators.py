from django.http import JsonResponse, HttpResponseRedirect
from django.urls import resolve
from django.urls import reverse

from rest_framework.response import Response
from django.conf import settings
from .utility import get_object,get_all_keys_data
from .models import (User, UserVariable, Group, Campaign,
	Disposition, PauseBreak, CampaignSchedule, Script, AudioFile, RelationTag,
	UserRole, Switch, DialTrunk, CampaignVariable, CSS,SkilledRouting,ThirdPartyApi,
	VoiceBlaster,Holidays,ThirdPartyApiUserToken)
import pickle

def user_validation(function):
	"""
	This validation is used to do validation of
	user is already exist or not with same detail
	"""
	def wrap(request, *args, **kwargs):
		caller_id = camp_callerid = []
		pk = kwargs.get("pk", "")
		name = User.objects.filter(username__iexact=request.POST["username"])
		email = request.POST.get("email", "")
		caller_id = request.POST.get("caller_id", "")
		# extension = request.POST.get("extension", "")
		wfh_numeric = request.POST.get("wfh_numeric","")
		camp_callerid = CampaignVariable.objects.none()
		user_caller_id = User.objects.none()
		password = User.objects.filter(password=request.POST.get("password", ""))
		if caller_id:
			user_caller_id = User.objects.filter(caller_id=request.POST["caller_id"])
		if caller_id:
			camp_callerid = CampaignVariable.objects.filter(caller_id=caller_id)
		if wfh_numeric:
			wfh_numeric = UserVariable.objects.filter(wfh_numeric=wfh_numeric)
		if pk:
			user = get_object(kwargs["pk"], "callcenter", "User")
			user_variable = UserVariable.objects.get(user_id=pk)
			name = name.exclude(username=user.username)
			if user_caller_id:
				user_caller_id = user_caller_id.exclude(username=user.username)
			if camp_callerid:
				camp_callerid = camp_callerid.exclude(extension=user.extension)
			if user_variable and wfh_numeric:
				wfh_numeric = wfh_numeric.exclude(wfh_numeric=user_variable.wfh_numeric)
		if name.exists():
			return JsonResponse({"username": "User with this username already exists"},
				status=500)	
		if user_caller_id.exists():
			return JsonResponse({"caller_id": "User with this caller id already exists"},
				status=500)
		if camp_callerid.exists():
			return JsonResponse({"caller_id": "This caller id is already taken"},
				status=500)
		if wfh_numeric and wfh_numeric.exists() and wfh_numeric != 'None':
			return JsonResponse({"wfh_numeric": "This wfh numeric is already taken : "+wfh_numeric.first().user.username},
				status=500)

		return function(request, *args, **kwargs)
	return wrap

def group_validation(function):
	"""
	This validation is used to do validation of
	department is already exist or not with same detail
	"""
	def wrap(request, *args, **kwargs):
		pk = kwargs.get("pk", "")
		if request.data.get("name", ""):
			if pk:
				group = Group.objects.filter(name=request.data.get("name")).exclude(
					id=pk).exists()
			else:
				group = Group.objects.filter(name=request.data.get("name")).exists()

			if group:
				return JsonResponse(
					{"name": "Group with given name already exists"},
					status=500)
		return function(request, *args, **kwargs)
	return wrap

def campaign_validation(function):
	"""
	This validation is used to do validation of
	campaign is already exist or not with same name or
	extension at the time of campaign creation
	"""
	def wrap(request, *args, **kwargs):
		disposition = request.POST.getlist('disposition','')
		dispos_val = Disposition.objects.filter(id__in=disposition).values_list('show_dispo',flat=True)
		dispo = list(set(dispos_val))
		if len(dispo) == 1:
			if dispo[0] in ['1','2']:
				if dispo[0] == '1':
					return JsonResponse({"errors": "Only Connected Disposition are Selected, Select NotConnected/Both Dispositions "},status=500)
				else:
					return JsonResponse({"errors": "Only Not-Connected Disposition are Selected, Select Connected/Both Dispositions "},status=500)
		campaign_name = request.POST.get("name", "")
		extension = request.POST.get("extension", "")
		wfh_caller_id = request.POST.get("wfh_caller_id", "")
		if Campaign.objects.filter(name__iexact=campaign_name).exists():
			return JsonResponse({"camp_name_error": "Campaign with this name already exists"},status=500)
		if wfh_caller_id:
			campvariable_obj = CampaignVariable.objects.filter(wfh_caller_id=wfh_caller_id)
			skill_obj = SkilledRouting.objects.filter(skill_id__did__contains=wfh_caller_id)
			usr_obj = User.objects.filter(caller_id=wfh_caller_id)

			if campvariable_obj.exists() and wfh_caller_id != None:
				return JsonResponse({"camp_callerid_error": "Campaign with this wfh caller id already exists at : "+campvariable_obj.first().campaign.name},
					status=500)
			if usr_obj.exists():
				print("This wfh caller id already taken"+usr_obj.first().username)
				return JsonResponse({"camp_callerid_error": "This wfh caller id already taken by :"+usr_obj.first().username},
					status=500)
			if skill_obj.exists():
				return JsonResponse({"camp_callerid_error": "This wfh caller id already taken by Skill Routing: "+skill_obj.first().name},
					status=500)
		# if caller_id:
		# 	if CampaignVariable.objects.filter(caller_id=caller_id).exists():
		# 		return JsonResponse({"camp_callerid_error": "Campaign with this caller id already exists"},
		# 			status=500)
		# 	if User.objects.filter(caller_id=caller_id).exists():
		# 		return JsonResponse({"camp_callerid_error": "This caller id already taken"},
		# 			status=500)
		return function(request, *args, **kwargs)
	return wrap

def campaign_edit_validation(function):
	"""
	This validation is used to do validation of
	campaign detail already exist or not at the time of campaign
	edit
	"""
	def wrap(request, *args, **kwargs):
		object_data = get_object(kwargs["pk"], "callcenter", "Campaign")
		disposition = request.POST.getlist('disposition','')
		dispos_val = Disposition.objects.filter(id__in=disposition).values_list('show_dispo',flat=True)
		dispo = list(set(dispos_val))
		if len(dispo) == 1:
			if dispo[0] in ['1','2']:
				if dispo[0] == '1':
					return JsonResponse({"errors": "Only Connected Disposition are Selected, Select NotConnected/Both Dispositions "},status=500)
				else:
					return JsonResponse({"errors": "Only Not-Connected Disposition are Selected, Select Connected/Both Dispositions "},status=500)
		campaign_name = request.POST.get("name", "")
		extension = request.POST.get("extension", "")
		wfh_caller_id = request.POST.get("wfh_caller_id", "")

		if campaign_name!=object_data.name:
			campaign_pd = pickle.loads(settings.R_SERVER.get("campaign_status") or pickle.dumps({}))
			if campaign_pd and object_data.name in campaign_pd and len(campaign_pd[object_data.name])>0:
				return JsonResponse({"camp_name_error": "Oops you cannot change campaign name because agents is login with this campaign in dialer"},status=500)

		if Campaign.objects.filter(name__iexact=campaign_name).exclude(
			id=object_data.id).exists():
			return JsonResponse({"camp_name_error": "Campaign with this name already exists"},
				status=500)
		if wfh_caller_id:
			campvariable_obj = CampaignVariable.objects.filter(wfh_caller_id=wfh_caller_id)
			usr_obj = User.objects.filter(caller_id=wfh_caller_id)
			skill_obj = SkilledRouting.objects.filter(skill_id__did__contains=wfh_caller_id)
			if campvariable_obj.exclude(campaign_id=object_data.id).exists() and wfh_caller_id != None:
				return JsonResponse({"camp_callerid_error": "Campaign with this wfh caller id already exists at : "+campvariable_obj.first().campaign.name},
					status=500)

			if usr_obj.exists():
				return JsonResponse({"camp_callerid_error": "This wfh caller id already taken by : "+usr_obj.first().username},
					status=500)
			if skill_obj.exists():
				return JsonResponse({"camp_callerid_error": "This wfh caller id already taken by Skill Routing: "+skill_obj.first().name},
					status=500)
		return function(request, *args, **kwargs)
	return wrap

def skill_validation(function):
	"""
	This validation is used to do validation of
	skill name is already exist or not with same name or
	skill id at the time of campaign creation
	"""
	def wrap(request, *args, **kwargs):
		skill_name = request.POST.get('name', '')
		skill_id = request.POST.get('skill_id','')
		if SkilledRouting.objects.filter(name__iexact=skill_name).exists():
			return JsonResponse({"errors":"Skill with this name already exists"}, status=500)
		return function(request, *args, **kwargs)
	return wrap

def skill_edit_validation(function):
	"""
	This validation is used to do validation of
	skill name is already exist or not with same name or
	skill id at the time of campaign creation
	"""
	def wrap(request, *args, **kwargs):
		data_obj = get_object(kwargs["pk"], "callcenter", "SkilledRouting")
		skill_name = request.POST.get('name', '')
		if SkilledRouting.objects.filter(name__iexact=skill_name).exclude(id=data_obj.id).exists():
			return JsonResponse({"errors":"Skill with this name already exists"}, status=500)
		return function(request, *args, **kwargs)
	return wrap

def phone_validation(function):
	"""
	This validation is used to do validation of
	campaign detail already exist or not at the time of campaign
	edit
	"""
	def wrap(request, *args, **kwargs):
		if UserVariable.objects.filter(extension=request.POST["extension"]).exclude(
			id=user_variable.id).exists():
			return JsonResponse({"errors": "Phone with this extension already exists"}, status=500)
		return function(request, *args, **kwargs)
	return wrap

def dispo_validation(function):
	"""
	This validation is used to do validation of
	campaign detail already exist or not at the time of campaign
	edit
	"""
	def wrap(request, *args, **kwargs):
		pk = kwargs.get("pk", "")
		if request.POST.get("name", ""):
			if pk:
				dispo = Disposition.objects.filter(
				name__iexact=request.POST["name"]).exclude(id=pk).exclude(status="Delete").exists()
			else:	
				dispo = Disposition.objects.filter(
					name__iexact=request.POST["name"]).exclude(status="Delete").exists()
			if dispo:
				return JsonResponse(
					{"name": "Disposition with given name already exists"},
					status=409)
			if request.POST.get("name","").lower() in ['nc','invalid number', 'abandonedcall', 'drop']:
				return JsonResponse({
					'name':'Disposition with the given name cannot be used'
					},status=500)

		return function(request, *args, **kwargs)
	return wrap

def relationtag_validation(function):
	"""
	This validation is used to do validation of
	relationtag already exist or not at the time of relationtag
	edit or create
	"""
	def wrap(request, *args, **kwargs):
		pk = kwargs.get("pk", "")
		if request.POST.get("name", ""):
			if pk:
				relationtag = RelationTag.objects.filter(
				name__iexact=request.POST["name"]).exclude(id=pk).exists()
			else:	
				relationtag = RelationTag.objects.filter(
					name__iexact=request.POST["name"]).exists()
			if relationtag:
				return JsonResponse(
					{"name": "RelationTag with given name already exists"},
					status=409)

		return function(request, *args, **kwargs)
	return wrap

def pausebreak_validation(function):
	"""
	This validation is used to do validate pause break
	is already exist or not at the time of creation
	"""
	def wrap(request, *args, **kwargs):
		pk = kwargs.get("pk", "")
		if request.POST.get("name", ""):
			if pk:
				pausebreak = PauseBreak.objects.filter(
				name__icontains=request.POST["name"]).exclude(id=pk).exists()
			else:	
				pausebreak = PauseBreak.objects.filter(
					name__icontains=request.POST["name"]).exists()
			if pausebreak:
				return JsonResponse(
					{"name": "PauseBreak with given name already exists"},
					status=500)
		return function(request, *args, **kwargs)
	return wrap

def call_time_validation(function):
	"""
	This validation is used to do validate call time
	is already exist or not at the time of creation
	"""
	def wrap(request, *args, **kwargs):
		pk = kwargs.get("pk", "")
		if request.POST.get("name", ""):
			if pk:
				call_time = CampaignSchedule.objects.filter(
				name__iexact=request.POST["name"]).exclude(id=pk).exists()
			else:	
				call_time = CampaignSchedule.objects.filter(
					name__iexact=request.POST["name"]).exists()
			if call_time:
				return JsonResponse(
					{"name": "Call Time with given name already exists"},
					status=500)
		return function(request, *args, **kwargs)
	return wrap

def script_validation(function):
	"""
	This validation is used to do validate script
	is already exist or not at the time of creation
	"""
	def wrap(request, *args, **kwargs):
		pk = request.POST.get("script_id", "")
		if request.POST.get("name", ""):
			if pk:
				script = Script.objects.filter(
				name__iexact=request.POST["name"]).exclude(id=pk).exists()
			else:	
				script = Script.objects.filter(
					name__iexact=request.POST["name"]).exists()
			if script:
				return JsonResponse(
					{"name": "Script with given name already exists"},
					status=500)
		return function(request, *args, **kwargs)
	return wrap


def audio_file_validation(function):
	"""
	This validation is used to do validate audio
	is already exist or not at the time of creation
	"""
	def wrap(request, *args, **kwargs):
		pk = kwargs.get("pk", "")
		if request.POST.get("name", ""):
			if pk:
				audio = AudioFile.objects.filter(
				name__iexact=request.POST["name"]).exclude(id=pk).exists()
			else:	
				audio = AudioFile.objects.filter(
					name__iexact=request.POST["name"]).exists()
			if audio:
				return JsonResponse(
					{"name": "Audio with given name already exists"},
					status=500)
		return function(request, *args, **kwargs)
	return wrap

def user_role_validation(function):
	"""
	This validation is used to do validate use role
	is already exist or not at the time of creation
	"""
	def wrap(request, *args, **kwargs):
		pk = kwargs.get("pk", "")
		if request.POST.get("name", ""):
			if pk:
				user_role = UserRole.objects.filter(
				name__iexact=request.POST["name"]).exclude(id=pk).exists()
			else:	
				user_role = UserRole.objects.filter(
					name__iexact=request.POST["name"]).exists()
			if user_role:
				return JsonResponse(
					{"name": "Given role is already exists"},
					status=500)
		return function(request, *args, **kwargs)
	return wrap

def switch_validation(function):
	"""
	This validation is used to do validate switch
	is already exist or not at the time of creation
	"""
	def wrap(request, *args, **kwargs):
		pk = kwargs.get("pk", "")
		name = Switch.objects.filter(name__icontains=request.POST["name"])
		ip_address = Switch.objects.filter(ip_address=request.POST["ip_address"])
		if pk:
			switch = get_object(pk, "callcenter", "Switch")
			name = name.exclude(name=switch.name)
			ip_address = ip_address.exclude(ip_address=switch.ip_address)
		if name.exists():
			return JsonResponse({"name": "Switch with this name already exists"},
				status=500)
		if ip_address.exists():
			return JsonResponse({"ip_address": "Switch with this IP already exists"},
				status=500)		
		return function(request, *args, **kwargs)
	return wrap

def trunk_validation(function):
	"""
	This validation is used to do validate trunk
	is already exist or not at the time of creation
	"""
	def wrap(request, *args, **kwargs):
		pk = kwargs.get("pk", "")
		if request.POST.get("name", ""):
			if pk:
				dial_trunk = DialTrunk.objects.filter(
				name__iexact=request.POST["name"]).exclude(id=pk).exists()
			else:	
				dial_trunk = DialTrunk.objects.filter(
					name__iexact=request.POST["name"]).exists()
			if dial_trunk:
				return JsonResponse(
					{"name": "Given name is already exists"},
					status=500)
		return function(request, *args, **kwargs)
	return wrap

def check_read_permission(function):
	"""
	This method is used to check the read permission for the pages
	"""
	def wrap(request, *args, **kwargs):
		permission_dict = {'can_read':False, 'can_create':False,
		'can_update':False, 'can_delete':False, 'can_switch':False, 'can_boot':False}
		current_url = resolve(request.path_info).url_name
		module = current_url.split('-')[-1]
		if request.user.is_superuser == False:
			permissions = request.session.get('permissions')
			if 'R' not in permissions['dashboard']:
				return HttpResponseRedirect(reverse('agent'))
			elif 'R' not in permissions[module]:
				return Response({"error": "You are Not Authorized"})
			else:
				if 'R' in permissions[module]:
					permission_dict['can_read'] = True
				if 'C' in permissions[module]:
					permission_dict['can_create'] = True
				if 'U' in permissions[module]:
					permission_dict['can_update'] = True
				if 'D' in permissions[module]:
					permission_dict['can_delete'] = True
				if 'R' in permissions['switchscreen']:
					permission_dict['can_switch'] = True
				if 'R' in permissions['system_boot_action']:
					permission_dict['can_boot'] = True
		else:
			permission_dict = {'can_read':True, 'can_create':True,
			'can_update':True, 'can_delete':True, 'can_switch':True, 'can_boot':True}
		kwargs['permissions'] = permission_dict
		return function(request, *args, **kwargs)
	return wrap

def check_create_permission(function):
	"""
	This method is used to check the create permission for page
	"""
	def wrap(request, *args, **kwargs):
		permission_dict = {'can_create':False, 'can_switch':False, 'can_boot':False}
		current_url = resolve(request.path_info).url_name
		module = current_url.split('-')[-1]
		if request.user.is_superuser == False:
			permissions = request.session.get('permissions')
			if 'R' not in permissions['dashboard']:
				return HttpResponseRedirect(reverse('agent'))
			elif 'C' not in permissions[module]:
				return Response({"error": "You are Not Authorized"})
			else:
				if 'C' in permissions[module]:
					permission_dict['can_create'] = True
				if 'R' in permissions['switchscreen']:
					permission_dict['can_switch'] = True
				if 'R' in permissions['system_boot_action']:
					permission_dict['can_boot'] = True
		else:
			permission_dict = {'can_create':True, 'can_switch':True, 'can_boot':True}
		kwargs['permissions'] = permission_dict
		return function(request, *args, **kwargs)
	return wrap

def check_update_permission(function):
	"""
	This method is used to check the update permission for a page
	"""
	def wrap(request, *args, **kwargs):
		permission_dict = {'can_update':False, 'can_switch':False, 'can_boot':False}
		current_url = resolve(request.path_info).url_name
		module = current_url.split('-')[-1]
		if request.user.is_superuser == False:
			permissions = request.session.get('permissions')
			if 'R' not in permissions['dashboard']:
				return HttpResponseRedirect(reverse('agent'))
			elif 'U' not in permissions[module]:
				return Response({"error": "You are Not Authorized"})
			else:
				if 'U' in permissions[module]:
					permission_dict['can_update'] = True
				if 'R' in permissions['switchscreen']:
					permission_dict['can_switch'] = True
				if 'R' in permissions['system_boot_action']:
					permission_dict['can_boot'] = True
		else:
			permission_dict = {'can_update':True, 'can_switch':True, 'can_boot':True}
		kwargs['permissions'] = permission_dict
		return function(request, *args, **kwargs)
	return wrap

def thirdparty_validation(function):
	"""
	This method is used to check the thirdparty crm
	validation with the name and api of the crm 
	"""
	def wrap(request,*args,**kwargs):
		name = request.POST.get('name',"")
		campaign = request.POST.get('campaign',"")
		if name:
			if ThirdPartyApi.objects.filter(name__iexact=name).exists():
				return JsonResponse({"name":"ThirdPartyApi with this name already exists"}, status=500)
			if ThirdPartyApi.objects.filter(campaign__id=campaign).exists():
				return JsonResponse({"campaign":"ThirdPartyApi with this Campaign already assigned"}, status=500)
		return function(request, *args, **kwargs)
	return wrap

def thirdparty_edit_validation(function):
	"""
	This method is used to check the thirdpart edit 
	validation with the name and api of the crm 
	"""
	def wrap(request,*args,**kwargs):
		data_obj = get_object(kwargs["pk"], "callcenter", "ThirdPartyApi")
		name = request.POST.get('name',"")
		campaign = request.POST.get('campaign',"")
		if name:
			if ThirdPartyApi.objects.filter(name__iexact=name).exclude(id=data_obj.id).exists():
				return JsonResponse({"name":"ThirdPartyApi with this name already exists"}, status=500)
			if ThirdPartyApi.objects.filter(campaign__id=campaign).exclude(id=data_obj.id).exists():
				return JsonResponse({"campaign":"ThirdPartyApi with this Campaign already assigned"}, status=500)
		return function(request, *args, **kwargs)
	return wrap



def voiceblaster_validation(function):
	"""
	This method is used to check the voiceblater
	validation with the name and campaign 
	"""
	def wrap(request,*args,**kwargs):
		name = request.POST.get('name',"")
		campaign = request.POST.get('campaign',"")
		if name:
			if VoiceBlaster.objects.filter(name__iexact=name).exists():
				return JsonResponse({"name":"VoiceBlaster with this name already exists"}, status=500)
			if VoiceBlaster.objects.filter(campaign__id=campaign).exists():
				return JsonResponse({"campaign":"VoiceBlaster with this Campaign already assigned"}, status=500)
		return function(request, *args, **kwargs)
	return wrap

def voiceblaster_edit_validation(function):
	"""
	This method is used to check the voiceblater edit
	validation with the name and campaign 
	"""
	def wrap(request,*args,**kwargs):
		data_obj = get_object(kwargs["pk"], "callcenter", "VoiceBlaster")
		name = request.POST.get('name',"")
		campaign = request.POST.get('campaign',"")
		if name:
			if VoiceBlaster.objects.filter(name__iexact=name).exclude(id=data_obj.id).exists():
				return JsonResponse({"name":"VoiceBlaster with this name already exists"}, status=500)
			if VoiceBlaster.objects.filter(campaign__id=campaign).exclude(id=data_obj.id).exists():
				return JsonResponse({"campaign":"VoiceBlaster with this Campaign already assigned"}, status=500)
		return function(request, *args, **kwargs)
	return wrap

def holiday_validation(function):

	def wrap(request,*args,**kwargs):
		name = request.POST.get('name',"")
		holiday_date = request.POST.get("holiday_date","")
		if "pk" in kwargs:
			data_obj = get_object(kwargs["pk"], "callcenter", "Holidays")
			if Holidays.objects.filter(name__iexact=name).exclude(id=data_obj.id).exists():
				return JsonResponse({"name":"Holiday with this name already exists"})
			if Holidays.objects.filter(holiday_date=holiday_date).exclude(id=data_obj.id).exists():
				return JsonResponse({"holiday_date":"Holiday with this date already exists"})
		else:
			if Holidays.objects.filter(name__iexact=name).exists():
				return JsonResponse({"name":"Holiday with this name already exists"})
			if Holidays.objects.filter(holiday_date=holiday_date).exists():
				return JsonResponse({"holiday_date":"Holiday with this date already exists"})
		return function(request,*args,**kwargs)
	return wrap


def edit_third_party_token(function):
	def wrap(request,*args,**kwargs):
		user_id = request.POST.get('user')
		mobile = request.POST.get("mobile_no")
		data_obj = get_object(kwargs["pk"], "callcenter", "ThirdPartyApiUserToken")
		user = User.objects.get(id=user_id)
		if ThirdPartyApiUserToken.objects.filter(user=user).exclude(id=data_obj.id).exists():
			return JsonResponse({"name":"User is already created "})
		if ThirdPartyApiUserToken.objects.filter(mobile_no=mobile).exclude(id=data_obj.id).exists():
			return JsonResponse({"mobile_no":"Mobile Number is already Taken "})
		return function(request,*args,**kwargs)
	return wrap