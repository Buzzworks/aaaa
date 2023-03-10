# Generated by Django 2.2 on 2022-12-14 15:45

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0142_auto_20221214_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucketcredentials',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bucketcredentials',
            name='created_by',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='bucketcredentials',
            name='storage_bucket_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bucketcredentials',
            name='storage_credentials',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, help_text='\nIf storage type is GCP Simply copy the content in credentials.json file and paste in this field <br>\nor <br>\nIf the storage type is AWS then enter your credentials in the below mentioned format <br>\n<div class=\'\' style=\'background: #d0dfd6;margin-left: 40px;margin-right: 150px;\'>\n\t<p style=\'padding: 20px 0px 20px 00px;color:blueviolet\'>\n\t\t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  { <br>\t\n\t\t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      "AWS_ACCESS_KEY_ID" &nbsp;:&nbsp; "<-------access key id-------------->", <br>\n\t\t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      "AWS_SECRET_ACCESS_KEY" &nbsp;:&nbsp; "<-----------secret key---------------------->", <br>\n\t\t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      "AWS_STORAGE_BUCKET_NAME" &nbsp;:&nbsp; "<---------bucket name--------------------->"<br>\n\t\t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; } <br>\n\t<p>\n<div>\n'),
        ),
        migrations.AlterField(
            model_name='bucketcredentials',
            name='storage_type',
            field=models.CharField(choices=[('GCP', 'GCP'), ('AWS', 'AWS')], default=django.utils.timezone.now, max_length=30),
            preserve_default=False,
        ),
    ]
