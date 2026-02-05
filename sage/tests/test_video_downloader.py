"""Tests for VideoDownloader - source type detection and resolution."""

import asyncio
import base64

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from sage.services.video_downloader import VideoDownloader


@pytest.fixture
def downloader():
    return VideoDownloader()


class TestSourceTypeDetection:
    """Test that _is_youtube, _is_url, _is_s3 correctly classify data strings."""

    def test_youtube_watch_url(self, downloader):
        assert downloader._is_youtube("https://www.youtube.com/watch?v=abc123")

    def test_youtube_short_url(self, downloader):
        assert downloader._is_youtube("https://youtu.be/abc123")

    def test_youtube_shorts_url(self, downloader):
        assert downloader._is_youtube("https://www.youtube.com/shorts/abc123")

    def test_non_youtube_url(self, downloader):
        assert not downloader._is_youtube("https://example.com/video.mp4")

    def test_s3_uri(self, downloader):
        assert downloader._is_s3("s3://my-bucket/video.mp4")

    def test_non_s3(self, downloader):
        assert not downloader._is_s3("https://example.com/video.mp4")

    def test_http_url(self, downloader):
        assert downloader._is_url("https://example.com/video.mp4")

    def test_http_url_no_ssl(self, downloader):
        assert downloader._is_url("http://example.com/video.mp4")

    def test_base64_not_url(self, downloader):
        assert not downloader._is_url("AAAA/base64data==")


class TestResolveS3:
    """Test S3 URI passthrough."""

    @pytest.mark.asyncio
    async def test_s3_passthrough(self, downloader):
        result = await downloader.resolve("s3://bucket/video.mp4")
        assert result.source_type == "s3"
        assert result.data == "s3://bucket/video.mp4"
        assert result.s3_bucket_owner is None

    @pytest.mark.asyncio
    async def test_s3_with_bucket_owner(self, downloader):
        result = await downloader.resolve("s3://bucket/video.mp4", s3_bucket_owner="123456789")
        assert result.source_type == "s3"
        assert result.s3_bucket_owner == "123456789"


class TestResolveBase64:
    """Test base64 passthrough."""

    @pytest.mark.asyncio
    async def test_base64_passthrough(self, downloader):
        b64 = base64.b64encode(b"fake video data").decode()
        result = await downloader.resolve(b64)
        assert result.source_type == "base64"
        assert result.data == b64


class TestResolveYouTube:
    """Test YouTube download resolution."""

    @pytest.mark.asyncio
    async def test_youtube_downloads_and_encodes(self, downloader):
        fake_bytes = b"fake mp4 content"

        with patch.object(downloader, "_download_youtube", new_callable=AsyncMock) as mock_dl:
            mock_dl.return_value = fake_bytes
            result = await downloader.resolve("https://www.youtube.com/watch?v=test123")

        assert result.source_type == "base64"
        assert result.data == base64.b64encode(fake_bytes).decode("ascii")
        mock_dl.assert_called_once_with("https://www.youtube.com/watch?v=test123")


class TestResolveURL:
    """Test direct URL download resolution."""

    @pytest.mark.asyncio
    async def test_url_downloads_and_encodes(self, downloader):
        fake_bytes = b"fake mp4 content"

        with patch.object(downloader, "_download_url", new_callable=AsyncMock) as mock_dl:
            mock_dl.return_value = fake_bytes
            result = await downloader.resolve("https://example.com/video.mp4")

        assert result.source_type == "base64"
        assert result.data == base64.b64encode(fake_bytes).decode("ascii")
        mock_dl.assert_called_once_with("https://example.com/video.mp4")


class TestCaching:
    """Test that resolved video sources are cached within a single downloader instance."""

    @pytest.mark.asyncio
    async def test_cache_hit_skips_download(self, downloader):
        """Resolve same URL twice - download should only be called once."""
        fake_bytes = b"fake mp4 content"
        url = "https://example.com/video.mp4"

        with patch.object(downloader, "_download_url", new_callable=AsyncMock) as mock_dl:
            mock_dl.return_value = fake_bytes
            await downloader.resolve(url)
            await downloader.resolve(url)

        mock_dl.assert_called_once_with(url)

    @pytest.mark.asyncio
    async def test_different_urls_not_cached(self, downloader):
        """Resolve two different URLs - both should be downloaded."""
        fake_bytes = b"fake mp4 content"

        with patch.object(downloader, "_download_url", new_callable=AsyncMock) as mock_dl:
            mock_dl.return_value = fake_bytes
            await downloader.resolve("https://example.com/video1.mp4")
            await downloader.resolve("https://example.com/video2.mp4")

        assert mock_dl.call_count == 2

    @pytest.mark.asyncio
    async def test_cache_returns_same_result(self, downloader):
        """Cached result should be identical to the first resolve."""
        fake_bytes = b"fake mp4 content"
        url = "https://example.com/video.mp4"

        with patch.object(downloader, "_download_url", new_callable=AsyncMock) as mock_dl:
            mock_dl.return_value = fake_bytes
            first = await downloader.resolve(url)
            second = await downloader.resolve(url)

        assert first is second


    @pytest.mark.asyncio
    async def test_concurrent_resolves_download_once(self, downloader):
        """Many concurrent resolves of the same URL should only download once."""
        fake_bytes = b"fake mp4 content"
        url = "https://example.com/video.mp4"

        with patch.object(downloader, "_download_url", new_callable=AsyncMock) as mock_dl:
            mock_dl.return_value = fake_bytes
            results = await asyncio.gather(*[downloader.resolve(url) for _ in range(50)])

        mock_dl.assert_called_once_with(url)
        assert all(r is results[0] for r in results)


class TestPriorityOrder:
    """Test that detection priority is S3 > YouTube > URL > base64."""

    @pytest.mark.asyncio
    async def test_s3_takes_priority(self, downloader):
        # An S3 URI is also technically a URL-like string
        result = await downloader.resolve("s3://bucket/video.mp4")
        assert result.source_type == "s3"

    @pytest.mark.asyncio
    async def test_youtube_before_generic_url(self, downloader):
        with patch.object(downloader, "_download_youtube", new_callable=AsyncMock) as mock_dl:
            mock_dl.return_value = b"data"
            result = await downloader.resolve("https://www.youtube.com/watch?v=test")
        # Should have used YouTube downloader, not generic URL
        assert result.source_type == "base64"
        mock_dl.assert_called_once()
