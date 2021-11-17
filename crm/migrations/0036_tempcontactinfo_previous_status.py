# Generated by Django 2.2 on 2020-08-27 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0035_leadbucket_reverify_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempcontactinfo',
            name='previous_status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandonedcall', 'Abandonedcall'), ('Drop', 'Drop'), ('Dnc', 'Dnc'), ('NC', 'NC'), ('Invalid Number', 'Invalid Number'), ('CBR', 'CBR'), ('Queued-Abandonedcall', 'Queued-Abandonedcall'), ('Queued-Callback', 'Queued-Callback'), ('Dialed-Queued', 'Dialed-Queued')], db_index=True, default='NotDialed', max_length=15),
        ),
    ]