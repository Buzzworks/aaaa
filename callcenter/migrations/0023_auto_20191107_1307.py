# Generated by Django 2.2 on 2019-11-07 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0022_merge_20191105_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='callback_threshold',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.3.35', help_text='Server IP address', max_length=100),
        ),
    ]