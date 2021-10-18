# Generated by Django 2.2 on 2020-01-13 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0044_merge_20200108_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abandonedcall',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandonedcall', 'Abandonedcall'), ('Drop', 'Drop'), ('Dnc', 'Dnc'), ('NC', 'NC'), ('Invalid Number', 'Invalid Number'), ('AbandonedCallback', 'AbandonedCallback'), ('Queued-Abandonedcall', 'Queued-Abandonedcall'), ('Queued-Callback', 'Queued-Callback')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='callbackcontact',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandonedcall', 'Abandonedcall'), ('Drop', 'Drop'), ('Dnc', 'Dnc'), ('NC', 'NC'), ('Invalid Number', 'Invalid Number'), ('AbandonedCallback', 'AbandonedCallback'), ('Queued-Abandonedcall', 'Queued-Abandonedcall'), ('Queued-Callback', 'Queued-Callback')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='currentcallback',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandonedcall', 'Abandonedcall'), ('Drop', 'Drop'), ('Dnc', 'Dnc'), ('NC', 'NC'), ('Invalid Number', 'Invalid Number'), ('AbandonedCallback', 'AbandonedCallback'), ('Queued-Abandonedcall', 'Queued-Abandonedcall'), ('Queued-Callback', 'Queued-Callback')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='disposition',
            name='name',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.3.37', help_text='Server IP address', max_length=100),
        ),
    ]
