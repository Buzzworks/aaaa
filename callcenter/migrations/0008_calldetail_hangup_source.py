# Generated by Django 2.2 on 2019-09-20 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0007_auto_20190919_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='calldetail',
            name='hangup_source',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
