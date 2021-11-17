# Generated by Django 2.2 on 2019-11-01 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20191101_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempcontactinfo',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Auto-Dialed', 'Auto-Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandoned', 'Abandoned'), ('INVALID_NUMBER', 'INVALID_NUMBER'), ('Agent-Answered', 'Agent-Answered'), ('Drop', 'Drop')], db_index=True, default='NotDialed', max_length=15),
        ),
    ]