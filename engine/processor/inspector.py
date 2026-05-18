import json
import subprocess
from pathlib import Path

from config.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


# Inspect video metadata using ffprobe
class VideoInspector:
    @staticmethod
    def inspect(file_path: str) -> dict:
        logger.info(f"Inspecting video file: {file_path}")

        command = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            file_path,
        ]

        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode != 0:
            logger.error(f"ffprobe failed: {process.stderr}")

            raise Exception(f"ffprobe failed:\n{process.stderr}")

        data = json.loads(process.stdout)

        video_stream = next(
            (stream for stream in data["streams"] if stream["codec_type"] == "video"),
            {},
        )

        audio_stream = next(
            (stream for stream in data["streams"] if stream["codec_type"] == "audio"),
            {},
        )

        logger.info(f"Successfully inspected video file: {file_path}")

        return {
            "file_name": Path(file_path).name,
            "format": data["format"].get("format_name"),
            "duration": float(data["format"].get("duration", 0)),
            "size_bytes": int(data["format"].get("size", 0)),
            "bit_rate": int(data["format"].get("bit_rate", 0)),
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "video_codec": video_stream.get("codec_name"),
            "audio_codec": audio_stream.get("codec_name"),
            "fps": eval(video_stream.get("r_frame_rate", "0/1")),
        }
