# Generated by Django 2.2 on 2022-06-29 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0130_auto_20220530_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='thirdpartyapidisposition',
            name='callid',
            field=models.CharField(default='', max_length=100),
        ),
    ]
