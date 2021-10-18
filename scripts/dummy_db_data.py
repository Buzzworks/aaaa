from callcenter.models import *

#create disposition instance
Disposition.objects.create(name="No feedback", sub_dispos={})

#create calltime instance
CampaignSchedule.objects.create(name="morning", comment="", schedule_time={})

#create server instance
Switch.objects.create(name="local server", ip_address="192.168.3.151")
Switch.objects.create(name="private server", ip_address="192.168.3.167")

#create carrier instance
DialTrunk.objects.create(name="first carrier", switch_id=1)
DialTrunk.objects.create(name="second carrier", switch_id=2)

#create department instance
Department.objects.create(name="solution", dept_extension="101")
Department.objects.create(name="IT", dept_extension="102")

#create break instance

Break.objects.create(name="Lunch Break")
Break.objects.create(name="Tea Break")

#create acces level
UserRole.objects.create(role_name="agent", permissions={})

#create phonebook instance
Phonebook.objects.create(name="first_phonebook", slug="first_phonebook", comment="dummy data")

#create scripts data
Contact.objects.create(numeric="9773249208", first_name="yamini", last_name="parab", email="yamini@gmail.com")
Contact.objects.create(numeric="9773249207", first_name="teju", last_name="parab", email="teju@gmail.com")

#create user role
UserRole.objects.create(name="Agent", access_level="Agent")
UserRole.objects.create(name="Manager", access_level="Manager")
UserRole.objects.create(name="Admin", access_level="Admin")

#create Modules
Modules.objects.bulk_create([
	Modules(name='dashboard', permissions='R'),Modules(name='users'),Modules(name='user_roles'),
	Modules(name='groups'),Modules(name='campaigns'),Modules(name='switch'),Modules(name='dialtrunks'),
	Modules(name='dispositions'),Modules(name='pause_breaks'),Modules(name='campaign_schedules'),
	Modules(name='scripts'),Modules(name='audio_files'),Modules(name='phonebook'),Modules(name='crm_fields'),Modules(name='dialler_logs'),
	Modules(name='report'),Modules(name='contact_info')
	])
	init_time = cdr[0].init_time
	ring_time = cdr[0].ring_time
	connect_time = cdr[0].connect_time
	wait_time = cdr[0].wait_time
	hold_time = cdr[0].hold_time
	media_time = cdr[0].media_time
	transfer_history = cdr[0].transfer_history
	call_duration = cdr[0].call_duration
	bill_sec = cdr[0].bill_sec
	hangup_time = cdr[0].hangup_time
	dialed_status = cdr[0].dialed_status
	hangup_cause = cdr[0].hangup_cause
	hangup_cause_code = cdr[0].hangup_cause_code
	channel = cdr[0].channel
	info = cdr[0].info
