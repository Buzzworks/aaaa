# Generated by Django 2.2 on 2020-04-16 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0027_downloadreports_is_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadlistpriority',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.CampaignInfo'),
        ),
        migrations.AddField(
            model_name='leadlistpriority',
            name='is_global',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='leadlistpriority',
            name='uniqueid',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterUniqueTogether(
            name='leadlistpriority',
            unique_together={('uniqueid', 'campaign')},
        ),
    ]
