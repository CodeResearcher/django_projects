# Generated by Django 4.2.2 on 2023-06-23 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_history', '0010_sorting_default_alter_sorting_ascending'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playlist',
            options={'ordering': ['rank'], 'verbose_name': 'Playlist'},
        ),
        migrations.AlterModelOptions(
            name='sorting',
            options={'ordering': ['rank'], 'verbose_name': 'Sorting'},
        ),
        migrations.AddField(
            model_name='sorting',
            name='rank',
            field=models.SmallIntegerField(default=99),
        ),
    ]
