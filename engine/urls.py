from django.urls import path

from .views import DownloadVideoView

urlpatterns = [
    path("download/", DownloadVideoView.as_view(), name="download-video"),
]
