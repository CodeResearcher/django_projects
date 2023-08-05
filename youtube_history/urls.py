from django.urls import path
from youtube_history import views

urlpatterns = [
    path("", views.index, name="index"),
    path("privacy", views.privacy, name="privacy"),
]