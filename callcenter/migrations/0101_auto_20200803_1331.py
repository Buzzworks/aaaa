# Generated by Django 2.2 on 2020-08-03 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0100_auto_20200731_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilledrouting',
            name='skill_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.0.102', help_text='Server IP address', max_length=100),
        ),
    ]
