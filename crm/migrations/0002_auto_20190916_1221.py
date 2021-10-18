# Generated by Django 2.2 on 2019-09-16 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followupcontact',
            name='phonebook',
        ),
        migrations.RemoveField(
            model_name='followupcontact',
            name='site',
        ),
        migrations.RemoveField(
            model_name='snoozedfollowup',
            name='site',
        ),
        migrations.AlterField(
            model_name='contact',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Auto-Dialed', 'Auto-Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Missedcall', 'Missedcall'), ('INVALID_NUMBER', 'INVALID_NUMBER'), ('Agent-Answered', 'Agent-Answered'), ('Drop', 'Drop')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='tempcontactinfo',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Auto-Dialed', 'Auto-Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Missedcall', 'Missedcall'), ('INVALID_NUMBER', 'INVALID_NUMBER'), ('Agent-Answered', 'Agent-Answered'), ('Drop', 'Drop')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='trashcontact',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Auto-Dialed', 'Auto-Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Missedcall', 'Missedcall'), ('INVALID_NUMBER', 'INVALID_NUMBER'), ('Agent-Answered', 'Agent-Answered'), ('Drop', 'Drop')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.DeleteModel(
            name='CurrentFollowUp',
        ),
        migrations.DeleteModel(
            name='FollowUpContact',
        ),
        migrations.DeleteModel(
            name='SnoozedFollowup',
        ),
    ]
