# Generated by Django 2.2 on 2019-10-09 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20190916_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Auto-Dialed', 'Auto-Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abundant', 'Abundant'), ('INVALID_NUMBER', 'INVALID_NUMBER'), ('Agent-Answered', 'Agent-Answered'), ('Drop', 'Drop')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='tempcontactinfo',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Auto-Dialed', 'Auto-Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abundant', 'Abundant'), ('INVALID_NUMBER', 'INVALID_NUMBER'), ('Agent-Answered', 'Agent-Answered'), ('Drop', 'Drop')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='trashcontact',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Auto-Dialed', 'Auto-Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abundant', 'Abundant'), ('INVALID_NUMBER', 'INVALID_NUMBER'), ('Agent-Answered', 'Agent-Answered'), ('Drop', 'Drop')], db_index=True, default='NotDialed', max_length=15),
        ),
    ]