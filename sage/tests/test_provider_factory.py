"""Tests for the ProviderFactory."""

import pytest

from sage.services.llm_provider import ProviderFactory
from sage.services.openai_provider import (
    OpenAIEmbeddingProvider,
    OpenAIGenerationProvider,
    OpenAIVisionProvider,
)


class TestProviderFactory:
    """Test factory creates correct provider types."""

    def test_create_openai_generation(self):
        provider = ProviderFactory.create_generation_provider("openai", "gpt-4o")
        assert isinstance(provider, OpenAIGenerationProvider)

    def test_create_openai_embedding(self):
        provider = ProviderFactory.create_embedding_provider("openai", "text-embedding-3-small")
        assert isinstance(provider, OpenAIEmbeddingProvider)

    def test_create_openai_vision(self):
        provider = ProviderFactory.create_vision_provider("openai", "gpt-4o")
        assert isinstance(provider, OpenAIVisionProvider)

    def test_create_bedrock_generation(self):
        from sage.services.bedrock_provider import BedrockGenerationProvider

        provider = ProviderFactory.create_generation_provider(
            "bedrock", "eu.anthropic.claude-sonnet-4-5-20250929-v1:0"
        )
        assert isinstance(provider, BedrockGenerationProvider)

    def test_create_bedrock_embedding(self):
        from sage.services.bedrock_provider import BedrockEmbeddingProvider

        provider = ProviderFactory.create_embedding_provider(
            "bedrock", "amazon.titan-embed-text-v2:0"
        )
        assert isinstance(provider, BedrockEmbeddingProvider)

    def test_create_bedrock_vision(self):
        from sage.services.bedrock_provider import BedrockVisionProvider

        provider = ProviderFactory.create_vision_provider(
            "bedrock", "eu.anthropic.claude-sonnet-4-5-20250929-v1:0"
        )
        assert isinstance(provider, BedrockVisionProvider)

    def test_unknown_generation_provider_raises(self):
        with pytest.raises(ValueError, match="Unknown generation provider"):
            ProviderFactory.create_generation_provider("azure", "gpt-4o")

    def test_unknown_embedding_provider_raises(self):
        with pytest.raises(ValueError, match="Unknown embedding provider"):
            ProviderFactory.create_embedding_provider("azure", "some-model")

    def test_unknown_vision_provider_raises(self):
        with pytest.raises(ValueError, match="Unknown vision provider"):
            ProviderFactory.create_vision_provider("azure", "some-model")
