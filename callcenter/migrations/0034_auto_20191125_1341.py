# Generated by Django 2.2 on 2019-11-25 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0033_auto_20191122_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='callback_threshold',
            field=models.IntegerField(blank=True, db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='inbound_threshold',
            field=models.IntegerField(blank=True, db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.3.35', help_text='Server IP address', max_length=100),
        ),
    ]
