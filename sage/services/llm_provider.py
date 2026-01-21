"""Abstract interfaces and factory for LLM providers."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

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


class ProviderFactory:
    """Factory to create providers based on configuration."""

    @staticmethod
    def create_generation_provider(
        provider: str,
        model: str,
    ) -> GenerationProvider:
        """
        Create a generation provider.

        Args:
            provider: Provider type ("openai" or "bedrock")
            model: Model identifier

        Returns:
            GenerationProvider instance
        """
        # Import here to avoid circular imports
        from .bedrock_provider import BedrockGenerationProvider
        from .openai_provider import OpenAIGenerationProvider

        if provider == ProviderType.OPENAI or provider == "openai":
            return OpenAIGenerationProvider(model=model)
        elif provider == ProviderType.BEDROCK or provider == "bedrock":
            return BedrockGenerationProvider(model=model)
        raise ValueError(f"Unknown generation provider: {provider}")

    @staticmethod
    def create_embedding_provider(
        provider: str,
        model: str,
    ) -> EmbeddingProvider:
        """
        Create an embedding provider.

        Args:
            provider: Provider type ("openai" or "bedrock")
            model: Model identifier

        Returns:
            EmbeddingProvider instance
        """
        from .bedrock_provider import BedrockEmbeddingProvider
        from .openai_provider import OpenAIEmbeddingProvider

        if provider == ProviderType.OPENAI or provider == "openai":
            return OpenAIEmbeddingProvider(model=model)
        elif provider == ProviderType.BEDROCK or provider == "bedrock":
            return BedrockEmbeddingProvider(model=model)
        raise ValueError(f"Unknown embedding provider: {provider}")

    @staticmethod
    def create_vision_provider(
        provider: str,
        model: str,
    ) -> VisionProvider:
        """
        Create a vision provider.

        Args:
            provider: Provider type ("openai" or "bedrock")
            model: Model identifier

        Returns:
            VisionProvider instance
        """
        from .bedrock_provider import BedrockVisionProvider
        from .openai_provider import OpenAIVisionProvider

        if provider == ProviderType.OPENAI or provider == "openai":
            return OpenAIVisionProvider(model=model)
        elif provider == ProviderType.BEDROCK or provider == "bedrock":
            return BedrockVisionProvider(model=model)
        raise ValueError(f"Unknown vision provider: {provider}")
