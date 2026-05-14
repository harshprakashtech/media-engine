import os
import subprocess
from pathlib import Path
from uuid import uuid4


# Convert any video into universally compatible MP4
class VideoNormalizer:
    @staticmethod
    def normalize(input_path: str) -> str:
        input_file = Path(input_path)

        # Final normalized output
        output_path = input_file.parent / f"{uuid4()}.mp4"

        command = [
            "ffmpeg",
            "-i",
            input_path,
            # Video codec -> H264
            "-c:v",
            "libx264",
            # Audio codec -> AAC
            "-c:a",
            "aac",
            # Move MP4 header to the start for HTTP streaming
            "-movflags",
            "+faststart",
            # Overwrite existing file
            "-y",
            str(output_path),
        ]

        # Run ffmpeg command
        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode != 0:
            raise Exception(f"FFmpeg normalization failed:\n{process.stderr}")

        # Delete original raw file after successful normalization
        if os.path.exists(input_path):
            os.remove(input_path)

        return str(output_path)
