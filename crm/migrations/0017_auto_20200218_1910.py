# Generated by Django 2.2 on 2020-02-18 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0016_leadlistpriority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='priority',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='leadlistpriority',
            name='priority',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='phonebook',
            name='caller_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='phonebook',
            name='priority',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tempcontactinfo',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
