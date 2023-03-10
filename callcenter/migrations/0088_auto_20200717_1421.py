# Generated by Django 2.2 on 2020-07-17 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0087_merge_20200716_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='dnc',
            name='uniqueid',
            field=models.CharField(default=None, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='calldetail',
            name='uniqueid',
            field=models.CharField(default=None, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.0.101', help_text='Server IP address', max_length=100),
        ),
    ]
