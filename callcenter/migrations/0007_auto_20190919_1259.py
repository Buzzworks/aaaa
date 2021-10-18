# Generated by Django 2.2 on 2019-09-19 12:59

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0006_merge_20190918_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='disposition',
            name='dispo_keys',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.3.52', help_text='Server IP address', max_length=100),
        ),
    ]
