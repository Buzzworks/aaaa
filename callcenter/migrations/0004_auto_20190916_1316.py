# Generated by Django 2.2 on 2019-09-16 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0003_auto_20190916_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callbackcontact',
            name='contact_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='calldetail',
            name='contact_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='cdrfeedbck',
            name='contact_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='currentcallback',
            name='contact_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='diallereventlog',
            name='contact_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='contact_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='snoozedcallback',
            name='contact_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
