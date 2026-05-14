from .base import BaseDownloader


class YouTubeDownloader(BaseDownloader):
    platform = "youtube"

    # Youtube specific options
    def get_ydl_opts(self):
        opts = super().get_ydl_opts()

        opts.update(
            {
                # Best video + audio available
                "format": "bestvideo+bestaudio/best",
                # Merge into mp4 if possible
                "merge_output_format": "mp4",
                # Allow yt-dlp to execute YouTube JS extraction
                # "js_runtimes": {"node": "node"},
            }
        )

        return opts
