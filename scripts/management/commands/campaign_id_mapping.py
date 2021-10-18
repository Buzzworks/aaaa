from django.core.management.base import BaseCommand
from crm.models import *
from callcenter.models import *

class Command(BaseCommand):

    help = "Update campaign name to campaign id"

    def handle(self, **options):
        campaigns = Campaign.objects.filter().values('id','name')
        CampaignInfo.objects.all().delete()
        for camp_id in campaigns:
        	CampaignInfo.objects.create(id=camp_id['id'], name=camp_id['name'])

        ex_camp = list(Campaign.objects.filter().values_list('name',flat=True))
        CSS.objects.exclude(campaign__in=ex_camp).update(campaign=None)
        CallBackContact.objects.exclude(campaign__in=ex_camp).update(campaign=None)
        CurrentCallBack.objects.exclude(campaign__in=ex_camp).update(campaign=None)
        Abandonedcall.objects.exclude(campaign__in=ex_camp).update(campaign=None)
        Notification.objects.exclude(campaign__in=ex_camp).update(campaign=None)
        SkilledRouting.objects.filter(d_abandoned_camp__in=ex_camp).update(d_abandoned_camp=None)
        Contact.objects.exclude(campaign__in=ex_camp).update(campaign=None)
        TempContactInfo.objects.exclude(campaign__in=ex_camp).update(campaign=None)
        for camp in campaigns:
            CSS.objects.filter(campaign=camp['name']).update(campaign=camp['id'])
            CallBackContact.objects.filter(campaign=camp['name']).update(campaign=camp['id'])
            CurrentCallBack.objects.filter(campaign=camp['name']).update(campaign=camp['id'])
            Abandonedcall.objects.filter(campaign=camp['name']).update(campaign=camp['id'])
            Notification.objects.filter(campaign=camp['name']).update(campaign=camp['id'])
            SkilledRouting.objects.filter(d_abandoned_camp=camp['name']).update(d_abandoned_camp=camp['id'])
            Contact.objects.filter(campaign=camp['name']).update(campaign=camp['id'])
            TempContactInfo.objects.filter(campaign=camp['name']).update(campaign=camp['id'])
        skill_route = SkilledRouting.objects.all()
        campaigns = list(Campaign.objects.filter().values_list('name',flat=True))

        for skill in skill_route:
            temp = {}
            for label,value in skill.skills.items():
                camp = Campaign.objects.filter(name=value)
                if camp.exists():
                    temp[label] = camp.first().id
                else:
                    temp[label] = value
            skill.skills = temp
            skill.save()

        print("*********************************************************")