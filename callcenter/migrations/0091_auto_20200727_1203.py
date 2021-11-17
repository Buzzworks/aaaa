# Generated by Django 2.2 on 2020-07-27 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0090_diallereventlog_campaign_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stickyagent',
            name='campaign',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='callcenter.Campaign'),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.3.77', help_text='Server IP address', max_length=100),
        ),
    ]