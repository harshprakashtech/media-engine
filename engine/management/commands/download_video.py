from django.core.management.base import BaseCommand

from engine.downloader.manager import DownloadManager


class Command(BaseCommand):
    help = "Download video from supported platforms"

    # Command arguments
    def add_arguments(self, parser):
        # URL passed from terminal
        parser.add_argument("url", type=str)

    # Command handler
    def handle(self, *args, **options):
        url = options["url"]

        self.stdout.write(self.style.NOTICE(f"Starting download: {url}"))

        result = DownloadManager.download(url)

        if result.success:
            self.stdout.write(
                self.style.SUCCESS(f"""
                Download completed

                Platform: {result.platform}
                Title: {result.title}
                File: {result.file_path}
            """)
            )

        else:
            self.stdout.write(self.style.ERROR(f"Download failed: {result.error}"))
