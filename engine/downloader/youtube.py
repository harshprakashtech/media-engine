from .base import BaseDownloader


class YouTubeDownloader(BaseDownloader):
    platform = "youtube"

    # Youtube specific options
    def get_ydl_opts(self):
        opts = super().get_ydl_opts()

        opts.update(
            {
                # Fallback format string to ensure it finds a valid format
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                # Merge into mp4 if possible
                "merge_output_format": "mp4",
                # Allow yt-dlp to execute YouTube JS extraction
                "js_runtimes": {"nodejs": {}},
                # Use mobile clients to bypass web JavaScript challenges and rate limits
                "extractor_args": {
                    "youtube": ["player_client=android", "player_client=ios"]
                },
            }
        )

        return opts
