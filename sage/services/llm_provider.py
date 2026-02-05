"""Abstract interfaces and factory for LLM providers."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .bedrock_provider import (
        BedrockEmbeddingProvider,
        BedrockGenerationProvider,
        BedrockVisionProvider,
    )
    from .openai_provider import (
        OpenAIEmbeddingProvider,
        OpenAIGenerationProvider,
        OpenAIVisionProvider,
    )


class ProviderType(str, Enum):
    """Supported LLM provider types."""

    OPENAI = "openai"
    BEDROCK = "bedrock"


class GenerationProvider(ABC):
    """Abstract base class for text generation providers."""

    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text response.

        Args:
            system_prompt: System instructions
            user_prompt: User message
            temperature: Sampling temperature

        Returns:
            Generated text response
        """
        pass


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        pass

    @abstractmethod
    async def embed_single(self, text: str) -> list[float]:
        """
        Embed a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        pass

    @abstractmethod
    async def embed_with_cache(self, texts: list[str]) -> list[list[float]]:
        """
        Embed texts with caching (for anchor texts).

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors (possibly from cache)
        """
        pass


class VisionProvider(ABC):
    """Abstract base class for vision (multimodal) providers."""

    @abstractmethod
    async def generate_with_images(
        self,
        system_prompt: str,
        user_prompt: str,
        images: list[dict],  # [{"data": base64, "media_type": "image/jpeg"}]
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text response with images.

        Args:
            system_prompt: System instructions
            user_prompt: User message
            images: List of image data dicts
            temperature: Sampling temperature

        Returns:
            Generated text response
        """
        pass

    async def generate_with_video(
        self,
        prompt: str,
        video_source: Any,
        temperature: float = 0.2,
    ) -> str:
        """Generate text response from a video.

        Args:
            prompt: Combined prompt text
            video_source: Resolved video source
            temperature: Sampling temperature

        Returns:
            Generated text response
        """
        raise NotImplementedError("Video generation not supported by this provider")


class ProviderFactory:
    """Factory to create providers based on configuration.

    Caches provider instances by (provider_type, capability, model) to avoid
    creating duplicate clients for the same configuration.
    """

    _cache: dict[tuple[str, str, str], object] = {}

    @classmethod
    def create_generation_provider(
        cls,
        provider: str,
        model: str,
    ) -> GenerationProvider:
        """Create or return cached generation provider."""
        from .bedrock_provider import BedrockGenerationProvider
        from .openai_provider import OpenAIGenerationProvider

        key = (provider, "generation", model)
        if key not in cls._cache:
            if provider == ProviderType.OPENAI or provider == "openai":
                cls._cache[key] = OpenAIGenerationProvider(model=model)
            elif provider == ProviderType.BEDROCK or provider == "bedrock":
                cls._cache[key] = BedrockGenerationProvider(model=model)
            else:
                raise ValueError(f"Unknown generation provider: {provider}")
        return cls._cache[key]  # type: ignore[return-value]

    @classmethod
    def create_embedding_provider(
        cls,
        provider: str,
        model: str,
    ) -> EmbeddingProvider:
        """Create or return cached embedding provider."""
        from .bedrock_provider import BedrockEmbeddingProvider
        from .openai_provider import OpenAIEmbeddingProvider

        key = (provider, "embedding", model)
        if key not in cls._cache:
            if provider == ProviderType.OPENAI or provider == "openai":
                cls._cache[key] = OpenAIEmbeddingProvider(model=model)
            elif provider == ProviderType.BEDROCK or provider == "bedrock":
                cls._cache[key] = BedrockEmbeddingProvider(model=model)
            else:
                raise ValueError(f"Unknown embedding provider: {provider}")
        return cls._cache[key]  # type: ignore[return-value]

    @classmethod
    def create_vision_provider(
        cls,
        provider: str,
        model: str,
    ) -> VisionProvider:
        """Create or return cached vision provider."""
        from .bedrock_provider import BedrockVisionProvider
        from .openai_provider import OpenAIVisionProvider

        key = (provider, "vision", model)
        if key not in cls._cache:
            if provider == ProviderType.OPENAI or provider == "openai":
                cls._cache[key] = OpenAIVisionProvider(model=model)
            elif provider == ProviderType.BEDROCK or provider == "bedrock":
                cls._cache[key] = BedrockVisionProvider(model=model)
            else:
                raise ValueError(f"Unknown vision provider: {provider}")
        return cls._cache[key]  # type: ignore[return-value]
