# Generated by Django 2.2 on 2022-08-22 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0136_merge_20220822_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calldetail',
            name='session_uuid',
            field=models.UUIDField(db_index=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='emailgateway',
            name='email_trigger_on',
            field=models.CharField(choices=[('0', 'On Pre-Call'), ('1', 'On Disposition'), ('2', 'On Call'), ('3', 'On Abandonded Call')], default='2', max_length=2),
        ),
        migrations.AlterField(
            model_name='smsgateway',
            name='sms_trigger_on',
            field=models.CharField(choices=[('0', 'On Pre-Call'), ('1', 'On Disposition'), ('2', 'On Call'), ('3', 'On Abandonded Call')], default='2', max_length=2),
        ),
    ]
