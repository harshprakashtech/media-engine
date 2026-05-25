import cloudinary.uploader

from config.logger import get_logger

logger = get_logger(__name__)


class CloudinaryStorage:
    @staticmethod
    def upload(file_path: str, platform: str) -> dict:
        logger.info(f"Uploading {file_path} to Cloudinary")

        result = cloudinary.uploader.upload_large(
            file_path,
            resource_type="video",
            folder=f"media-engine/{platform}",
        )

        logger.info(f"Upload successful: {result['secure_url']}")

        return {
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "file_size": result["bytes"],
            "duration": result.get("duration"),
            "width": result.get("width"),
            "height": result.get("height"),
            "format": result.get("format"),
        }
