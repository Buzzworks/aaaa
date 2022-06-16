from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
	path('UserManagement/Users/', views.UsersListApiView.as_view(), name="users"),
	path('UserManagement/Users/create/', views.UsersCreateApiView.as_view(), name="create-users"),
	path('UserManagement/Users/<int:pk>/',
		 views.UsersEditApiView.as_view(), name="edit-users"),
	path('UserManagement/PasswordManagement/',views.PasswordManagementApiView.as_view(), name="password_management"),
	path('UserManagement/check-user/',
		 views.CheckUserApiView.as_view(), name="check-user"),
	path('UserManagement/UserRoles/',
		 views.UserRoleView.as_view(), name="user_roles"),
	path('UserManagement/UserRole/create',
		 views.UserRoleCreateApiView.as_view(), name="create-user_roles"),
	path('UserManagement/UserRole/<int:pk>/',
		 views.UserRoleModifyView.as_view(), name="modify-user_roles"),
	path('UserManagement/Groups/',
		 views.GroupListApiView.as_view(), name="groups"),
	path('UserManagement/get-group/<int:pk>/',
		 views.GroupModifyApiView.as_view(), name="get-group"),
	path('CampaignManagement/DialTrunk/',
		 views.DialTrunkListApiView.as_view(), name="dialtrunks"),
	path('Modules/DialTrunkGroup/',
		 views.DialTrunkGroupListApiView.as_view(), name="dialtrunk_group"),
	path('Modules/DialTrunkGroup/create/', views.TrunkGroupCreateEditApiView.as_view(), name="create-trunk-group"),
	path('Modules/DialTrunkGroup/<int:pk>/', views.TrunkGroupCreateEditApiView.as_view(), name="edit-trunk-group"),
	path('Modules/DialTrunkGroup/check-dial-trunk/', views.TrunkGroupCheckApiView.as_view(), name="trunk-check"),
	path('CampaignManagement/get-dialtrunk/<int:pk>/',
		 views.DialTrunkModifyApiView.as_view(), name="get-dialtrunk"),
	path('CampaignManagement/Switch/',
		 views.SwitchListApiView.as_view(), name="switch"),
	path('CampaignManagement/get-switch/<int:pk>/',
		 views.SwitchListApiView.as_view(), name="get-switch"),
	path('CampaignManagement/Campaign/create/',
		 views.CampaignCreateApiView.as_view(), name="create-campaigns"),
	path('CampaignManagement/Campaign/<int:pk>/',
		 views.CampaignEditApiView.as_view(), name="edit-campaigns"),
	path('CampaignManagement/Campaigns/',
		 views.CampaignListApiView.as_view(), name="campaigns"),
	path('CampaignManagement/InGroupCampaign/',
		 views.InGroupCampaignListApiView.as_view(), name="ingroup_campaign"),
	path('CampaignManagement/InGroupCampaign/create/',
		 views.InGroupCampaignCreateApiView.as_view(), name="create-ingroup_campaign"),
	path('CampaignManagement/InGroupCampaign/<int:pk>/', views.InGroupCampaignCreateApiView.as_view(), name="edit-ingroup_campaign"),
	path('CampaignManagement/skilled/',
		 views.SkilledRoutingApiView.as_view(), name="skilledrouting"),
	path('CampaignManagement/create/skilled/',
		 views.CreateSkilledRoutingApiView.as_view(), name="create-skilledrouting"),
	 path('CampaignManagement/skilled/<int:pk>/',
		 views.EditSkilledRoutingApiView.as_view(), name="edit-skilledrouting"),
	path('CampaignManagement/css/',
		 views.CssListApiView.as_view(), name="css"),
	path('CampaignManagement/css/create/',
		 views.CssCreateEditApiView.as_view(), name="create-css"),
	path('CampaignManagement/css/<int:pk>/',
		 views.CssCreateEditApiView.as_view(), name="edit-css"),
	path('CampaignManagement/check-query/',
		 views.CssExecuteQuery.as_view(), name="edit-css"),
	path('CampaignManagement/Dispositions/create/',
		 views.DispositionsCreateApiView.as_view(), name="create-dispositions"),    
	path('CampaignManagement/Dispositions/<int:pk>/',
		 views.DispositionsEditApiView.as_view(), name="edit-dispositions"),   
	path('CampaignManagement/get-existing-disposition/<int:pk>/',
		 views.GetExistingDisposition.as_view(), name="get-existing-dispositions"),    
	path('CampaignManagement/Dispositions/',
		 views.DisposListApiView.as_view(), name="dispositions"),
	path('CampaignManagement/RelationTags/',
		 views.RelationTagListApiView.as_view(), name="relationtags"),
	path('CampaignManagement/RelationTags/create/',
		 views.RelationTagCreateApiView.as_view(), name="create-relationtags"),
	path('CampaignManagement/RelationTags/<int:pk>/',
		 views.RelationTagEditApiView.as_view(), name="edit-relationtags"),
	path('CampaignManagement/Pausebreaks/',
		 views.PausebreaksListApiView.as_view(), name="pause_breaks"),
	path('CampaignManagement/get-pausebreak/<int:pk>/',
		 views.PausebreaksModifyApiView.as_view(), name="get-pausebreak"),
	path('CampaignManagement/Scripts/', views.ScriptListApiView.as_view(), name="scripts"),
	path('CampaignManagement/Script/create/',
		 views.ScriptCreateEditApiView.as_view(), name="create-scripts"),
	path('CampaignManagement/Script/edit/<int:pk>/',
		 views.ScriptCreateEditApiView.as_view(), name="edit-scripts"),
	path('CampaignManagement/Script/get-crm-fields/',
		 views.ScriptGetCrmFieldsApiView.as_view(), name="script-get-crmfields"),
	path('CampaignManagement/Audiofiles/',
		 views.AudioListApiView.as_view(), name="audio_files"),
	path('UserManagement/Users/bulk-upload/',
		 views.ValidateUserUploadApiView.as_view(), name="users-bulk-upload"),
	path('UserManagement/Users/upload-operation/',
		 views.UserUploadApiView.as_view(), name="users-upload"),
	path('CampaignManagement/upload-audio-file/',
		 views.UploadAudioFileApiView.as_view(), name="upload-audio-file"),
	path('CampaignManagement/edit-audio/<int:pk>/',
		 views.UploadAudioFileApiView.as_view(), name="edit-audio"),
	path('CampaignManagement/CampaignSchedule/create/',
		 views.CamapignScheduleCreateApiView.as_view(), name="create-campaign_schedules"),
	path('CampaignManagement/CampaignSchedule/<int:pk>/',
		 views.CampaignScheduleEditApiView.as_view(), name="edit-campaign_schedules"),
	path('CampaignManagement/CampaignSchedule/',
		views.CampaignScheduleListApiView.as_view(), name="campaign_schedules"),
	# Reports section starts
	path('CallReports/CallDetailReport/',views.CallDetailReportView.as_view(),name='report-call_detail'),
	path('CallReports/AgentActivity/',views.AgentActivityReportView.as_view(),name='report-agent_activity'),
	path('CallReports/AgentPerformance/',views.AgentPerformanceReportView.as_view(),name='report-agent_performance'),
	path('CallReports/CampaignPerformance/',views.CampainwisePerformanceReportView.as_view(),name='report-campaign_performance'),
	path('CallReports/AgentMIS/',views.AgentMISReportView.as_view(),name='report-agent_mis'),
	path('CallReports/CampaignMIS/',views.CampaignMISReportView.as_view(),name='report-campaign_mis'),
	path('CallReports/CallRecordings/', views.CallRecordingView.as_view(), name='report-call_recordings'),
	path('CallReports/CallRecordingsDetail/<int:pk>/', views.CallRecordingDetailView.as_view(), name='report-call_recordings-detail'),
	path('CallReports/PendingCallBackReport/', views.PendingCallbackCallView.as_view(), name='report-reschedule_callbacks'),
	path('CallReports/PendingAbandonedReport/', views.PendingAbandonedCallView.as_view(), name='report-reschedule_abandoned_call'),
	path('CallReports/CallRecordingFeddbackReport/', views.CallRecordingFeedbackView.as_view(), name='call_recording_feedback'),
	path('AlternateNumberReport/', views.AlternateNumberView.as_view(), name='alternate_number'),
	path('Management/ManagementPerformance/',views.ManagementPerformanceReportView.as_view(),name='management_performance'),
	path('Billings/', views.BillingView.as_view(), name='report-billing'),
	path('api/pending-call-update-user/', views.PendingCallbackUpdateUserView.as_view(), name='report-pending_callback_update_user'),
	path('api/update-abandoned-call-user/', views.UpdateAbandonedCallUserView.as_view(), name='report-update_abandoned_call_user'),
	path('Administration/daemon/',
         views.DaemonServicesListAPIView.as_view(), name="daemon"),
    path('Administration/daemon/create_edit/',
         views.DaemonCreateModifyApiView.as_view(), name="daemon_create_edit"),
	path('Administration/admin-log/', views.AdminLogAPIView.as_view(), name='admin_log'),
	path('Administration/Ndnc/', views.NdncListAPIView.as_view(), name="ndnc"),
	path('Administration/dnc/', views.DNCListAPIView.as_view(), name="dnc"),
	path('Administration/dnc-upload/',views.DNCUploadApiView.as_view(), name="dnc-upload"),
	path('Administration/dnc/create_edit/', views.DNCCreateModifyApiView.as_view(),name="get-dnc"),
	path('Administration/modules/', views.ModulesView.as_view(), name="modules"),
	path('api/adminlivecount/', views.AdminLiveCountApiView.as_view(), name='adminlivecount'),
	path('api/reset_password/', views.ResetPasswordApiView.as_view(), name='reset_password'),
	path('api/wfh_reset_password/', views.ResetWfhPasswordApiView.as_view(), name='reset_wfh_password'),
	path('api/emergency_logout/', views.EmergencyLogoutApiView.as_view(), name='emergency_logout'),
	path('api/emergency_logout_all_user/', views.EmergencyLogoutAllUserApiView.as_view(), name='emergency_logout_all_user'),
	path('api/get-onCallAgent-data/',views.OnCallAgentData.as_view(), name='get-onCallAgent-data'),
	path('api/get-loginAgent-data/', views.LoginAgentLiveDataView.as_view(), name='get-loginAgent-data'),
	path('api/get-activeCampaign-data/', views.CampaignLiveDataView.as_view(), name='get-activeCampaign-data'),
	path('api/get-activeAgent-data/', views.ActiveAgentLiveDataAPIView.as_view(), name='get-activeAgent-data'),
	path('api/config/directory/<str:domain>/', views.curl_addsip),
	path('api/config/callcenter/<str:domain>/', views.curl_loadcc),
	path('agent/', views.AgentHomeApiView.as_view(), name="agent"),
	path('api/dailer_login/', views.DiallerLogin.as_view(), name="dailer-login"),
	path('api/manual_dial/', views.ManualDial.as_view(), name="manual_dial"),
	path('api/manual_dial_list/', views.MaunalDialListAPIView.as_view(), name="manual_dial_list"),
	path('api/hangup_call/', views.HangupCall.as_view(), name="hangup_call"),
	path('api/submit_dispo/',views.DispoSubmit.as_view(), name="dispo_submit"),
	path('api/preview-update-contact-status/', views.PreviewUpdateContactStatus.as_view(),
		name="preview-update-contact-status"),
	path('api/skip-call/', views.SkipCallContactStatus.as_view(), name="skip-call"),
	path('api/pause-progressive-call/', views.PauseprogressiveContactStatus.as_view(), name="pause-progressive"),
	path('api/stop-progressive-call/', views.StopprogressiveContactStatus.as_view(), name="stop-progressive"),
	path('api/start-autodial/', views.AutoDialApiView.as_view(),
		name="start-autodial"),
	path('api/autodial-customer-detail/', views.AutodialCustomerDetail.as_view(),
		name="autodial-customer-detail"),
	path('api/start-inbound/', views.InboundApiView.as_view(),
		name="start-inbound"),
	path('api/start-blended-mode/', views.BlendedApiView.as_view(),
		name="start-blended-mode"),    
	path('api/inbound-customer-detail/', views.InboundCustomerDetail.as_view(),
		name="inbound-customer-detail"), 
	path('api/set_ibc_contact_id/', views.SetIbcContactId.as_view(),
		name="set_ibc_contact_id"),           
	path(r'inbound_agents/', views.inbound_agents_availability,name='inbound_agents'),
	path(r'rec_inbound_agents/', views.rec_check_agent_availabilty,name='rec_inbound_agents'),
	path(r'wfh_customer_details/', views.wfh_customer_details,name='wfh_customer_details'),
	path('api/incomingCall/', views.IncomingCallAPIView.as_view(), name="incomingCall"),
	path('api/incoming-sticky-bridge/', views.InboundStickyAgent.as_view(), name="incoming-sticky-bridge"),
	path('api/get-campaign-users/', views.GetCampaignUserAPIView.as_view(), name="get-campaign-user"),
	path('api/park_call/', views.ParkCallAPIView.as_view(),name='park_call'),
	path('api/transferagent/', views.TransferAgentCallAPIView.as_view(),name='transferagent_call'),
	path('api/get-available-agent/', views.GetAvailableAgentsAPIView.as_view(),name='get-available-agent'),
	path('api/webrtc_session_setvar/', views.WebrtcSessionSetVar.as_view(),name='webrtc_session_setvar'),
	path('agent/api/transfer_park_call/', views.TransferParkCallAPIView.as_view(),name='transfer_park_call'),
	path('agent/api/transfer_agentcall_hangup/', views.TransferAgentCallHangupAPIView.as_view(),
		name='transfer_agentcall_hangup'),
	path('agent/api/transfer_call/', views.TransferCallAPIView.as_view(),name='transfer_call'), 
	path('agent/api/internal_transfercall_hangup/',views.InternalTransferCallHangup.as_view(),
		name='internal_transfercall_hangup'),
	path('api/transfer-customer-detail/', views.TransferCustomerDetail.as_view(),
		name="transfer-customer-detail"),
	path('agent/api/merge_call/', views.MergeCallAPIView.as_view(),name='merge_call'), 
	path('api/eavesdrop_activity/', views.EavesdropApiView.as_view(), name="eavesdrop_activity"),
	path('api/eavesdrop_session/', views.EavesdropSessionApiView.as_view(), name="eavesdrop_session"),
	path('api/customer_info/', views.CustomerInfoAPIView.as_view(), name="customer_api_info"),
	path('api/window_reload/',views.WindowReloadApiView.as_view(),name="window_reload"),
	path('api/agentlivedata/', views.AgentLiveDataAPIView.as_view(), name="get-agentlivedata"),
	path('api/get-notifications/', views.NotificationAPIView.as_view(), name="get-notifications"),
	path('api/get-totalcallbacks/', views.GetTotalCallbacks.as_view(), name="get-totalcallbacks"),
	path('api/get-activecallbacks/', views.GetActiveCallbacks.as_view(), name="get-activecallbacks"),
	path('api/get-campaigntotalcallbacks/', views.GetCampaignTotalCallbacks.as_view(), name="get-campaigntotalcallbacks"),
	path('api/update-notification/',views.UpdateNotificationAPIView.as_view(), name="update-notification"),
	path('api/snooze-callback/', views.SnoozeCallbackAPIView.as_view(), name="snooze-callback"),
	path('api/make-callbackcall/', views.MakeCallbackCallAPIView.as_view(), name="make-callbackcall"),
	path('api/get-totalabandonedcalls/', views.GetTotalAbandonedcalls.as_view(), name="get-totalabandonedcalls"),
	path('api/get-campaignabandonedcalls/', views.GetCampaignAbandonedcalls.as_view(), name="get-campaignabandonedcalls"),
	path('api/make-abandonedcall-call/', views.MakeAbandonedCall.as_view(), name="make-abandonedcall-call"),
	path('api/get-totalcallsperday/', views.GetTotalCallsPerDay.as_view(), name="get-totalcallsperday"),
	path('api/get-totalcallsper-month/', views.GetTotalCallsPerMonth.as_view(), name="get-totalcallsper-month"),
	path('api/get-totaluniquecallsper-month/', views.UniqueCallsPerMonth.as_view(), name="get-totaluniquecallsper-month"),
	path('api/get-leadbucket-data/', views.GetLeadBucket.as_view(),name="get-leadbucket-data"),
	path('api/get-piechartlivedata/', views.PieChartLiveData.as_view(),name='piechart-live-data'),
	path('api/get-multilinechartdata/', views.GetMultilineChartLiveData.as_view(), name='get-linelivedata'),
	path('api/get-barchartlivedata/', views.GetAgentCallCountLiveData.as_view(), name='get-barchartlivedata'),
	path('api/get-crmfields-bycampaign/',views.GetCrmFieldsByCampaign.as_view(), name='get-crmfields-bycampaign'),
	path('api/conference_mute/',views.ConferenceMute.as_view(), name='conference_mute'),
	path('api/conference_hangup/', views.ConferenceHangup.as_view(), name='conference_hangup'),
	path('api/get-call-history/',views.GetCallHistoryApiView.as_view(), name="get-call-history"),
	path('api/import-relation-jsondata/',views.ImportRelationData.as_view(),name='import-relation-jsondata'),
	path('api/import-dispo-jsondata/',views.ImportDispositionData.as_view(),name='import-dispo-jsondata'),
	path('api/download-dispo-jsondata/',views.DownloadDispoJsonData,name='download-dispo-jsondata'),
	path('api/download-relation-jsondata/',views.DownloadRelationJsonData,name='download-relation-jsondata'),
	path('api/checkskilled/',views.CheckCampaignInSkilled.as_view(),name="check-skilled-assigned"),
	path('api/get-agent-campaign/',views.GetAgentCampaign.as_view(),name='get-agent-campaign'),
	path('api/get-total-assigned-calls/',views.GetAgentAssignedCall.as_view(), name='get-agent-total-calls'),
	path('api/change-agent-state/',views.ChangeAgentState.as_view(), name='change-agent-state'),
	path('api/reset-agent-availabilty-status/',views.ResetAgentAvailabilityStatus.as_view(), name='reset-agent-availabilty-status'),
	path('api/create-third-party-token/',views.CreateThirdPartyToken.as_view(), name='create-third-party-token'),
	path('api/third-party-call/<str:token>/<int:contact>/',views.ThirdPartyCall.as_view(), name='third-party-user-list'),
	path('api/third-party-user-list/<str:token>/',views.ThirdPartyUserCampaignAPIView.as_view(), name='third-party-call'),
	path('api/third-party-upload-file/<str:token>/',views.UploadCsvThirdParty.as_view(), name='third-party-upload-file'),
	path('api/third-party-download-sample/<str:token>/',views.ThirdPartyCsvDownloadAPIView.as_view(), name='third-party-download-sample'),
	path('api/third-party-call-hangup/<str:token>/',views.HangUpThirdPartyCall.as_view(), name='third-party-call-hangup'),
	path('api/third-party-csv/',views.ThirdPartyCsvAPIView.as_view(), name='third-party-csv'),
	path('api/third-party-delete/<str:token>/<int:pk>/',views.ThirdPartyUserDeleteAPIView.as_view(), name='third-party-delete'),
	path('api/send_sms/',views.SendSMSApiView.as_view(), name='send_sms'),
	path('api/send_email/',views.SendEmailApiView.as_view(),name='send_email'),
	path('CampaignManagement/third-party-user-campaign/',views.ThirdPartyUserCampaignListAPIView.as_view(), name="third_party_user_campaign"),
	path('CampaignManagement/third-party-user-campaign/<int:pk>/',views.ThirdPartyUserCampaignListEditAPIView.as_view(), name="edit-third_party_user_campaign"),
	path('SMSManagement/gateway-settings/',views.SMSGatewayView.as_view(), name='gateway_settings'),
	path('SMSManagement/sms-template/',views.SMSTemplateView.as_view(), name='sms_template'),
	path('SMSManagement/Sms-Template/create/',
		 views.SmsTemplateCreateEditApiView.as_view(), name="create-sms_template"),
	path('SMSManagement/Sms-Template/edit/<int:pk>/',
		 views.SmsTemplateCreateEditApiView.as_view(), name="edit-sms_template"),
	path('SMSManagement/Sms-Template/get-crm-fields/',
		 views.SmsTemplateGetCrmFieldsApiView.as_view(), name="sms-get-crmfields"),
	path('SMSManagement/get-sample-template/<str:campaign>/<str:file_type>/',views.DownloadSampleSmsTemplate.as_view(), name="get-sample-sms-template"),
	path('SMSManagement/upload-sms-template/',
		 views.UploadSmsApiView.as_view(), name="upload-sms-template"),
	path('SMSManagement/Sms-Gateway/create/',
		 views.SmsGatewayCreateEditApiView.as_view(), name="create-gateway_settings"),
	path('SMSManagement/Sms-Gateway/edit/<int:pk>/',
		 views.SmsGatewayCreateEditApiView.as_view(), name="edit-gateway_settings"),
	path('CampaignManagement/third-party-api/',views.ThirdPartyAPIView.as_view(),name="thirdpartyapi"),
	path('CampaignManagement/third-party-api/create/',views.ThirdPartyCreateAPIView.as_view(),name="create-thirdpartyapi"),
	path('CampaignManagement/third-party-api/<int:pk>/',views.ThirdPartyEditAPIView.as_view(),name="edit-thirdpartyapi"),
	path('api/check-api-crm-campaings/',views.ApiCrmCampaings.as_view(),name="api-crm-campaings"),
	path('CampaignManagement/voiceblaster/',views.VoiceBlasterAPIView.as_view(),name="voiceblaster"),
	path('CampaignManagement/voiceblaster/create/',views.VoiceBlasterCreateAPIView.as_view(),name="create-voiceblaster"),
	path('CampaignManagement/voiceblaster/<int:pk>/',views.VoiceBlasterEditAPIView.as_view(),name="edit-voiceblaster"),
	path('api/download-certificate/',views.DownloadCertificateApiView.as_view(),name='download_certificate'),
	path('CampaignManagement/GetCamapignSwitchTrunk/',
		 views.GetCampaignSwitchTrunkView.as_view(), name="get-switch-trunk"),
	path('api/get-phonebook-details/',views.GetPhonebookDetailsApi.as_view(),name='phonebook_deails'),
	path('api/get-customer-details/',views.CustomerInfoInMessage.as_view(),name='msg_customer_info'),
	path('agentscreen/', views.SwitchingScreens.as_view(), name="agent-switchscreen"),
	path('api/get-agent-dispo-count/',views.GetAgentDispoCount.as_view(),name="get_agent_dispo_count"),
	path('Modules/report-scheduler/',views.ReportEmailSchedulerAPIView.as_view(),name="email_scheduler"),
	path('Modules/email-log/',views.EmailLogAPI.as_view(),name="email_log"),
	path('api/save-column-visibility/', views.SaveReportColumnVisibilityAPIView.as_view(),name='save-column-visibility'),
	path('api/download-scheduled-report/<str:token>/', views.DownloadScheduledReportAPIView.as_view(),name='download-scheduled-report'),
	path('EmailManagement/EmailGateway/create/', views.EmailGatewayCreateEditApiView.as_view(), name="create-email_gateway"),
	path('EmailManagement/EmailGateway/edit/<int:pk>/', views.EmailGatewayCreateEditApiView.as_view(), name="edit-email_gateway"),
	path('EmailManagement/EmailGateway/', views.EmailGatewayView.as_view(), name="email_gateway"),
	path('EmailManagement/EmailTemplate/', views.EmailTemplateListApiView.as_view(), name="email_template"),
	path('EmailManagement/EmailTemplate/create/', views.EmailTemplateCreateEditApiView.as_view(), name="create-email_template"),
	path('EmailManagement/EmailTemplate/edit/<int:pk>/', views.EmailTemplateCreateEditApiView.as_view(), name="edit-email_template"),
	path('api/check-email-crm-fields/', views.EmailTemplateGetCrmFieldsApiView.as_view(), name="edit-email_crm_field"),
	path('api/get-userwisecampaign-leadlist/',views.UserWiseCampaignDataApi.as_view(), name='get-usercampaignwise-leadlist'),
	path('api/broadcast-usermessage/', views.BroadCastUserMessageApi.as_view(), name="broadcast_usermessage"),
	path('api/get-broadcastmessages/', views.GetBroadCastMessage.as_view(), name="get-broadcastmessages"),
	path('api/get-agent-breaks/', views.GetAgentBreakwisetotal.as_view(), name="get-breakwisetotal"),
	path('api/reset_trunk_channels_count/', views.ResetTrunkChannelCount.as_view(), name="reset_trunk_channels_count"),
	path('Administration/Holidays/',views.HolidaysApiView.as_view(),name='holidays'),
	path('Administration/Holidays/create/',views.CreateEditHolidaysApiView.as_view(),name='create-holidays'),
	path('Administration/Holidays/edit/<int:pk>/',views.CreateEditHolidaysApiView.as_view(),name='edit-holidays'),
	path('Administration/upload-holiday-list/',views.UploadHolidaysApiView.as_view(), name="upload-holiday-list"),
	path('api/send_dtmf/', views.SendDTMFAPIView.as_view(),name='send_dtmf'),
	path('CallReports/pending-contacts/',views.PendingContactAPIView.as_view(),name='pending_contacts'),
	path('CallReports/pending-contacts/<int:pk>/',views.PendingContactEditAPIView.as_view(),name='edit-pending_contacts'),
] + static(settings.RECORDING_URL, document_root=settings.RECORDING_ROOT)

