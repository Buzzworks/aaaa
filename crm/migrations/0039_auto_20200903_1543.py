# Generated by Django 2.2 on 2020-09-03 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0038_leadlistpriority_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crmfield',
            name='status',
        ),
        migrations.RemoveField(
            model_name='leadlistpriority',
            name='status',
        ),
    ]
