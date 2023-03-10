# Generated by Django 2.2 on 2019-09-25 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0011_auto_20190923_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.3.35', help_text='Server IP address', max_length=100),
        ),
    ]
