import json
import os

from django.http import FileResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from config.logger import get_logger
from engine.downloader.manager import DownloadManager

logger = get_logger(__name__)


# Download video from platforms
@method_decorator(csrf_exempt, name="dispatch")
class DownloadVideoView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            url = data.get("url")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        # Validate URL
        if not url:
            return JsonResponse(
                {"error": "URL is required in the request body"}, status=400
            )

        logger.info(f"API download request received for URL: {url}")

        # Start download
        result = DownloadManager.download(url)

        # Return file
        if result.success and result.file_path and os.path.exists(result.file_path):
            logger.info(f"API download successful. Returning file: {result.file_path}")
            try:
                # FileResponse handles streaming and safely closing the file
                response = FileResponse(
                    open(result.file_path, "rb"),
                    as_attachment=True,
                    filename=os.path.basename(result.file_path),
                    content_type="video/mp4",
                )

                return response

            except Exception as e:
                logger.error(f"Error serving file {result.file_path}: {str(e)}")
                return JsonResponse(
                    {"error": "Failed to serve the downloaded file"}, status=500
                )
        else:
            error_msg = result.error or "Download failed for unknown reasons"
            logger.error(f"API download failed. Error: {error_msg}")
            return JsonResponse({"error": error_msg}, status=400)
