# Generated by Django 2.2.5 on 2019-09-29 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20190929_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='remote_channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.TwitchIrcChannel'),
        ),
    ]
