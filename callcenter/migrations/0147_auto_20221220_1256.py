# Generated by Django 2.2 on 2022-12-20 12:56

import callcenter.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0146_auto_20221220_1102'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='diallereventlog',
            name='recording_file',
            field=models.FileField(blank=True, storage=callcenter.models.GCPCustomBucketSelection(), upload_to=callcenter.models.get_upload_path),
        ),
    ]
