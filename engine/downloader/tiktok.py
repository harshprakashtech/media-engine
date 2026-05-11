from .base import BaseDownloader


class TikTokDownloader(BaseDownloader):
    platform = "tiktok"

    # TikTok specific options
    def get_ydl_opts(self):
        opts = super().get_ydl_opts()

        opts.update(
            {
                "format": "best",
            }
        )

        return opts
