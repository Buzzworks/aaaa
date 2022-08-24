# Generated by Django 2.2 on 2022-07-25 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0133_auto_20220721_0500'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='whatsapp_gateway',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='whatsapp_campaign', to='callcenter.SMSGateway'),
        ),
    ]
