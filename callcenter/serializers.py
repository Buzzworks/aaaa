from rest_framework import serializers
from callcenter.models import *
from flexydial.views import get_login_campaign, get_login_agent
from crm.models import Contact, ContactInfo
from datetime import timedelta
from .constants import four_digit_number, three_digits_list

class LoginSerializer(serializers.Serializer):
	""" login serializer for user """
	username = serializers.CharField(required=True, max_length=100)
	password = serializers.CharField(required=True, max_length=100)

class UserSerializer(serializers.ModelSerializer):
	""" user Serializer for showing and saving the data"""
	class Meta:
		model = User
		fields = ('username', 'email', 'password',
			'user_role', 'group', 'is_active', 'first_name',
			'last_name', 'date_of_birth', 'reporting_to',
			'user_timezone', 'caller_id','employee_id', 'email_password' ,'call_type')

class CurlSerializer(serializers.ModelSerializer):
	""" serializer for curl request to the freeswith xml file  """
	user = UserSerializer()
	call_type =  serializers.ReadOnlyField(source='get_call_type_display')
	switch = serializers.ReadOnlyField()
	class Meta:
		model = UserVariable
		fields = ('user','switch','call_type')

class UserPaginationSerializer(serializers.ModelSerializer):
	""" User pagination serializer for pagination of user"""
	extension = serializers.ReadOnlyField()
	groups = serializers.ReadOnlyField()
	role_name = serializers.ReadOnlyField()
	status = serializers.ReadOnlyField(source='active_status')
	created_by_user = serializers.ReadOnlyField()
	class Meta:
		model = User
		fields = ('username', 'id', 'extension', 'role_name', 'groups', 'created_by_user', 'status','created','updated')

class UserVariableCreateSerializer(serializers.ModelSerializer):
	""" Serializer used for uservariable create """
	class Meta:
		model = UserVariable
		fields = ('device_pass', 'level', 'position', 'domain',
			'type', 'contact', 'max_no_answer', 'wrap_up_time',
			'reject_delay_time','busy_delay_time','extension', 'dial_status')
	def validate(self,data):
		try:
			extension_exist = UserVariable.objects.all().values_list('extension', flat=True)
			latest_extension = sorted(list(set(four_digit_number) - set(extension_exist)))[0]
			data['extension']= latest_extension if data['extension']=='NEW'  else ""
			return data
		except Exception as e:
			print('exception at UserVariableCreateSerializer',e)
		

class UpdateUserSerializer(serializers.ModelSerializer):
	""" This serializer is used for updating the user details"""
	class Meta:
		model = User
		fields = ('username', 'email',
			'user_role', 'group', 'is_active', 'first_name',
			'last_name','reporting_to','call_type',
			'is_superuser', 'first_name', 'last_name', 'date_of_birth',
			'caller_id', 'user_timezone', 'employee_id', 'email_password', 'trunk')

class UserVariableSerializer(serializers.ModelSerializer):
	""" This seriliazer is used for creating the uservariable"""
	class Meta:
		model = UserVariable
		fields = ('device_pass', 'domain', 'level', 'position',
			'type', 'contact', 'max_no_answer', 'wrap_up_time',
			'reject_delay_time','busy_delay_time','extension', 'protocol','wfh_numeric','w_req_callback')
		
class CampaignSerializer(serializers.ModelSerializer):
	'''
	This serializer is for creating campaign
	'''
	class Meta:
		model = Campaign
		fields = '__all__'

class CampaignPaginationSerializer(serializers.ModelSerializer):
	'''
	This serializer is for creating campaign
	'''
	extension = serializers.ReadOnlyField()
	switch = serializers.SerializerMethodField()
	wfh_caller_id = serializers.SerializerMethodField()
	created_by_user = serializers.SerializerMethodField()
	class Meta:
		model = Campaign
		fields = ('name', 'id', 'extension', 'switch', 'created_by_user','status', 'wfh_caller_id','created_date','modified_date')

	def get_switch(self, obj):
		if obj.switch:
			return obj.switch.name
		else:
			return ""
			
	def get_wfh_caller_id(self, obj):
		if obj.id:
			wfh_caller_id = CampaignVariable.objects.get(campaign_id=obj.id).wfh_caller_id
			return wfh_caller_id if wfh_caller_id !=None else ''
		else:
			return ""

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""

