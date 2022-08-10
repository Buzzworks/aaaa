from django.core.management.base import BaseCommand
from callcenter.models import CallDetail
from django.db.models import Count

class Command(BaseCommand):
    help = "Delete duplicate calldetails"
    def handle(self, **options):
        try:
            qs = CallDetail.objects.all()
            for i in qs:
                calldt = qs.filter(session_uuid = i.session_uuid).order_by("id")
                if calldt.count() > 1:
                    req_ids = list(calldt.values_list("id",flat=True))[1:]
                    CallDetail.objects.filter(id__in=req_ids).delete()
            print("++++++ DUPLICATED RECORDS DELETED SUCCESSFULLY ++++++++++")
        except Exception as e:
            print("Exception while deleting duplicates ",e)