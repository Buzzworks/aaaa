# Generated by Django 2.2 on 2020-05-29 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0028_auto_20200416_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadlistpriority',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.CampaignInfo'),
        ),
    ]
