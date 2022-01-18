from django.core.management.base import BaseCommand
from django.conf import settings
from callcenter.models import *
from datetime import time
from flexydial.constants import MODULE_LIST
import platform
import os
import getpass
import numpy as np

class Command(BaseCommand):

    help = "Dummy Fixture"

    # def add_arguments(self, parser):
    #    parser.add_argument('--verbose', action='store_true')

    def handle(self, **options):
        # delete existing disposition
        User.objects.filter(username="admin", is_superuser=True).delete()
        superuser = User.objects.create(username="admin", is_superuser=True)
        superuser.set_password("flexydial")
        superuser.save()
        UserVariable.objects.filter(user=superuser).delete()
        UserVariable.objects.create(user=superuser, extension="1000")
        admin_user = User.objects.filter(username="admin")
        if admin_user:
            admin_user = admin_user[0]
            Disposition.objects.all().delete()

            # default disposition
            Disposition.objects.bulk_create([Disposition(name='Dnc', dispos=[]), Disposition(name='Not Connected', dispos=[]), Disposition( name='Connected', dispos=[]), Disposition(name='Callback',dispos=[]), Disposition(name='Busy', dispos=[]), Disposition(name='Transfer', dispos=[])])
            Disposition.objects.all().update(created_by=admin_user, color_code="#3a3f51")

            # #delete all pausebreak
            PauseBreak.objects.all().delete()

            break_time = time(hour=0, minute=2, second=0)

            # #default pausebreak
            PauseBreak.objects.bulk_create([PauseBreak(name="Tea Break", created_by=admin_user), PauseBreak(name="Lunch Break", created_by=admin_user), PauseBreak(name="Breakfast Break", created_by=admin_user), PauseBreak(name="Meeting", created_by=admin_user), PauseBreak(name="Dinner Break", created_by=admin_user)])
            PauseBreak.objects.update(break_time=break_time)

            # #delete switch
            Switch.objects.all().delete()

            # #default switch
            Switch.objects.bulk_create([Switch(name="call_server", ip_address=settings.FREESWITCH_IP_ADDRESS, created_by=admin_user)])

            DialTrunk.objects.all().delete()
            camp_switch = Switch.objects.filter(name="call_server").first()
            # sofia string = sofia/external/${destination_number}@192.168.3.202
            DialTrunk.objects.create(name="carrier1", dial_string="sofia/external/${destination_number}@0.0.0.0", created_by=admin_user, channel_count=31, switch=camp_switch, prefix=False, did_range='0,0')

            # delete user role
            UserRole.objects.all().delete()

            # #default user role
            UserRole.objects.bulk_create([UserRole(name="agent", access_level="Agent", permissions={"dashboard":[],"users":[],"user_roles":[],"groups":[],"campaigns":[],"switch":[],"dialtrunks":[],"dialtrunk_group":[],"dispositions":[],"pause_breaks":[],"campaign_schedules":[],"scripts":[],"audio_files":[],"phonebook":[],"crm_fields":[],"contact_info":[],"dnc":[],"call_detail":[],"agent_activity":[],"agent_performance":[],"agent_mis":[],"campaign_mis":[],"campaign_performance":[],"call_recordings":[],"css":[],"relationtags":[],"lead_priority":[],"billing":[],"switchscreen":[]}),
                UserRole(name="admin", access_level="Admin", permissions={"dashboard":["R"],"users":["C","R","U","D"],"user_roles":["C","R","U","D"],"groups":["C","R","U","D"],"campaigns":["C","R","U","D"],"switch":["C","R","U","D"],"dialtrunks":["C","R","U","D"],"dialtrunk_group":["C","R","U","D"],"dispositions":["C","R","U","D"],"pause_breaks":["C","R","U","D"],"campaign_schedules":["C","R","U","D"],"scripts":["C","R","U","D"],"audio_files":["C","R","U","D"],"phonebook":["C","R","U","D"],"crm_fields":["C","R","U","D"],"contact_info":["R","U","D"],"dnc":["C","R","U","D"],"call_detail":["R"],"agent_activity":["R"],"agent_performance":["R"],"agent_mis":["R"],"campaign_mis":["R"],"campaign_performance":["R"],"call_recordings":["R"],"css":["C","R","U","D"],"relationtags":["C","R","U","D"],"lead_priority":["C","R","U","D"],"billing":["C","R","U","D"],'switchscreen':['R']}),
                UserRole(name="manager", access_level="Manager", permissions={"dashboard":["R"],"users":["C","R","U","D"], "user_roles":[],"groups":["C","R","U","D"],"campaigns":["C","R","U","D"],"switch":["C","R","U","D"], "dialtrunks":["C","R","U","D"],"dialtrunk_group":["C","R","U","D"],"dispositions":["C","R","U","D"],"pause_breaks":["C","R","U","D"],"campaign_schedules":["C","R","U","D"],"scripts":["C","R","U","D"],"audio_files":["C","R","U","D"],"phonebook":["C","R","U","D"],"crm_fields":["C","R","U","D"],"contact_info":["R","U","D"],"dnc":["C","R","U","D"],"agent_mis":["R"],"campaign_mis":["R"],"campaign_performance":["R"],"call_detail":["R"],"agent_activity":["R"],"agent_performance":["R"], "call_recordings":["R"],"css":["C","R","U","D"],"relationtags":["C","R","U","D"],"lead_priority":["C","R","U","D"],"billing":["C","R","U","D"],'switchscreen':['R']}),
                UserRole(name="supervisor", access_level="Supervisor", permissions={'css': [], 'dnc': [], 'users': [],'groups': [], 'report': [], 'switch': [], 'scripts': [], 'agent_mis': [],'campaign_performance':[],"campaign_mis":[],'campaigns': [],'dashboard': [],'phonebook': [], 'crm_fields': [], 'dialtrunks': [], 'dialtrunk_group': [], 'user_roles': [], 'audio_files': [], 'call_detail': [],'contact_info': [], 'dialler_logs': [], 'dispositions': [], 'pause_breaks': [], 'agent_activity': [],'call_recordings': [], 'agent_performance': [], 'campaign_schedules': [],"lead_priority":[],"billing":[],'switchscreen':['R']})])
            UserRole.objects.update(created_by=admin_user)

            # delete campaign
            Campaign.objects.all().delete()

            # default campaign
            #camp_caller_id = 68627702
            camp_dial_trunk = DialTrunk.objects.filter(name="carrier1")[0]
            camp_inst = Campaign.objects.create(name="test", slug="test", dial_method={"manual":True,"inbound":False,"outbound":"Predictive", "ibc_popup": False, "no_agent_audio": False, "sticky_agent_map": False}, created_by=admin_user, auto_feedback=True, auto_feedback_time="02:00")
            camp_inst.switch = camp_switch
            camp_inst.trunk = camp_dial_trunk
            camp_inst.trunk_did = {"did": ["0"], "did_end": "", "did_start": "", "type_of_did": "single"}
            camp_inst.all_caller_id = ["0"]
            camp_inst.disposition.add(*Disposition.objects.all())
            camp_inst.breaks.add(*PauseBreak.objects.all())
            camp_inst.save()
            camp_variable = CampaignVariable()
            camp_variable.extension = 100
            camp_variable.campaign = camp_inst
            camp_variable.save()

            # create test group
            Group.objects.all().delete()
            group = Group.objects.create(name="test_group", created_by=admin_user)

            camp_inst.group.add(group)
            camp_inst.save()

            User.objects.all().exclude(username="admin").delete()
            user_role = UserRole.objects.filter(access_level="Agent")[0]
            for index, element in enumerate(range(1001, 1006)):
                user = User.objects.create(username=element, user_role=user_role, created_by=admin_user)
                user.set_password("flexydial@4")
                user.group.add(group)
                user.save()
                user_variable = UserVariable()
                user_variable.user = user
                user_variable.extension = element
                user_variable.domain = camp_switch
                user_variable.save()

            # modules creation
            Modules.objects.all().delete()
            for module in MODULE_LIST:
                children = module['children']
                del module['children']
                parent = Modules.objects.create(**module)
                if children:
                    for child in children:
                        del child['children']
                        child['parent'] = parent
                        Modules.objects.create(**child)

            md_name = list(Modules.objects.filter().exclude(parent=None).values_list('name',flat=True))
            usr_role = UserRole.objects.all()
            for i in usr_role:
                for mod in md_name:
                    if mod not in i.permissions:
                        i.permissions.update({mod:[]})
                i.save()

            Daemons.objects.all().delete()
            
            print("*********************************************************")
            print("!!!!!!!!!!  DUMMY DATA CREATED SUCCEFULLY  !!!!!!!!!!")
            print("*********************************************************")


