from config.logger import get_logger

from .factory import DownloaderFactory

logger = get_logger(__name__)


class DownloadManager:
    @staticmethod
    def download(url: str):
        logger.info(f"Starting download manager for URL: {url}")

        # Select correct platform downloader
        downloader = DownloaderFactory.get_downloader(url)

        # Start download
        logger.info(f"Delegating download to {downloader.__class__.__name__}")

        return downloader.download(url)
