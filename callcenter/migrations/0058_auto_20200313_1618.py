# Generated by Django 2.2 on 2020-03-13 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0057_auto_20200305_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.3.64', help_text='Server IP address', max_length=100),
        ),
    ]
