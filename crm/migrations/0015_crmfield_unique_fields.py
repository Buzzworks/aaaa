# Generated by Django 2.2 on 2020-02-17 17:13

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0014_auto_20200123_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='crmfield',
            name='unique_fields',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
