# Generated by Django 2.2 on 2019-10-09 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('callcenter', '0012_auto_20190925_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abundantcall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.CharField(max_length=100, null=True)),
                ('caller_id', models.CharField(max_length=100, null=True)),
                ('numeric', models.CharField(db_index=True, default='', max_length=50, null=True)),
                ('status', models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Auto-Dialed', 'Auto-Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abundant', 'Abundant'), ('INVALID_NUMBER', 'INVALID_NUMBER'), ('Agent-Answered', 'Agent-Answered'), ('Drop', 'Drop')], db_index=True, default='NotDialed', max_length=15)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('site', models.ForeignKey(default=1, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.AlterField(
            model_name='callbackcontact',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Auto-Dialed', 'Auto-Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abundant', 'Abundant'), ('INVALID_NUMBER', 'INVALID_NUMBER'), ('Agent-Answered', 'Agent-Answered'), ('Drop', 'Drop')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='calldetail',
            name='dialed_status',
            field=models.CharField(choices=[('Connected', 'Connected'), ('Drop', 'Drop'), ('Abundant', 'Abundant'), ('Auto-Dialed', 'Auto-Dialed'), ('Dialed', 'Dialed'), ('Agent-Answered', 'Agent-Answered'), ('INVALID_NUMBER', 'INVALID_NUMBER')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='currentcallback',
            name='status',
            field=models.CharField(choices=[('NotDialed', 'NotDialed'), ('Queued', 'Queued'), ('Dialed', 'Dialed'), ('Auto-Dialed', 'Auto-Dialed'), ('Locked', 'Locked'), ('NDNC', 'NDNC'), ('Callback', 'Callback'), ('Snoozed', 'Snoozed'), ('Abundant', 'Abundant'), ('INVALID_NUMBER', 'INVALID_NUMBER'), ('Agent-Answered', 'Agent-Answered'), ('Drop', 'Drop')], db_index=True, default='NotDialed', max_length=15),
        ),
        migrations.AlterField(
            model_name='diallereventlog',
            name='dialed_status',
            field=models.CharField(choices=[('Connected', 'Connected'), ('Drop', 'Drop'), ('Abundant', 'Abundant'), ('Auto-Dialed', 'Auto-Dialed'), ('Dialed', 'Dialed'), ('Agent-Answered', 'Agent-Answered'), ('INVALID_NUMBER', 'INVALID_NUMBER')], default='', max_length=50),
        ),
        migrations.DeleteModel(
            name='Missedcall',
        ),
    ]
