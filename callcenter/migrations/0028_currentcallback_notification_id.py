# Generated by Django 2.2 on 2019-11-09 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0027_currentcallback_callbackcontact_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentcallback',
            name='notification_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
