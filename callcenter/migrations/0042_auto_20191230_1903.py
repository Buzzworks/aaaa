# Generated by Django 2.2 on 2019-12-30 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0041_currentcallback_callmode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='css',
            name='name',
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.3.36', help_text='Server IP address', max_length=100),
        ),
    ]