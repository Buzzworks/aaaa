# Generated by Django 2.2 on 2020-03-02 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0026_merge_20200227_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='downloadreports',
            name='is_start',
            field=models.BooleanField(default=False),
        ),
    ]