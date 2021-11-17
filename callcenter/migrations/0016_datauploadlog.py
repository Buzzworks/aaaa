# Generated by Django 2.2 on 2019-10-16 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0015_auto_20191010_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataUploadLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonebook', models.CharField(blank=True, max_length=100, null=True)),
                ('improper_file', models.FileField(blank=True, upload_to='upload')),
                ('completed_percentage', models.IntegerField(default='0')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('job_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]