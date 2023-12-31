# Generated by Django 4.2.2 on 2023-06-11 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_history', '0003_alter_video_playlist'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-created_on'], 'verbose_name': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='playlist',
            options={'ordering': ['-created_on'], 'verbose_name': 'Playlist'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-created_on'], 'verbose_name': 'Tag'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-published_at'], 'verbose_name': 'Video'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='addedAt',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='playlist',
            old_name='channelId',
            new_name='channel_id',
        ),
        migrations.RenameField(
            model_name='playlist',
            old_name='channelTitle',
            new_name='channel_title',
        ),
        migrations.RenameField(
            model_name='playlist',
            old_name='addedAt',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='addedAt',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='commentCount',
            new_name='comment_count',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='addedAt',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='likeCount',
            new_name='like_count',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='publishedAt',
            new_name='published_at',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='thumbnailUrl',
            new_name='thumbnail_url',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='videoUrl',
            new_name='video_url',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='viewCount',
            new_name='view_count',
        ),
        migrations.RemoveField(
            model_name='category',
            name='categoryId',
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='playlistId',
        ),
        migrations.RemoveField(
            model_name='video',
            name='videoId',
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='video',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='video',
            name='playlist',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='youtube_history.playlist'),
            preserve_default=False,
        ),
    ]
