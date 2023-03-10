# Generated by Django 2.2 on 2022-05-09 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0128_dnc_dnc_end_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThirdPartyApiDisposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(default='', max_length=50)),
                ('disposition', models.CharField(default='', max_length=100)),
                ('subdisposition', models.CharField(default='', max_length=100)),
                ('callback', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='api_disposition',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
