# Generated by Django 2.2 on 2020-09-02 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0036_tempcontactinfo_previous_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='crmfield',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], db_index=True, default='Active', max_length=10),
        ),
    ]
