from django.core.management.base import BaseCommand
from django.conf import settings 
from callcenter.models import * 

class Command(BaseCommand):

	help = "Update switch screen modules"

	def handle(self, **options):
		md_name = list(Modules.objects.filter().values_list('name',flat=True))
		if 'qc_feedback' not in md_name:
			update_qc_feedback = {'qc_feedback':[]}
			Modules.objects.create(name='qc_feedback',permissions='C')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_qc_feedback)
				i.save()
		else:
			print("qc_feedback Module already present")

		if 'management_performance' not in md_name:
			permission_dict = {'management_performance':[]}
			Modules.objects.create(name='management_performance',permissions='R')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(permission_dict)
				i.save()
		else:
			print("call_recording_feedback Module already present")
		
		if 'call_recording_feedback' not in md_name:
			call_recording_feedback = {'call_recording_feedback':[]}
			Modules.objects.create(name='call_recording_feedback',permissions='R')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(call_recording_feedback)
				i.save()
		else:
			print("call_recording_feedback Module already present")

		if 'sms_template' not in md_name:
			update_screen = {'sms_template':[]}
			Modules.objects.create(name='sms_template',permissions='C,R,U,D')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_screen)
				i.save()
		else:
			print("sms_template Module already present")

		if 'gateway_settings' not in md_name:
			update_screen = {'gateway_settings':[]}
			Modules.objects.create(name='gateway_settings',permissions='C,R,U,D')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_screen)
				i.save()
		else:
			print("gateway_settings Module already present")

		if 'thirdpartyapi' not in md_name:
			update_screen = {'thirdpartyapi':[]}
			Modules.objects.create(name='thirdpartyapi',permissions='C,R,U,D')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_screen)
				i.save()
		else:
			print("thirdpartyapi Module already present")

		if 'third_party_user_campaign' not in md_name:
			update_screen = {'third_party_user_campaign':[]}
			Modules.objects.create(name='third_party_user_campaign',permissions='C,R,U,D')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_screen)
				i.save()
		else:
			print("third_party_user_campaign Module already present")

		if 'voiceblaster' not in md_name:
			update_screen = {'voiceblaster':[]}
			Modules.objects.create(name='voiceblaster',permissions='C,R,U,D')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_screen)
				i.save()
		else:
			print("voiceblaster Module already present")

		if 'email_scheduler' not in md_name:
			update_screen = {'email_scheduler':[]}
			Modules.objects.create(name='email_scheduler',permissions='C,R,U,D')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_screen)
				i.save()
		else:
			print("email_scheduler Module already present")

		if 'emaillog' not in md_name:
			update_screen = {'emaillog':[]}
			Modules.objects.create(name='emaillog',permissions='R')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_screen)
				i.save()
		else:
			print("emaillog Module already present")

		if 'email_gateway' not in md_name:
			permission_dict = {'email_gateway':[]}
			Modules.objects.create(name='email_gateway',permissions='C,R,U,D')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(permission_dict)
				i.save()
		else:
			print("email_gateway Module already present")

		if 'email_template' not in md_name:
			permission_dict = {'email_feedback':[]}
			Modules.objects.create(name='email_template',permissions='C,R,U,D')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(permission_dict)
				i.save()
		else:
			print("email_template Module already present")
		
		if 'switchscreen' not in md_name:
			update_screen = {'switchscreen':[]}
			Modules.objects.create(name='switchscreen',permissions='R')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_screen)
				i.save()
		else:
			print("switchscreen Module is present")

		if 'system_boot_action' not in md_name:
			update_screen = {'system_boot_action':[]}
			Modules.objects.create(name='system_boot_action',permissions='R')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_screen)
				i.save()
		else:
			print("system_boot_action Module is present")

		if 'lan' not in md_name:
			update_screen = {'lan':[]}
			Modules.objects.create(name='lan',permissions='R')
			usr_role = UserRole.objects.all()
			for i in usr_role:
				i.permissions.update(update_screen)
				i.save()
		else:
			print("Lan Report Module is present")
		print("********************************************************************")
		print("!!!!!!!!!!  Module and UserRole Updated with qc feedback !!!!!!!!!!")
		print("********************************************************************")
