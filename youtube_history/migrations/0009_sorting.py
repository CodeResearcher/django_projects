# Generated by Django 4.2.2 on 2023-06-23 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_history', '0008_playlist_color_playlist_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sorting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=50)),
                ('column_name', models.CharField(max_length=50)),
                ('ascending', models.BooleanField(default=True, max_length=50)),
            ],
        ),
    ]
