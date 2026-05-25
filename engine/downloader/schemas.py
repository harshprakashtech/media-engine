from dataclasses import dataclass
from typing import Optional


@dataclass
class DownloadResult:
    success: bool
    platform: str
    title: Optional[str] = None
    duration: Optional[int] = None
    file_path: Optional[str] = None
    thumbnail: Optional[str] = None
    uploader: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None
