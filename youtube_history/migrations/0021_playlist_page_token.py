# Generated by Django 4.2.2 on 2023-06-29 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_history', '0020_playlist_last_api_call'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='page_token',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