class IngroupCampaignSerializer(serializers.ModelSerializer):
	""" This serializer is used for ingroup create """
	class Meta:
		model = InGroupCampaign
		fields = ('name','caller_id','strategy','status')


class InGroupCampaignPaginationSerializer(serializers.ModelSerializer):
	'''
	This serializer is for creating campaign
	'''
	created_by_user = serializers.SerializerMethodField()
	campaign_name = serializers.SerializerMethodField()
	class Meta:
		model = InGroupCampaign
		fields = ('name', 'id', 'created_by_user','status', 'campaign_name','created_date')

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""
	def get_campaign_name(self, obj):
		if obj.ingroup_campaign:
			campaign_list = list(obj.ingroup_campaign.all().values_list("campaign__name", flat=True))
			if campaign_list:
				return ', '.join(campaign_list)
		return ""

class ScriptSerializer(serializers.ModelSerializer):
	""" script Serializer is used in the creating of scripts"""
	class Meta:
		model = Script
		fields = ('name','campaign','text', 'status')

class ScriptPaginationSerializer(serializers.ModelSerializer):
	""" Script pagination serializer for pagination of Script"""
	created_by_user = serializers.SerializerMethodField()
	class Meta:
		model = Script
		fields = ('name','id','created_by_user', 'status','created_date','modified_date')

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""

class EmailTemplateSerializer(serializers.ModelSerializer):
	""" Email Template serilaizer for creating """
	class Meta:
		model = EmailTemplate
		fields = ('name','campaign','email_body', 'email_subject', 'status')

class EmailTemplatePaginationSerializer(serializers.ModelSerializer):
	""" Email Template pagination serializer for email template pagination  of Script"""
	created_by_user = serializers.SerializerMethodField()
	campaign = serializers.SerializerMethodField()
	class Meta:
		model = EmailTemplate
		fields = ('name','id','campaign','created_by_user', 'status','created_date','modified_date')

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""

	def get_campaign(self,obj):
		if obj.campaign.all():
			return ",".join(i.name for i in obj.campaign.all())

# this class is for validating the pausebreaks serializer form
class PauseBreakSerializer(serializers.ModelSerializer):
	is_edit = serializers.SerializerMethodField()
	class Meta:
		model = PauseBreak
		fields = ('id','name','break_time','break_color_code','status', 'created_by','is_edit','inactive_on_exceed')

	def get_is_edit(self, obj):
		agent_logged_in_campaign = get_login_campaign()
		break_entries = list(Campaign.objects.filter(name__in=agent_logged_in_campaign).values_list("breaks__id",flat=True))
		if obj.id in break_entries:
			return "false"
		return "true"


class PauseBreakPaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the breaks that is created """
	created_by_user = serializers.SerializerMethodField()
	class Meta:
		model = PauseBreak
		fields = ('name','id','status', 'created_by_user','created_date','modified_date')

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""
		
# this class is for validating the group serializer form
class GroupSerializer(serializers.ModelSerializer):
	users = serializers.ReadOnlyField()
	is_edit = serializers.SerializerMethodField()
	class Meta:
		model = Group
		fields = ('id','name','status','color_code', 'users','is_edit')

	def get_is_edit(self, obj):
		agent_logged_in = get_login_agent()
		group_list = list(User.objects.filter(username__in=agent_logged_in).values_list("group__id",flat=True))
		if obj.id in group_list:
			return "false"
		return "true"

class GroupPaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the group that is created """
	users_name = serializers.ReadOnlyField()
	created_by = serializers.SerializerMethodField()
	class Meta:
		model = Group
		fields = ('name','id', 'status','users_name', 'created_by','created_date','modified_date')

	def get_created_by(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""

# this class is for validating the pausebreaks serializer form
class CampaignScheduleSerializer(serializers.ModelSerializer):
	class Meta:
		model = CampaignSchedule
		fields = ('name','description','status','schedule','schedule_days')

class CampaignSchedulePaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the campaignscheduler that is created """
	created_by_user = serializers.SerializerMethodField()
	class Meta:
		model = CampaignSchedule
		fields = ('name','id','description','status','created_by_user','created_date','modified_date')

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""

# this class is for validating the switch serializer form
class SwitchSerializer(serializers.ModelSerializer):
	is_edit = serializers.SerializerMethodField()
	class Meta:
		model = Switch
		fields = ('name', 'id','ip_address','status', 'created_by','is_edit', 'sip_udp_port','rpc_port','wss_port',)

	def get_is_edit(self, obj):
		agent_logged_in_campaign = []
		# agent_logged_in_campaign = get_login_campaign()
		switch_entries = list(Campaign.objects.filter(name__in=agent_logged_in_campaign).values_list("switch__id",flat=True))
		if obj.id in switch_entries:
			return "false"
		return "true"

# this class is for validating the switch serializer form
class SwitchPaginationSerializer(serializers.ModelSerializer):
	created_by_user = serializers.SerializerMethodField()
	class Meta:
		model = Switch
		fields = ('name', 'id','ip_address','status', 'created_by_user','created_date','modified_date')

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""

class AgentPauseBreakSerializer(serializers.ModelSerializer):
	class Meta:
		model = PauseBreak
		fields = ('name','break_time','inactive_on_exceed')

class ReadOnlyCampaignSerializer(serializers.ModelSerializer):
	'''
	This serializer is for creating campaign
	'''
	breaks = AgentPauseBreakSerializer(many=True)
	group = GroupSerializer(many=True)
	switch = SwitchSerializer()
	prefix = serializers.ReadOnlyField()
	class Meta:
		model = Campaign
		exclude = ()

# this class is for validating the disposition serializer form
class DispositionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Disposition
		fields = ('name','dispos','dispo_type','dispo_keys','color_code','status','updatelead','show_dispo')

class DispositionPaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the disposition that is created """
	created_by_user = serializers.SerializerMethodField()
	class Meta:
		model = Disposition
		fields = ('name','id','status', 'created_by_user','created_date','modified_date')

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""

# this class is for validating the disposition serializer form
class RelationTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = RelationTag
		fields = ('name','relation_fields','relation_type','color_code','status')

class RelationTagPaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the relationtag that is created """
	created_by_user = serializers.SerializerMethodField()
	class Meta:
		model = RelationTag
		fields = ('name','id','status', 'created_by_user','created_date','modified_date')

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""

# this class is for validating the pausebreaks serializer form
class DialTrunkSerializer(serializers.ModelSerializer):
	is_edit = serializers.SerializerMethodField()
	class Meta:
		model = DialTrunk
		fields = ('name','dial_string','channel_count','trunk_type','switch','status','prefix','country_code', 'created_by','did_range','is_edit' )

	def get_is_edit(self, obj):
		agent_logged_in_campaign = get_login_campaign()
		trunk_entries = list(Campaign.objects.filter(name__in=agent_logged_in_campaign).values_list("trunk__id",flat=True))
		if obj.id in trunk_entries:
			return "false"
		return "true"

class DialTrunkPaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the dialtrunk that is created """
	switch_name = serializers.SerializerMethodField()
	created_by_user = serializers.SerializerMethodField()
	class Meta:
		model = DialTrunk
		fields = ('name','id','dial_string','trunk_type', 'switch_name', 'created_by_user', 'status','created_date','modified_date')

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""

	def get_switch_name(self, obj):
		if obj.switch:
			return obj.switch.ip_address
		else:
			return ""

class DialTrunkGroupSerializer(serializers.ModelSerializer):
	""" Dail trunk serializer group for creation"""
	class Meta:
		model = DiaTrunkGroup
		fields = ('name','total_channel_count','status')

class DialTrunkGroupPaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the dialtrunkgroup that is created """
	created_by_user = serializers.SerializerMethodField()
	class Meta:
		model = DiaTrunkGroup
		fields = ('name','id','total_channel_count','created_by_user', 'status','created_date')

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""

# this class is for validating the user group serializer form
class UserRoleSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserRole
		fields = ('name','description','status','access_level','permissions')

class UserRolePaginationSerializer(serializers.ModelSerializer):
	created_by_user = serializers.ReadOnlyField()
	class Meta:
		model = UserRole
		fields = ('name','id','access_level','created_by_user','status','created_date','modified_date')

class UpdateCampaignSerializer(serializers.ModelSerializer):
	class Meta:
		model = CampaignVariable
		fields = ('strategy', 'dial_ratio', 'variables', 'ndnc_scrub',
			'moh_sound', 'time_base_score', 'max_wait_time_with_no_agent',
			'max_wait_time_with_no_agent_time_reached', 'dialtimeout',
			'extension', 'caller_id', 'prefix','max_wait_time', 'hold_music', 'wfh_caller_id')

class LeadRecycleSerializer(serializers.ModelSerializer):
	class Meta:
		model = LeadRecycle
		fields = ('name','schedule_period','recycle_time','count', 'status', 'schedule_type')

class AudioSerializer(serializers.ModelSerializer):
	class Meta:
		model = AudioFile
		fields = ('name', 'description', 'audio_file', 'status')

class AudioPaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the audio file that is created """
	created_by_user = serializers.SerializerMethodField()
	class Meta:
		model = AudioFile
		fields = ('name','id','description', 'created_by_user', 'status','created_date','modified_date')

	def get_created_by_user(self, obj):
		if obj.created_by:
			return obj.created_by.username
		else:
			return ""



class CallDetailSerializer(serializers.ModelSerializer):
	""" serializer for calldetails display """
	class Meta:
		model = CallDetail
		exclude = ('campaign','user','ring_time', 'call_duration','phonebook')

class NdncDeltaUploadSerializer(serializers.ModelSerializer):
	""" serializer for NDNC upload """
	class Meta:
		model = NdncDeltaUpload
		fields =  ('delta_file',)


class DncSerializer(serializers.ModelSerializer):
	""" serializer for DNC contacts """
	class Meta:
		model = DNC
		exclude = ('campaign','user')

class DNCUpdateSerializer(serializers.ModelSerializer):
	""" serializer for DNC Update contacts """
	class Meta:
		model = DNC
		fields = ('numeric','campaign','global_dnc','status')

class SkilledRoutingSerializer(serializers.ModelSerializer):
	"""docstring for CssSerializer """
	class Meta:
		model = SkilledRouting
		exclude = ('skills','skill_id')

class SkilledRoutingPaginationSerializer(serializers.ModelSerializer):
	"""docstring for skillrouting pagination created """
	skill_id = serializers.SerializerMethodField()
	class Meta:
		model = SkilledRouting
		fields = ('name', 'id', 'skill_id', 'status','created','updated')

	def get_skill_id(self,obj):
		skill_dids = SkilledRoutingCallerid.objects.filter(skill=obj).values_list('caller_id',flat=True)
		if skill_dids.exists():
			return ','.join(list(skill_dids))
		return ""


class CssSerializer(serializers.ModelSerializer):
	"""docstring for CssSerializer """
	class Meta:
		model = CSS
		exclude = ('raw_query',)


class CssPaginationSerializer(serializers.ModelSerializer):
	"""docstring for CssSerializer """
	data_count = serializers.SerializerMethodField()
	class Meta:
		model = CSS
		fields = ('name','id', 'status','campaign','data_count','created','updated')

	def get_data_count(self,obj):
		contact_count = 0
		try:
			for query in obj.raw_query:
				contact = Contact.objects.raw(query['query_string'])
				contact_count = contact_count + len(list(contact))
			return contact_count
		except Exception as e:
			print(e, "error is css query count")
			return contact_count 

class NotificationSerializer(serializers.ModelSerializer):
	""" docstring for Notification data """
	class Meta:
		model = Notification
		fields = '__all__'

class CurrentCallBackSerializer(serializers.ModelSerializer):
	""" serializer for currentcallbackcontacts data  """
	schedule_date = serializers.ReadOnlyField()
	full_name = serializers.SerializerMethodField()
	class Meta:
		model = CurrentCallBack
		fields = '__all__'

	def get_full_name(self,obj):
		username = ""
		if obj.user:
			user_var = UserVariable.objects.filter(extension = obj.user)
			if user_var.exists():
				username = user_var.first().user.first_name + " " + user_var.first().user.last_name
		return username


class AbandonedcallSerializer(serializers.ModelSerializer):
	""" serializer for abandonedcall data  """
	call_date = serializers.ReadOnlyField()
	full_name = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	class Meta:
		model = Abandonedcall
		fields = '__all__'

	def get_username(self,obj):
		username = ""
		user_var = UserVariable.objects.filter(extension=obj.user).values('user__username').first()
		if user_var:
			username = user_var['user__username']
		return username

	def get_full_name(self,obj):
		fullname = ""
		user_var = UserVariable.objects.filter(extension=obj.user).values('user__first_name', 'user__last_name').first()
		if user_var:
			fullname = user_var['user__first_name'] + " " + user_var['user__last_name']
		return fullname

class SnoozedCallbackSerializer(serializers.ModelSerializer):
	""" serializer for snoozedcall data  """
	class Meta:
		model = SnoozedCallback
		fields = '__all__'

class CallBackContactSerializer(serializers.ModelSerializer):
	""" serializer for callbackcontacts data  """
	class Meta:
		model = CallBackContact
		fields = '__all__'

class SetCallBackContactSerializer(serializers.ModelSerializer):
	""" serializer for callback  data  insertion"""
	class Meta:
		model = CallBackContact
		exclude = ('customer_raw_data','alt_numeric')

class TempCallBackContactSerializer(serializers.ModelSerializer):
	""" serializer for callback  data  insertion data  """
	call_date = serializers.ReadOnlyField()
	class Meta:
		model = CallBackContact
		fields = ('user','comment','call_date')

class CdrFeedbckReportSeializer(serializers.ModelSerializer):
	""" serializer for cdr feedback insertion for the calldetail report """
	class Meta:
		model = CdrFeedbck
		fields = ('primary_dispo','feedback','relation_tag','comment')


class DiallerEventLogSerializer(serializers.ModelSerializer):
	""" serializer for diallerevent log report """
	user = serializers.StringRelatedField()
	full_name = serializers.SerializerMethodField()
	campaign = serializers.StringRelatedField()
	init_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	ring_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	connect_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	hangup_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	is_feedback = serializers.SerializerMethodField()
	ip_address = serializers.SerializerMethodField()
	class Meta:
		model = DiallerEventLog
		fields= '__all__'   

	def get_full_name(self,obj):
		username = ""
		if obj.user:
			username = obj.user.first_name + " " + obj.user.last_name
		return username

	def get_is_feedback(self,obj):
		feedback = "false"
		call_recording_feedback = CallRecordingFeedback.objects.filter(calldetail__session_uuid=obj.session_uuid)
		if call_recording_feedback.exists():
			feedback = "true"
		return feedback
	def get_ip_address(self,obj):
		ip_address = ''
		if obj.campaign_name:
			ip_address = list(Campaign.objects.filter(name=obj.campaign_name).values_list('switch__ip_address', flat=True))[0]
		return ip_address

class DiallerEventLogTimeSerializer(serializers.ModelSerializer):
	""" sericlizzer for diallerevent log time format data serilizer"""
	init_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	ring_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	connect_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	hangup_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	class Meta:
		model = DiallerEventLog
		fields = ('init_time', 'ring_time', 'connect_time', 'hangup_time', 'wait_time', 'ring_duration', 'hold_time', 'bill_sec','ivr_duration','call_duration','hangup_cause','hangup_cause_code','dialed_status',)

class SMSLogSerializer(serializers.ModelSerializer):
	""" SMS sent log serilaizer data """
	class Meta:
		model = SMSLog
		fields = '__all__'
		
class CallDetailReportSerializer(serializers.ModelSerializer):
	""" serlialzer for calldetail report data """
	user = serializers.StringRelatedField()
	supervisor_name = serializers.SerializerMethodField() 
	campaign = serializers.StringRelatedField()
	diallereventlog = DiallerEventLogSerializer()
	call_length = serializers.SerializerMethodField()
	cdrfeedback = CdrFeedbckReportSeializer(read_only=True)
	full_name = serializers.SerializerMethodField()
	customer_name = serializers.SerializerMethodField()
	client_name = serializers.SerializerMethodField()
	smslog = serializers.SerializerMethodField()
	class Meta:
		model = CallDetail
		# fields= '__all__'
		exclude = ('init_time', 'ring_time', 'connect_time', 'hangup_time', 'wait_time', 'ring_duration', 'hold_time', 'bill_sec','ivr_duration','hangup_cause','hangup_cause_code','dialed_status',)
		
	def get_call_length(self,obj):
		call_duration = timedelta(hours=obj.diallereventlog().call_duration.hour, minutes=obj.diallereventlog().call_duration.minute,
			seconds=obj.diallereventlog().call_duration.second)
		feedback = timedelta(hours=obj.feedback_time.hour, minutes=obj.feedback_time.minute, 
			seconds=obj.feedback_time.second)
		call_length = datetime.strptime(str(call_duration + feedback),'%H:%M:%S').time()
		return call_length

	

	def get_full_name(self,obj):
		username = ""
		if obj.user:
			username = obj.user.first_name + " " + obj.user.last_name
		return username

	def get_customer_name(self,obj):
		customer_name = ""
		contact_inst  = Contact.objects.filter(id=obj.contact_id).first()
		print(contact_inst)
		if obj and contact_inst:
			if contact_inst and contact_inst.customer_raw_data and 'customer_information' in contact_inst.customer_raw_data:
				if 'customer_name' in contact_inst.customer_raw_data['customer_information']:
					customer_name = contact_inst.customer_raw_data['customer_information']['customer_name']
					print(customer_name)
		return customer_name

	def get_client_name(self,obj):
		client_name = ""
		contact_inst  = Contact.objects.filter(id=obj.contact_id).first()
		if obj and contact_inst:
			if contact_inst and contact_inst.customer_raw_data and 'customer_information' in contact_inst.customer_raw_data:
				if 'client_name' in contact_inst.customer_raw_data['customer_information']:
					client_name = contact_inst.customer_raw_data['customer_information']['client_name']
		return client_name

	def get_smslog(self,obj):
		fields_dict = {}
		message = []
		sms_list= []
		fields_dict['sms_sent'] = 'NO'
		if obj.session_uuid:
			sms_obj = SMSLog.objects.filter(session_uuid=obj.session_uuid)
			if sms_obj.exists():
				fields_dict['sms_sent'] = 'YES'
				fields_dict['sms_message'] = ','.join(list(sms_obj.exclude(template_id=None).values_list('template__name',flat=True)))               
		return fields_dict

	def get_supervisor_name(self,obj):
		supervisor_name = ""
		if obj.user:
			supervisor_name = obj.user.reporting_to.username if obj.user.reporting_to else ""
		return supervisor_name
		
class CallDetailReportFieldSerializer(serializers.ModelSerializer):
	""" serlializer to the fields of calldetails report """
	cdrfeedback = CdrFeedbckReportSeializer()
	class Meta:
		model = CallDetail
		fields = ('customer_cid','campaign_name','phonebook','call_duration','callmode','created','cdrfeedback',)

class CallHistorySerializer(serializers.ModelSerializer):
	""" Serlialzer for the callhistory data display """
	user = serializers.StringRelatedField()
	diallereventlog = DiallerEventLogTimeSerializer()
	primary_dispo = serializers.SerializerMethodField()
	comment = serializers.SerializerMethodField()
	class Meta:
		model = CallDetail
		fields = ('user','campaign_name','destination_extension','customer_cid','callflow','diallereventlog',
			'primary_dispo','uniqueid','comment','session_uuid','dialed_status')

	def get_primary_dispo(self,obj):
		try:
			if obj.cdrfeedback:
				return obj.cdrfeedback.primary_dispo
			return ''
		except:
			return ''

	def get_comment(self,obj):
		try:
			if obj.cdrfeedback:
				return obj.cdrfeedback.comment
			return ''
		except:
			return ''

class AgentActivityReportSerializer(serializers.ModelSerializer):
	""" Serlialzer for the agent activity report showing """
	user = serializers.StringRelatedField()
	full_name = serializers.SerializerMethodField()
	event_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	class Meta:
		model = AgentActivity
		exclude = ('wait_time',)

	def get_full_name(self,obj):
		username = ""
		if obj.user:
			username = obj.user.first_name + " " + obj.user.last_name
		return username

class TempAbandonedcallSerializer(serializers.ModelSerializer):
	class Meta:
		model = Abandonedcall
		fields = ('user',)

class AdminActivityReportSerializer(serializers.ModelSerializer):
	""" Serlialzer for the admin activity report showing"""
	created_by = serializers.StringRelatedField()
	class Meta:
		model = AdminLogEntry
		fields= '__all__'

class ThirdPartyApiUserTokenSerialzer(serializers.ModelSerializer):
	""" Serlialzer for the Thirdparyy user token showing """
	user = serializers.StringRelatedField()
	campaign = serializers.StringRelatedField()
	class Meta:
		model = ThirdPartyApiUserToken
		fields  = ('user','campaign','domain','mobile_no','id')

class SmsTemplateSerializer(serializers.ModelSerializer):
	"""Serlialzer for the sms template showing"""
	class Meta:
		model = SMSTemplate
		fields = ('name','campaign','text', 'status','template_type')
class TemplatePaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the templates that is created """
	created_by = serializers.StringRelatedField()
	status =  serializers.CharField(source='get_status_display')
	campaign = serializers.StringRelatedField()
	template_type = serializers.CharField(source='get_template_type_display')
	class Meta:
		model = SMSTemplate
		fields = ('name','id','created_by', 'status', 'campaign','template_type','created_date','modified_date')
class GatewayPaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the gateway that is created """
	created_by = serializers.StringRelatedField()
	disposition = serializers.SerializerMethodField()
	status = serializers.CharField(source='get_status_display')
	sms_trigger_on = serializers.CharField(source='get_sms_trigger_on_display')
	template = serializers.SerializerMethodField()
	class Meta:
		model = SMSGateway
		fields = ('name','id','disposition','created_by', 'status','sms_trigger_on','template','created_date','modified_date')
	def get_disposition(self,obj):
		if obj.disposition.all():
			return ",".join(i.name for i in obj.disposition.all())
	def get_template(self,obj):
		if obj.template.all():
			return ",".join(i.name for i in obj.template.all())
class SmsGatewaySerializer(serializers.ModelSerializer):
	class Meta:
		model = SMSGateway
		fields = ('name','disposition','sms_trigger_on', 'status','template','gateway_url','key')

class EmailGatewayPaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the emailgateway that is created """
	created_by = serializers.StringRelatedField()
	disposition = serializers.SerializerMethodField()
	status = serializers.CharField(source='get_status_display')
	email_trigger_on = serializers.CharField(source='get_email_trigger_on_display')
	template = serializers.SerializerMethodField()
	class Meta:
		model = EmailGateway
		fields = ('name','id','disposition','created_by', 'status','email_trigger_on','template','created_date','modified_date')
	def get_disposition(self,obj):
		if obj.disposition.all():
			return ",".join(i.name for i in obj.disposition.all())
	def get_template(self,obj):
		if obj.template.all():
			return ",".join(i.name for i in obj.template.all())

class EmailGatewaySerializer(serializers.ModelSerializer):
	class Meta:
		model = EmailGateway
		exclude = ('site','created_date','modified_date','created_by')

class ThirdPartyAPISerializer(serializers.ModelSerializer):
	class Meta:
		model =ThirdPartyApi
		fields = '__all__'

class ThirdPartyApiPaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the thirdparty crm that is created """
	status = serializers.CharField(source='get_status_display')
	campaign = serializers.SerializerMethodField()
	class Meta:
		model = ThirdPartyApi
		fields = ('name', 'id', 'status','created','dynamic_api','campaign','created','updated')

	def get_campaign(self,obj):
		camp_names = []
		if obj:
			for camp in obj.campaign.all():
				camp_names.append(camp.name)
			return camp_names 
		else:
			return ""
class VoiceBlasterSerializer(serializers.ModelSerializer):
	""" Serlialzer for the voiceblaster showing """
	class Meta:
		model = VoiceBlaster
		fields = '__all__'

class VoiceBlasterPaginationSerializer(serializers.ModelSerializer):
	""" This serializer for pagination of the voiceblaster that is created """
	status = serializers.CharField(source='get_status_display')
	campaign = serializers.SerializerMethodField()
	vb_mode = serializers.CharField(source='get_vb_mode_display')
	class Meta:
		model = VoiceBlaster
		fields = ('name','id','status','campaign','vb_mode', 'voice_blaster','created','updated')

	def get_campaign(self,obj):
		camp_names = []
		if obj:
			for camp in obj.campaign.all():
				camp_names.append(camp.name)
			return camp_names 
		else:
			return ""   

class EmailSchedulerSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmailScheduler
		exclude = ('reports',)

# this class is for validating the call recording serializer form
class CallRecordingFeedbackSerializer(serializers.ModelSerializer):
	agent = serializers.SerializerMethodField()
	cli = serializers.SerializerMethodField()
	session_uuid = serializers.SerializerMethodField()
	primary_dispo = serializers.SerializerMethodField()
	uniqueid = serializers.SerializerMethodField()
	submitted_by = serializers.SerializerMethodField()
	class Meta:
		model = CallRecordingFeedback
		fields = ('id','agent','cli','session_uuid','primary_dispo','uniqueid','feedback','submitted_by')

	def get_agent(self,obj):
		return obj.calldetail.user.username

	def get_cli(self,obj):
		return obj.calldetail.customer_cid

	def get_session_uuid(self,obj):
		return obj.calldetail.session_uuid

	def get_primary_dispo(self,obj):
		return CdrFeedbck.objects.get(calldetail=obj.calldetail).primary_dispo

	def get_uniqueid(self,obj):
		return obj.calldetail.uniqueid

	def get_submitted_by(self,obj):
		return obj.user.username
		
class SubModulesSerializer(serializers.ModelSerializer):
	url = serializers.SerializerMethodField()
	class Meta:
		model = Modules
		fields = ('id', 'name', 'title','url','icon', 'permission_list', 'status','parent','sequence','is_menu')
	def get_url(self, obj):
		if obj.url_abbr:
			return obj.url_abbr+'-'+obj.name
		return obj.name
class ModulesSerializer(serializers.ModelSerializer):
	""" Serlialzer for showing the submodules"""
	url = serializers.SerializerMethodField()
	parent_menu = SubModulesSerializer(many=True, read_only=True)
	class Meta:
		model = Modules
		fields = ('id', 'name', 'title', 'parent_menu','url','icon', 'permissions','status','parent','sequence')
	def get_url(self, obj):
		if obj.url_abbr:
			return obj.url_abbr+'-'+obj.name
		return obj.name
	def to_representation(self, instance):
		response = super().to_representation(instance)
		response["parent_menu"] = sorted(response["parent_menu"], key=lambda x: x["sequence"])
		return response
class ModuleSerializer(serializers.ModelSerializer):
	""" Serlialzer for the showing modules"""
	permission_list = serializers.ReadOnlyField()
	parent_menu = SubModulesSerializer(many=True, read_only=True)

	class Meta:
		model = Modules
		fields = ('name', 'permission_list','parent_menu', 'permissions')

	def to_representation(self, instance):
		response = super().to_representation(instance)
		response["parent_menu"] = sorted(response["parent_menu"], key=lambda x: x["sequence"])
		return response

class LoginAgentDataSerializer(serializers.ModelSerializer):
	access_level = serializers.SerializerMethodField()
	device_pass = serializers.CharField(source='properties.device_pass')
	class Meta:
		model = User
		fields = ('id','username','caller_id','call_type','extension','access_level','device_pass')

	def get_access_level(self, obj):
		if obj.user_role:
			return obj.user_role.access_level
		return ''
		
class BroadCastMessageSerializer(serializers.ModelSerializer):
	""" Serlialzer for the broadcast message create """
	class Meta:
		model = BroadcastMessages
		fields = ('message','message_type','receivers','sent_by')

class BroadcastMessageViewSerializer(serializers.ModelSerializer):
	""" Serlialzer for the boradcast message showing """
	sent_by = serializers.SerializerMethodField()
	class Meta:
		model = BroadcastMessages
		fields = ('id','message','sent_by','created')

	def get_sent_by(self, obj):
		if obj.sent_by:
			username = obj.sent_by.username
			if obj.sent_by:
				if obj.sent_by.first_name:
					username = obj.sent_by.first_name + " " + obj.sent_by.last_name
					return username
				else:
					return username
			else:
				return username
		return ''

class DaemonsUpdateSerializer(serializers.ModelSerializer):
	""" Serlialzer for the Demon service  showing """
	class Meta:
		model = Daemons
		fields = ('service_name','status')

class HolidaysSerializer(serializers.ModelSerializer):
	class Meta:
		model = Holidays
		fields = ('name','holiday_date','description', 'status','holiday_audio')

class HolidaysPaginationSerializer(serializers.ModelSerializer):
	created_by = serializers.StringRelatedField()
	holiday_audio = serializers.StringRelatedField()
	status =  serializers.CharField(source='get_status_display')
	class Meta:
		model = Holidays
		fields = ('name','id','created_by', 'holiday_date', 'holiday_audio','status')

class ThirdPartyApiUserTokenEditSerialzer(serializers.ModelSerializer):
	""" Serlialzer for the Thirdparyy user token showing """
	class Meta:
		model = ThirdPartyApiUserToken
		fields  = ('user','campaign','domain','mobile_no',)

class PasswordManagementSerialzer(serializers.ModelSerializer):
	""" Saving Password information and also for update """	
	class Meta:
		model = PasswordManagement
		fields ='__all__'


class ThirdPartyApiDispositionSerializer(serializers.ModelSerializer):	
	unique_id= serializers.CharField(required=True)
	disposition	= serializers.CharField(required=True)
	disposition_desc = serializers.CharField(required=False)
	callBabkDate = serializers.CharField(required=False)
	callBabkTime = serializers.CharField(required=False)
	flexiAgentId = serializers.CharField(required=False)
	callid = serializers.CharField(required=False)
	
	class Meta:
		model = ThirdPartyApiDisposition
		fields ="__all__"