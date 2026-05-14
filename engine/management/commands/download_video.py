from django.core.management.base import BaseCommand

from config.logger import get_logger
from engine.downloader.manager import DownloadManager

# Initialize logger
logger = get_logger("download_video")


# Command class to download video
class Command(BaseCommand):
    help = "Download video from supported platforms"

    # Command arguments
    def add_arguments(self, parser):
        # URL passed from terminal
        parser.add_argument("url", type=str)

    # Command handler
    def handle(self, *args, **options):
        url = options["url"]

        logger.info(f"Command started for URL: {url}")

        self.stdout.write(self.style.NOTICE(f"Starting download: {url}"))

        result = DownloadManager.download(url)

        if result.success:
            logger.info(f"Command finished successfully. File: {result.file_path}")

            self.stdout.write(
                self.style.SUCCESS(f"""
                Download completed

                Platform: {result.platform}
                Title: {result.title}
                File: {result.file_path}
            """)
            )

        else:
            logger.error(f"Command failed. Error: {result.error}")
            self.stdout.write(self.style.ERROR(f"Download failed: {result.error}"))
