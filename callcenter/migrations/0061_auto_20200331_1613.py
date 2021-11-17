# Generated by Django 2.2 on 2020-03-31 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0060_auto_20200328_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservariable',
            name='wfh_password',
            field=models.CharField(blank=True, help_text='wfh password', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='wfh_numeric',
            field=models.BigIntegerField(blank=True, default=None, help_text='wfh numeric', null=True, unique=True),
        ),
    ]