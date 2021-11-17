# Generated by Django 2.2 on 2020-05-28 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0079_merge_20200528_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsgateway',
            name='sms_trigger_on',
            field=models.CharField(choices=[('0', 'On Pre-Call'), ('1', 'On Disposition'), ('2', 'On Call')], default='2', max_length=2),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.3.77', help_text='Server IP address', max_length=100),
        ),
    ]