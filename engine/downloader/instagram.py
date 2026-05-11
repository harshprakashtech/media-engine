from .base import BaseDownloader


class InstagramDownloader(BaseDownloader):
    platform = "instagram"

    # Instagram specific options
    def get_ydl_opts(self):
        opts = super().get_ydl_opts()

        opts.update(
            {
                "format": "best",
            }
        )

        return opts
