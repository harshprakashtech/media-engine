import os
import subprocess
from pathlib import Path
from uuid import uuid4

from config.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


# Convert any video into universally compatible MP4
class VideoNormalizer:
    @staticmethod
    def normalize(input_path: str) -> str:
        logger.info(f"Starting video normalization for: {input_path}")

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
            "-preset",
            "ultrafast",
            # Video quality
            "-crf",
            "28",
            # Audio codec -> AAC
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            # Move MP4 header to the start for HTTP streaming
            "-movflags",
            "+faststart",
            # Overwrite existing file
            "-y",
            str(output_path),
        ]

        logger.info(f"Running FFmpeg command: {' '.join(command)}")

        # Run ffmpeg command
        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode != 0:
            logger.error(f"FFmpeg normalization failed with stderr: {process.stderr}")
            raise Exception(f"FFmpeg normalization failed:\n{process.stderr}")

        # Delete original raw file after successful normalization
        if os.path.exists(input_path):
            logger.info(f"Deleting original file: {input_path}")
            os.remove(input_path)

        logger.info(f"Normalization successful. Output saved to: {output_path}")
        return str(output_path)
