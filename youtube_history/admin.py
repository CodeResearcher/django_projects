from django.contrib import admin
from .models import Video, Sorting, Playlist, Category, Tag

# Register your models here.

admin.site.register(Video)
admin.site.register(Sorting)
admin.site.register(Playlist)
admin.site.register(Category)
admin.site.register(Tag)