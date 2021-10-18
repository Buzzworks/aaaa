# Generated by Django 2.2 on 2020-04-20 18:56

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0070_remove_thirdpartyapiusertoken_is_live'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='vb_audio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='voice_blaster_audio', to='callcenter.AudioFile'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='vb_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='campaign',
            name='vb_mode',
            field=models.CharField(choices=[('0', 'Audio File'), ('1', 'TTS(Text to speech)')], db_index=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='voice_blaster',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='uservariable',
            name='domain',
            field=models.CharField(default='192.168.0.109', help_text='Server IP address', max_length=100),
        ),
    ]
