# Generated by Django 2.2 on 2022-08-24 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0137_auto_20220822_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialtrunk',
            name='did_regex',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
