# Generated by Django 4.2.2 on 2023-06-25 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_history', '0016_alter_video_top_comment_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['created_on'], 'verbose_name': 'Video'},
        ),
    ]
