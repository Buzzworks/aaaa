# Generated by Django 2.2 on 2020-04-15 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0069_thirdpartyapiusertoken_is_live'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thirdpartyapiusertoken',
            name='is_live',
        ),
    ]
