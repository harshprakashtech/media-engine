from .instagram import InstagramDownloader
from .tiktok import TikTokDownloader
from .youtube import YouTubeDownloader


class DownloaderFactory:
    @staticmethod
    def get_downloader(url: str):
        # Extract platform from URL
        # Choose downloader based on platform
        if "youtube.com" in url or "youtu.be" in url:
            return YouTubeDownloader()

        if "instagram.com" in url:
            return InstagramDownloader()

        if "tiktok.com" in url:
            return TikTokDownloader()

        raise ValueError("Unsupported platform")
