# Generated by Django 2.2 on 2019-09-23 11:49

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0010_merge_20190923_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disposition',
            name='dispo_keys',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]
