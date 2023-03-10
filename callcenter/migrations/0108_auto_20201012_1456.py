# Generated by Django 2.2 on 2020-10-12 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0107_merge_20200924_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportcolumnvisibility',
            name='report_name',
            field=models.CharField(choices=[('1', 'call_detail'), ('2', 'call_recording'), ('3', 'agent_performance'), ('4', 'agent_mis'), ('5', 'agent_activity'), ('6', 'campaign_mis'), ('7', 'campaign_performance'), ('8', 'callback_call'), ('9', 'abandoned_call'), ('10', 'contact_info'), ('11', 'billing'), ('12', 'admin_log'), ('13', 'call_recording_feedback')], default='1', max_length=2),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_switch', to='callcenter.Switch'),
        ),
    ]
