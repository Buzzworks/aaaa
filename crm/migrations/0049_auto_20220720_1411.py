# Generated by Django 2.2 on 2022-07-20 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0048_auto_20220719_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='last_connected_user',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='priority',
            field=models.IntegerField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='uniqueid',
            field=models.CharField(blank=True, db_index=True, max_length=30, null=True),
        ),
    ]
