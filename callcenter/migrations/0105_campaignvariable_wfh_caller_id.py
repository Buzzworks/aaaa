# Generated by Django 2.2 on 2020-08-07 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0104_merge_20200806_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignvariable',
            name='wfh_caller_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]