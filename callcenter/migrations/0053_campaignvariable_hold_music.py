# Generated by Django 2.2 on 2020-02-18 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0052_auto_20200130_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignvariable',
            name='hold_music',
            field=models.ForeignKey(blank=True, help_text='The system will play this when you putcalls on hold', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hold_music', to='callcenter.AudioFile'),
        ),
    ]
