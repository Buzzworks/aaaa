# Generated by Django 2.2 on 2022-10-12 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0052_auto_20220827_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandonedcall', 'Abandonedcall'), ('Drop', 'Drop'), ('Dnc', 'Dnc'), ('NC', 'NC'), ('Invalid Number', 'Invalid Number'), ('CBR', 'CBR'), ('Queued-Abandonedcall', 'Queued-Abandonedcall'), ('Queued-Callback', 'Queued-Callback'), ('Dialed-Queued', 'Dialed-Queued'), ('AutoFeedback', 'AutoFeedback'), ('AutoWrapUp', 'AutoWrapUp')], db_index=True, default='NotDialed', max_length=30),
        ),
        migrations.AlterField(
            model_name='tempcontactinfo',
            name='contact',
            field=models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Contact'),
        ),
        migrations.AlterField(
            model_name='tempcontactinfo',
            name='previous_status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandonedcall', 'Abandonedcall'), ('Drop', 'Drop'), ('Dnc', 'Dnc'), ('NC', 'NC'), ('Invalid Number', 'Invalid Number'), ('CBR', 'CBR'), ('Queued-Abandonedcall', 'Queued-Abandonedcall'), ('Queued-Callback', 'Queued-Callback'), ('Dialed-Queued', 'Dialed-Queued'), ('AutoFeedback', 'AutoFeedback'), ('AutoWrapUp', 'AutoWrapUp')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='tempcontactinfo',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandonedcall', 'Abandonedcall'), ('Drop', 'Drop'), ('Dnc', 'Dnc'), ('NC', 'NC'), ('Invalid Number', 'Invalid Number'), ('CBR', 'CBR'), ('Queued-Abandonedcall', 'Queued-Abandonedcall'), ('Queued-Callback', 'Queued-Callback'), ('Dialed-Queued', 'Dialed-Queued'), ('AutoFeedback', 'AutoFeedback'), ('AutoWrapUp', 'AutoWrapUp')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='trashcontact',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abandonedcall', 'Abandonedcall'), ('Drop', 'Drop'), ('Dnc', 'Dnc'), ('NC', 'NC'), ('Invalid Number', 'Invalid Number'), ('CBR', 'CBR'), ('Queued-Abandonedcall', 'Queued-Abandonedcall'), ('Queued-Callback', 'Queued-Callback'), ('Dialed-Queued', 'Dialed-Queued'), ('AutoFeedback', 'AutoFeedback'), ('AutoWrapUp', 'AutoWrapUp')], db_index=True, default='NotDialed', max_length=30),
        ),
    ]
