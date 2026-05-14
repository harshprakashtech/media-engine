from config.logger import get_logger

from .instagram import InstagramDownloader
from .tiktok import TikTokDownloader
from .youtube import YouTubeDownloader

logger = get_logger(__name__)


class DownloaderFactory:
    @staticmethod
    def get_downloader(url: str):
        logger.info(f"Determining downloader for URL: {url}")

        # Extract platform from URL
        # Choose downloader based on platform
        if "youtube.com" in url or "youtu.be" in url:
            logger.info("Selected YouTube Downloader")
            return YouTubeDownloader()

        if "instagram.com" in url:
            logger.info("Selected Instagram Downloader")
            return InstagramDownloader()

        if "tiktok.com" in url:
            logger.info("Selected TikTok Downloader")
            return TikTokDownloader()

        logger.error(f"Unsupported platform for URL: {url}")
        raise ValueError("Unsupported platform")
