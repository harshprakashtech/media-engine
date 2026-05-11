from .factory import DownloaderFactory


class DownloadManager:
    @staticmethod
    def download(url: str):
        # Select correct platform downloader
        downloader = DownloaderFactory.get_downloader(url)

        # Start download
        return downloader.download(url)
