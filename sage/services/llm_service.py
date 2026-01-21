"""Unified LLM service that uses the appropriate provider based on configuration."""

from typing import Any

from ..models.request import Concept, Options, Question
from .llm_provider import (
    EmbeddingProvider,
    GenerationProvider,
    ProviderFactory,
    VisionProvider,
)


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

        # Check if concept has images
        images = [
            {"data": c.data, "media_type": self._detect_media_type(c.data)}
            for c in concept.content
            if c.type == "image"
        ]

        if images:
            # Use vision provider for multimodal
            return await self.vision_provider.generate_with_images(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                images=images,
                temperature=self.options.generation_temperature,
            )
        else:
            # Use generation provider for text-only
            return await self.generation_provider.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=self.options.generation_temperature,
            )

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

        prompt = f'Here is a product concept for "{concept.name}":\n\n'

        if text_content:
            prompt += f"{text_content}\n\n"

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
