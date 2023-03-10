# Generated by Django 2.2 on 2020-11-09 21:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0109_merge_20201109_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminlogentry',
            name='event_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='adminlogentry',
            name='login_duration',
            field=models.TimeField(blank=True, default=datetime.time(0, 0), null=True),
        ),
        migrations.AlterField(
            model_name='reportcolumnvisibility',
            name='report_name',
            field=models.CharField(choices=[('1', 'call_detail'), ('2', 'call_recording'), ('3', 'agent_performance'), ('4', 'agent_mis'), ('5', 'agent_activity'), ('6', 'campaign_mis'), ('7', 'campaign_performance'), ('8', 'callback_call'), ('9', 'abandoned_call'), ('10', 'contact_info'), ('11', 'billing'), ('12', 'admin_log'), ('13', 'call_recording_feedback'), ('14', 'management_performace')], default='1', max_length=2),
        ),
    ]
