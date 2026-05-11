import os
import uuid

import yt_dlp

from .schemas import DownloadResult


class BaseDownloader:
    platform = "unknown"

    # Get download output path
    def get_output_path(self):
        folder = f"/tmp/media-engine/{self.platform}"

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
            ydl_opts = self.get_ydl_opts()

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Download + extract metadata
                info = ydl.extract_info(url, download=True)

                # Final downloaded file path
                # file_path = ydl.prepare_filename(info)
                requested_downloads = info.get("requested_downloads")

                if requested_downloads:
                    file_path = requested_downloads[0].get("filepath")
                else:
                    file_path = ydl.prepare_filename(info)

            return DownloadResult(
                success=True,
                platform=self.platform,
                title=info.get("title"),
                duration=info.get("duration"),
                thumbnail=info.get("thumbnail"),
                uploader=info.get("uploader"),
                file_path=file_path,
            )

        except Exception as e:
            # Standardized failure response
            return DownloadResult(success=False, platform=self.platform, error=str(e))
