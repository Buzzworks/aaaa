# Generated by Django 2.2 on 2020-07-27 17:56

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0093_auto_20200724_1856'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dialtrunkpriority',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='dialtrunkpriority',
            name='type_of_did',
        ),
        migrations.AlterField(
            model_name='dialtrunkpriority',
            name='did',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.0.102', help_text='Server IP address', max_length=100),
        ),
    ]
