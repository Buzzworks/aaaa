# Generated by Django 2.2 on 2019-09-11 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0003_auto_20190911_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentactivity',
            name='inbound_time',
            field=models.TimeField(blank=True, default=datetime.time(0, 0), null=True),
        ),
        migrations.AddField(
            model_name='agentactivity',
            name='inbound_wait_time',
            field=models.TimeField(blank=True, default=datetime.time(0, 0), null=True),
        ),
    ]
