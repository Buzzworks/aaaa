# Generated by Django 2.2 on 2019-12-16 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20191115_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandonedcall', 'Abandonedcall'), ('Drop', 'Drop'), ('Dnc', 'Dnc'), ('NC', 'NC'), ('Invalid Number', 'Invalid Number')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='tempcontactinfo',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandonedcall', 'Abandonedcall'), ('Drop', 'Drop'), ('Dnc', 'Dnc'), ('NC', 'NC'), ('Invalid Number', 'Invalid Number')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='trashcontact',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandonedcall', 'Abandonedcall'), ('Drop', 'Drop'), ('Dnc', 'Dnc'), ('NC', 'NC'), ('Invalid Number', 'Invalid Number')], db_index=True, default='NotDialed', max_length=15),
        ),
    ]
