# Generated by Django 2.2 on 2020-09-17 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0104_reportcolumnvisibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.0.102', help_text='Server IP address', max_length=100),
        ),
    ]
