# Generated by Django 2.2 on 2020-07-16 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0083_auto_20200624_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.3.80', help_text='Server IP address', max_length=100),
        ),
    ]
