"""Unified LLM service that uses the appropriate provider based on configuration."""

import logging
from typing import Any

from ..models.request import Concept, Options, Question

logger = logging.getLogger(__name__)
from .llm_provider import (
    EmbeddingProvider,
    GenerationProvider,
    ProviderFactory,
    VisionProvider,
)
from .video_downloader import VideoDownloader


class LLMService:
    """
    Unified service that uses the appropriate provider based on configuration.
    Handles both text-only and multimodal (vision) requests.
    """

    def __init__(self, options: Options):
        """
        Initialize LLM service with configured providers.

        Args:
            options: Configuration options specifying providers and models
        """
        self.options = options

        # Create providers based on options
        self.generation_provider: GenerationProvider = (
            ProviderFactory.create_generation_provider(
                options.generation_provider,
                options.generation_model,
            )
        )
        self.embedding_provider: EmbeddingProvider = (
            ProviderFactory.create_embedding_provider(
                options.embedding_provider,
                options.embedding_model,
            )
        )
        self.vision_provider: VisionProvider = ProviderFactory.create_vision_provider(
            options.vision_provider,
            options.vision_model,
        )
        self.video_provider: VisionProvider = ProviderFactory.create_vision_provider(
            options.video_provider,
            options.video_model,
        )
        self.video_downloader = VideoDownloader()

    async def generate_response(
        self,
        persona: dict[str, Any],
        concept: Concept,
        question: Question,
    ) -> str:
        """
        Generate a response, using vision if images are present.

        Args:
            persona: Consumer persona with demographic attributes
            concept: Product concept being tested
            question: Survey question to answer

        Returns:
            Generated text response
        """
        system_prompt = self._build_system_prompt(persona)
        user_prompt = self._build_user_prompt(concept, question)

        # Check for video content (video takes priority over images)
        videos = [c for c in concept.content if c.type == "video"]

        if videos:
            if len(videos) > 1:
                logger.warning(
                    "Concept has %d videos, Pegasus processes one at a time - using first",
                    len(videos),
                )
            video = videos[0]
            logger.debug(
                "Video generation: persona=%s question=%s",
                persona.get("persona_id", "?"),
                question.id,
            )
            video_source = await self.video_downloader.resolve(
                video.data,
                s3_bucket_owner=self.options.s3_bucket_owner,
            )
            # Pegasus uses a single inputPrompt - combine system + user
            combined_prompt = f"{system_prompt}\n\n{user_prompt}"
            response = await self.video_provider.generate_with_video(
                prompt=combined_prompt,
                video_source=video_source,
                temperature=self.options.generation_temperature,
            )
        else:
            # Check if concept has images
            images = [
                {"data": c.data, "media_type": self._detect_media_type(c.data)}
                for c in concept.content
                if c.type == "image"
            ]

            if images:
                logger.debug(
                    "Vision generation: persona=%s question=%s (%d images)",
                    persona.get("persona_id", "?"),
                    question.id,
                    len(images),
                )
                response = await self.vision_provider.generate_with_images(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    images=images,
                    temperature=self.options.generation_temperature,
                )
            else:
                logger.debug(
                    "Text generation: persona=%s question=%s",
                    persona.get("persona_id", "?"),
                    question.id,
                )
                response = await self.generation_provider.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=self.options.generation_temperature,
                )

        logger.debug("Response (%d chars): %.80s...", len(response), response)
        return response

    async def get_embedding(self, text: str) -> list[float]:
        """Get embedding for a single text."""
        return await self.embedding_provider.embed_single(text)

    async def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings for multiple texts."""
        return await self.embedding_provider.embed(texts)

    async def get_embeddings_cached(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings with caching (for anchor texts)."""
        return await self.embedding_provider.embed_with_cache(texts)

    def _build_system_prompt(self, persona: dict[str, Any]) -> str:
        """Build system prompt for persona impersonation."""
        persona_desc = self._format_persona(persona)
        return f"""You are role-playing as a consumer with the following characteristics:

{persona_desc}

Respond naturally and authentically as this person would. Your responses should reflect your demographics, lifestyle, and perspective. Be genuine - if something doesn't appeal to you, say so honestly. Reply briefly to any questions posed to you."""

    def _format_persona(self, persona: dict[str, Any]) -> str:
        """Format persona attributes as a readable description."""
        lines = []
        for key, value in persona.items():
            if key != "persona_id":
                formatted_key = key.replace("_", " ").title()
                lines.append(f"- {formatted_key}: {value}")
        return "\n".join(lines)

    def _build_user_prompt(self, concept: Concept, question: Question) -> str:
        """Build user prompt with concept and question."""
        text_content = "\n".join([c.data for c in concept.content if c.type == "text"])
        has_video = any(c.type == "video" for c in concept.content)

        prompt = f'Here is a product concept for "{concept.name}":\n\n'

        if text_content:
            prompt += f"{text_content}\n\n"

        if has_video:
            prompt += "[A video is attached showing this concept.]\n\n"

        prompt += f"""Please respond to this question in 2-3 sentences, speaking as yourself:

{question.text}

Give your honest reaction as this consumer would."""

        return prompt

    def _detect_media_type(self, base64_data: str) -> str:
        """Detect media type from base64 data."""
        # Simple detection based on base64 header patterns
        if base64_data.startswith("/9j/"):
            return "image/jpeg"
        elif base64_data.startswith("iVBOR"):
            return "image/png"
        elif base64_data.startswith("R0lGO"):
            return "image/gif"
        elif base64_data.startswith("UklGR"):
            return "image/webp"
        # Default to JPEG
        return "image/jpeg"
