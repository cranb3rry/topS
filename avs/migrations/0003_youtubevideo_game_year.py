# Generated by Django 2.2.7 on 2019-12-22 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avs', '0002_auto_20191222_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='game_year',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
