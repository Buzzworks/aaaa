# Generated by Django 2.2 on 2020-03-28 18:08

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0059_auto_20200325_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='wfh_dispo',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='wfh_numeric',
            field=models.BigIntegerField(blank=True, default=None, help_text='sip extension', null=True, unique=True),
        ),
    ]
