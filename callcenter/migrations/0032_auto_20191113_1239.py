# Generated by Django 2.2 on 2019-11-13 12:39

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0031_merge_20191113_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilledrouting',
            name='audio',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='skilledrouting',
            name='skills',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
