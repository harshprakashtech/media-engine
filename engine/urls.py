from django.urls import path

from .views import DownloadVideoView, JobStatusView

urlpatterns = [
    path("download/", DownloadVideoView.as_view(), name="download-video"),
    path("download/<uuid:job_id>/", JobStatusView.as_view(), name="job-status"),
]
