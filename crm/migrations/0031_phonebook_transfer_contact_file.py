# Generated by Django 2.2 on 2020-06-23 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0030_auto_20200616_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonebook',
            name='transfer_contact_file',
            field=models.FileField(blank=True, upload_to='upload'),
        ),
    ]