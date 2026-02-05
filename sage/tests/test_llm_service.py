"""Tests for LLMService - prompt building, media detection, and routing."""

import pytest
from unittest.mock import AsyncMock, patch

from sage.models.request import Concept, ContentItem, Options, Question
from sage.services.llm_service import LLMService
from sage.services.video_downloader import VideoSource


@pytest.fixture
def options():
    return Options(
        generation_provider="openai",
        generation_model="gpt-4o",
        embedding_provider="openai",
        embedding_model="text-embedding-3-small",
        vision_provider="openai",
        vision_model="gpt-4o",
    )


@pytest.fixture
def text_concept():
    return Concept(
        name="Test Product",
        content=[ContentItem(type="text", data="A new widget.")],
    )


@pytest.fixture
def image_concept():
    # /9j/ is the base64 prefix for JPEG images
    return Concept(
        name="Visual Product",
        content=[
            ContentItem(type="text", data="A shiny product."),
            ContentItem(type="image", data="/9j/fakebase64data"),
        ],
    )


@pytest.fixture
def question():
    return Question(
        id="q1",
        text="Would you buy this?",
        weight=1.0,
        ssr_reference_sets=[["a", "b", "c", "d", "e"]] * 6,
    )


@pytest.fixture
def persona():
    return {"persona_id": "p1", "age": 30, "gender": "F"}


class TestPromptBuilding:
    """Test system and user prompt construction."""

    def test_system_prompt_contains_persona_attrs(self, options):
        with patch("sage.services.llm_service.ProviderFactory"):
            service = LLMService(options)
        prompt = service._build_system_prompt({"persona_id": "p1", "age": 30, "gender": "F"})
        assert "Age: 30" in prompt
        assert "Gender: F" in prompt
        assert "persona_id" not in prompt.lower() or "persona_id" not in prompt

    def test_user_prompt_contains_concept_and_question(self, options, text_concept, question):
        with patch("sage.services.llm_service.ProviderFactory"):
            service = LLMService(options)
        prompt = service._build_user_prompt(text_concept, question)
        assert "Test Product" in prompt
        assert "A new widget." in prompt
        assert "Would you buy this?" in prompt


class TestMediaTypeDetection:
    """Test image media type detection from base64 headers."""

    def test_jpeg_detection(self, options):
        with patch("sage.services.llm_service.ProviderFactory"):
            service = LLMService(options)
        assert service._detect_media_type("/9j/abc") == "image/jpeg"

    def test_png_detection(self, options):
        with patch("sage.services.llm_service.ProviderFactory"):
            service = LLMService(options)
        assert service._detect_media_type("iVBORxyz") == "image/png"

    def test_gif_detection(self, options):
        with patch("sage.services.llm_service.ProviderFactory"):
            service = LLMService(options)
        assert service._detect_media_type("R0lGOxyz") == "image/gif"

    def test_webp_detection(self, options):
        with patch("sage.services.llm_service.ProviderFactory"):
            service = LLMService(options)
        assert service._detect_media_type("UklGRxyz") == "image/webp"

    def test_unknown_defaults_to_jpeg(self, options):
        with patch("sage.services.llm_service.ProviderFactory"):
            service = LLMService(options)
        assert service._detect_media_type("unknowndata") == "image/jpeg"


