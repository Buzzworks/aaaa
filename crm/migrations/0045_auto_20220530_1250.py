# Generated by Django 2.2 on 2022-05-30 12:50

import crm.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0044_auto_20210322_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonebook',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], db_index=True, default='Active', max_length=10),
        ),
        migrations.AlterField(
            model_name='phonebookupload',
            name='phonebook_file',
            field=crm.models.FIleModelField(blank=True, upload_to='upload'),
        ),
    ]
