# Generated by Django 2.2 on 2020-03-31 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0061_auto_20200331_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='wfh_request_call',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
