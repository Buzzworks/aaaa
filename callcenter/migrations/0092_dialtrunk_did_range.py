# Generated by Django 2.2 on 2020-07-23 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0091_merge_20200723_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialtrunk',
            name='did_range',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
