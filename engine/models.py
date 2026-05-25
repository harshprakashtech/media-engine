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
    file_path = models.CharField(max_length=500, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} — {self.status}"
