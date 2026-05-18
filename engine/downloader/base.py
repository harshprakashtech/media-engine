import os
import uuid

import yt_dlp

from config.logger import get_logger
from engine.processor.inspector import VideoInspector
from engine.processor.normalizer import VideoNormalizer

from .schemas import DownloadResult

# # Initialize logger
logger = get_logger(__name__)


# Base class for all downloaders
class BaseDownloader:
    platform = "unknown"

    # Get download output path
    def get_output_path(self):
        folder = f"temp/{self.platform}"

        # Create folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        # yt-dlp replaces %(ext)s with actual extension
        return os.path.join(folder, f"{uuid.uuid4()}.%(ext)s")

    # Shared yt-dlp settings
    def get_ydl_opts(self):
        return {
            "outtmpl": self.get_output_path(),
            "quiet": True,
            "noplaylist": True,
        }

    # Download video
    def download(self, url: str) -> DownloadResult:
        try:
            logger.info(f"[{self.platform}] Starting download process for {url}")

            ydl_opts = self.get_ydl_opts()

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"[{self.platform}] Extracting video information")

                # Download + extract metadata
                info = ydl.extract_info(url, download=True)

                # Final downloaded file path & normalized
                file_path = ydl.prepare_filename(info)
                file_path = VideoNormalizer.normalize(file_path)

                metadata = VideoInspector.inspect(file_path)

            logger.info(
                f"[{self.platform}] Successfully downloaded and processed {url}"
            )

            return DownloadResult(
                success=True,
                platform=self.platform,
                title=info.get("title"),
                duration=info.get("duration"),
                thumbnail=info.get("thumbnail"),
                uploader=info.get("uploader"),
                file_path=file_path,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(f"[{self.platform}] Download failed: {str(e)}")

            # Standardized failure response
            return DownloadResult(success=False, platform=self.platform, error=str(e))
