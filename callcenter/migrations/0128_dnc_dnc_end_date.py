# Generated by Django 2.2 on 2022-05-05 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0127_auto_20220430_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='dnc',
            name='dnc_end_date',
            field=models.DateField(db_index=True, default=None, null=True),
        ),
    ]
