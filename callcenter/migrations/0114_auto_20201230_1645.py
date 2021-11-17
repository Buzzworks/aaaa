# Generated by Django 2.2 on 2020-12-30 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0113_auto_20201116_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='modules',
            name='icon',
            field=models.CharField(default='fa-file-contract', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='modules',
            name='is_menu',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='modules',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent_menu', to='callcenter.Modules'),
        ),
        migrations.AddField(
            model_name='modules',
            name='sequence',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='modules',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=10),
        ),
        migrations.AddField(
            model_name='modules',
            name='title',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='modules',
            name='url_abbr',
            field=models.CharField(default='', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='modules',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]