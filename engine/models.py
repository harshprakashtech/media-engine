from uuid import uuid4

from django.db import models


class DownloadJob(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("done", "Done"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    url = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Cloudinary
    cloud_url = models.URLField(blank=True)

    # Metadata
    platform = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=500, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    thumbnail = models.URLField(blank=True)
    uploader = models.CharField(max_length=200, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)

    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