class TestResponseRouting:
    """Test that text-only uses generation provider and images use vision provider."""

    @pytest.mark.asyncio
    async def test_text_only_uses_generation_provider(
        self, options, persona, text_concept, question
    ):
        mock_gen = AsyncMock()
        mock_gen.generate.return_value = "I would buy it."

        with patch("sage.services.llm_service.ProviderFactory") as factory:
            factory.create_generation_provider.return_value = mock_gen
            factory.create_embedding_provider.return_value = AsyncMock()
            factory.create_vision_provider.return_value = AsyncMock()
            service = LLMService(options)

        result = await service.generate_response(persona, text_concept, question)
        assert result == "I would buy it."
        mock_gen.generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_images_use_vision_provider(
        self, options, persona, image_concept, question
    ):
        mock_vision = AsyncMock()
        mock_vision.generate_with_images.return_value = "Looks great, I'd buy it."

        with patch("sage.services.llm_service.ProviderFactory") as factory:
            factory.create_generation_provider.return_value = AsyncMock()
            factory.create_embedding_provider.return_value = AsyncMock()
            factory.create_vision_provider.return_value = mock_vision
            service = LLMService(options)

        result = await service.generate_response(persona, image_concept, question)
        assert result == "Looks great, I'd buy it."
        mock_vision.generate_with_images.assert_called_once()

    @pytest.mark.asyncio
    async def test_video_uses_video_provider(self, options, persona, question):
        video_concept = Concept(
            name="Video Product",
            content=[
                ContentItem(type="text", data="A product demo."),
                ContentItem(type="video", data="s3://bucket/demo.mp4"),
            ],
        )

        mock_video = AsyncMock()
        mock_video.generate_with_video.return_value = "The video shows a great product."

        mock_downloader = AsyncMock()
        mock_downloader.resolve.return_value = VideoSource(
            source_type="s3", data="s3://bucket/demo.mp4"
        )

        with patch("sage.services.llm_service.ProviderFactory") as factory:
            factory.create_generation_provider.return_value = AsyncMock()
            factory.create_embedding_provider.return_value = AsyncMock()
            factory.create_vision_provider.return_value = mock_video
            service = LLMService(options)

        service.video_provider = mock_video
        service.video_downloader = mock_downloader

        result = await service.generate_response(persona, video_concept, question)
        assert result == "The video shows a great product."
        mock_video.generate_with_video.assert_called_once()
        mock_downloader.resolve.assert_called_once()

    @pytest.mark.asyncio
    async def test_video_takes_priority_over_images(self, options, persona, question):
        """When concept has both video and image, video path should be used."""
        mixed_concept = Concept(
            name="Mixed Product",
            content=[
                ContentItem(type="text", data="A product."),
                ContentItem(type="image", data="/9j/fakebase64"),
                ContentItem(type="video", data="s3://bucket/demo.mp4"),
            ],
        )

        mock_video = AsyncMock()
        mock_video.generate_with_video.return_value = "Video response."
        mock_vision = AsyncMock()

        mock_downloader = AsyncMock()
        mock_downloader.resolve.return_value = VideoSource(
            source_type="s3", data="s3://bucket/demo.mp4"
        )

        with patch("sage.services.llm_service.ProviderFactory") as factory:
            factory.create_generation_provider.return_value = AsyncMock()
            factory.create_embedding_provider.return_value = AsyncMock()
            factory.create_vision_provider.return_value = mock_vision
            service = LLMService(options)

        service.video_provider = mock_video
        service.video_downloader = mock_downloader

        result = await service.generate_response(persona, mixed_concept, question)
        assert result == "Video response."
        mock_video.generate_with_video.assert_called_once()
        mock_vision.generate_with_images.assert_not_called()


class TestVideoPromptBuilding:
    """Test that video-related prompts include video indicator."""

    def test_user_prompt_mentions_video_when_present(self, options, question):
        video_concept = Concept(
            name="Video Product",
            content=[
                ContentItem(type="text", data="A demo product."),
                ContentItem(type="video", data="s3://bucket/demo.mp4"),
            ],
        )
        with patch("sage.services.llm_service.ProviderFactory"):
            service = LLMService(options)
        prompt = service._build_user_prompt(video_concept, question)
        assert "[A video is attached showing this concept.]" in prompt

    def test_user_prompt_no_video_mention_without_video(self, options, question):
        text_concept = Concept(
            name="Text Product",
            content=[ContentItem(type="text", data="Just text.")],
        )
        with patch("sage.services.llm_service.ProviderFactory"):
            service = LLMService(options)
        prompt = service._build_user_prompt(text_concept, question)
        assert "video" not in prompt.lower()
