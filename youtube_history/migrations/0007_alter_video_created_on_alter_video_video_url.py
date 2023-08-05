# Generated by Django 4.2.2 on 2023-06-16 20:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_history', '0006_alter_playlist_options_alter_video_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_url',
            field=models.URLField(),
        ),
    ]
