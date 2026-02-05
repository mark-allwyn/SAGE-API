"""Video source resolver for Twelve Labs Pegasus.

Resolves video data from various sources (YouTube, URLs, S3, base64) into
a format that the Pegasus API accepts.
"""

import asyncio
import base64
import logging
import re
import tempfile
from dataclasses import dataclass
from functools import partial
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

YOUTUBE_PATTERNS = [
    re.compile(r"(?:https?://)?(?:www\.)?youtube\.com/watch"),
    re.compile(r"(?:https?://)?(?:www\.)?youtube\.com/shorts/"),
    re.compile(r"(?:https?://)?youtu\.be/"),
]

MAX_BASE64_SIZE = 25 * 1024 * 1024  # 25MB limit for base64 uploads


@dataclass
class VideoSource:
    """Resolved video source for the Pegasus API."""

    source_type: str  # "base64" or "s3"
    data: str  # base64 string or S3 URI
    s3_bucket_owner: str | None = None


class VideoDownloader:
    """Resolves video sources (URLs, YouTube, base64, S3) for Pegasus."""

    def __init__(self) -> None:
        self._cache: dict[str, VideoSource] = {}
        self._lock = asyncio.Lock()

    async def resolve(self, data: str, s3_bucket_owner: str | None = None) -> VideoSource:
        """Detect source type and resolve to base64 or S3 URI.

        Args:
            data: Video data - can be S3 URI, YouTube URL, HTTP URL, or base64
            s3_bucket_owner: Optional S3 bucket owner for S3 sources

        Returns:
            VideoSource with resolved data ready for Pegasus API
        """
        cache_key = data
        if cache_key in self._cache:
            logger.info("Video source: cache hit")
            return self._cache[cache_key]

        async with self._lock:
            # Double-check after acquiring lock
            if cache_key in self._cache:
                logger.info("Video source: cache hit")
                return self._cache[cache_key]

            if self._is_s3(data):
                logger.info("Video source: S3 URI")
                result = VideoSource(
                    source_type="s3",
                    data=data,
                    s3_bucket_owner=s3_bucket_owner,
                )
            elif self._is_youtube(data):
                logger.info("Video source: YouTube URL")
                video_bytes = await self._download_youtube(data)
                result = VideoSource(
                    source_type="base64",
                    data=self._to_base64(video_bytes),
                )
            elif self._is_url(data):
                logger.info("Video source: direct URL")
                video_bytes = await self._download_url(data)
                result = VideoSource(
                    source_type="base64",
                    data=self._to_base64(video_bytes),
                )
            else:
                # Assume base64-encoded video
                logger.info("Video source: base64")
                result = VideoSource(source_type="base64", data=data)

            self._cache[cache_key] = result
            return result

    @staticmethod
    def _is_youtube(data: str) -> bool:
        return any(p.search(data) for p in YOUTUBE_PATTERNS)

    @staticmethod
    def _is_url(data: str) -> bool:
        return data.startswith("http://") or data.startswith("https://")

    @staticmethod
    def _is_s3(data: str) -> bool:
        return data.startswith("s3://")

    async def _download_youtube(self, url: str) -> bytes:
        """Download a YouTube video as MP4 using yt-dlp."""
        import yt_dlp

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = str(Path(tmpdir) / "video.mp4")
            ydl_opts = {
                "format": "best[ext=mp4][filesize<25M]/worst[ext=mp4]",
                "quiet": True,
                "no_warnings": True,
                "outtmpl": temp_path,
            }

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                partial(self._run_yt_dlp, ydl_opts, url),
            )

            video_path = Path(temp_path)
            if not video_path.exists():
                raise RuntimeError(f"yt-dlp did not produce output file for: {url}")

            video_bytes = video_path.read_bytes()
            if len(video_bytes) > MAX_BASE64_SIZE:
                logger.warning(
                    "Downloaded video is %d bytes (limit %d), may fail base64 upload",
                    len(video_bytes),
                    MAX_BASE64_SIZE,
                )
            return video_bytes

    @staticmethod
    def _run_yt_dlp(opts: dict, url: str) -> None:
        import yt_dlp

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

    async def _download_url(self, url: str) -> bytes:
        """Download a video file from a direct URL."""
        async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            video_bytes = response.content
            if len(video_bytes) > MAX_BASE64_SIZE:
                logger.warning(
                    "Downloaded video is %d bytes (limit %d), may fail base64 upload",
                    len(video_bytes),
                    MAX_BASE64_SIZE,
                )
            return video_bytes

    @staticmethod
    def _to_base64(video_bytes: bytes) -> str:
        return base64.b64encode(video_bytes).decode("ascii")
