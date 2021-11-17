# Generated by Django 2.2 on 2020-02-27 15:31

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('crm', '0023_auto_20200220_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadReports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.CharField(blank=True, max_length=100, null=True)),
                ('serializers', models.CharField(blank=True, max_length=100, null=True)),
                ('col_list', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('filters', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('arguments', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('user', models.IntegerField(blank=True, default=None, null=True)),
                ('status', models.BooleanField(default=False)),
                ('view', models.BooleanField(default=False)),
                ('downloaded_file', models.FileField(blank=True, help_text='Click to downlad file', upload_to='download')),
                ('start_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('end_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('site', models.ForeignKey(default=1, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sites.Site')),
            ],
        ),
    ]