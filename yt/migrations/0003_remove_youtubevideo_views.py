# Generated by Django 2.2.7 on 2019-12-21 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yt', '0002_youtubevideo_yt_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youtubevideo',
            name='views',
        ),
    ]
