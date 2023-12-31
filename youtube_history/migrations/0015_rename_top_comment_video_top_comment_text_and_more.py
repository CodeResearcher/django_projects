# Generated by Django 4.2.2 on 2023-06-25 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_history', '0014_video_top_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='top_comment',
            new_name='top_comment_text',
        ),
        migrations.AddField(
            model_name='video',
            name='top_comment_author',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='video',
            name='top_comment_likes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
