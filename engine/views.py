import json
import os
import threading

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from config.logger import get_logger
from engine.downloader.manager import DownloadManager
from engine.models import DownloadJob
from engine.storage.cloudinary import CloudinaryStorage

logger = get_logger(__name__)


# Process job in the background (separate thread)
def process_job(job_id: str):
    job = DownloadJob.objects.get(id=job_id)
    job.status = "processing"
    job.save()

    try:
        result = DownloadManager.download(job.url)

        if result.success:
            # Upload to Cloudinary
            cloud = CloudinaryStorage.upload(result.file_path, result.platform)

            # Delete local temp file after upload
            if os.path.exists(result.file_path):
                os.remove(result.file_path)
                logger.info(f"Deleted local file: {result.file_path}")

            job.status = "done"
            job.cloud_url = cloud["url"]
            job.platform = result.platform
            job.title = result.title
            job.duration = result.duration
            job.thumbnail = result.thumbnail
            job.uploader = result.uploader
            job.file_size = cloud["file_size"]

        else:
            job.status = "failed"
            job.error = result.error or "Unknown error"

    except Exception as e:
        job.status = "failed"
        job.error = str(e)

    job.save()


# Download video API
# api/v1/engine/download
@method_decorator(csrf_exempt, name="dispatch")
class DownloadVideoView(View):
    def post(self, request, *args, **kwargs):
        # Parse request body
        try:
            data = json.loads(request.body)
            url = data.get("url")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        if not url:
            return JsonResponse({"error": "URL is required"}, status=400)

        logger.info(f"API download request received for URL: {url}")

        # Create job record immediately
        job = DownloadJob.objects.create(url=url)

        # Spin off background thread — response returns instantly
        thread = threading.Thread(target=process_job, args=(str(job.id),))
        thread.daemon = True
        thread.start()

        return JsonResponse({"job_id": str(job.id), "status": "pending"}, status=202)


# Get job status API
# api/v1/engine/download/{job_id}
@method_decorator(csrf_exempt, name="dispatch")
class JobStatusView(View):
    def get(self, request, job_id, *args, **kwargs):
        try:
            job = DownloadJob.objects.get(id=job_id)
        except DownloadJob.DoesNotExist:
            return JsonResponse({"error": "Job not found"}, status=404)

        # Job completed — return metadata and cloud URL
        if job.status == "done":
            return JsonResponse(
                {
                    "status": "done",
                    "url": job.cloud_url,
                    "platform": job.platform,
                    "title": job.title,
                    "duration": job.duration,
                    "thumbnail": job.thumbnail,
                    "uploader": job.uploader,
                    "file_size": job.file_size,
                }
            )

        # Still processing or failed
        return JsonResponse(
            {
                "job_id": str(job.id),
                "status": job.status,
                "error": job.error,
            }
        )
