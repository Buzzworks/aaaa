# Generated by Django 2.2 on 2019-09-16 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0004_auto_20190916_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.1.246', help_text='Server IP address', max_length=100),
        ),
    ]
