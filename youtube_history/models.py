from django.db import models
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=500)
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:    
        ordering = ['-created_on']
        verbose_name = 'Tag'

class Category(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:    
        ordering = ['-created_on']
        verbose_name = 'Category'

class Playlist(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    rank = models.SmallIntegerField(default=99)
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#e60007')
    channel_id = models.CharField(max_length=100)
    channel_title = models.CharField(max_length=100)
    PLAYLIST_STATUS = (
        ('a', 'active'),
        ('i', 'inactive')
    )
    status = models.CharField(
        max_length=1,
        choices=PLAYLIST_STATUS,
        default='a'
    )
    total_videos = models.IntegerField(null=True, blank=True)
    request_count = models.IntegerField(default=0)
    page_token = models.CharField(max_length=500, null=True, blank=True)
    last_api_call = models.DateTimeField(null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:    
        ordering = ['rank']
        verbose_name = 'Playlist'

class Sorting(models.Model):
    rank = models.SmallIntegerField(default=99)
    display_name = models.CharField(max_length=50)
    column_name = models.CharField(max_length=50)
    ascending = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name
    
    class Meta:    
        ordering = ['rank']
        verbose_name = 'Sorting'

class Video(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=10000, null=True, blank=True)
    published_at = models.DateTimeField()
    duration = models.DurationField(null=True, blank=True)
    view_count = models.IntegerField(null=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    comment_count = models.IntegerField(null=True, blank=True)
    top_comment_text = models.TextField(max_length=10000, null=True, blank=True)
    top_comment_likes = models.IntegerField(null=True, blank=True)
    top_comment_author = models.CharField(max_length=100, null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    video_url = models.URLField()
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )
    tag = models.ManyToManyField(
        Tag
    )
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(default=timezone.now) #models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_url
    
    class Meta:    
        ordering = [
            #'published_at'
            'playlist__rank', 
            '-published_at__year', 
            'published_at__hour', 
            'published_at__minute', 
            'title'
        ]
        verbose_name = 'Video'