# Generated by Django 2.2 on 2019-11-09 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0025_auto_20191109_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='inbound_threshold',
            field=models.IntegerField(blank=True, db_index=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='callback_threshold',
            field=models.IntegerField(blank=True, db_index=True, default=1, null=True),
        ),
    ]
