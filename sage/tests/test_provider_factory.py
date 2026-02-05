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

    def test_create_bedrock_vision_with_pegasus(self):
        """Pegasus model should create a BedrockVisionProvider with twelvelabs family."""
        from sage.services.bedrock_provider import BedrockVisionProvider

        provider = ProviderFactory.create_vision_provider(
            "bedrock", "eu.twelvelabs.pegasus-1-2-v1:0"
        )
        assert isinstance(provider, BedrockVisionProvider)
        assert provider.family == "twelvelabs"


class TestFamilyDetection:
    """Test _detect_family correctly identifies model families."""

    def test_twelvelabs_family(self):
        from sage.services.bedrock_provider import _detect_family

        assert _detect_family("eu.twelvelabs.pegasus-1-2-v1:0") == "twelvelabs"

    def test_anthropic_family(self):
        from sage.services.bedrock_provider import _detect_family

        assert _detect_family("eu.anthropic.claude-sonnet-4-5-20250929-v1:0") == "anthropic"

    def test_nova_family(self):
        from sage.services.bedrock_provider import _detect_family

        assert _detect_family("eu.amazon.nova-pro-v1:0") == "nova"

    def test_unknown_family_raises(self):
        from sage.exceptions import ConfigurationError
        from sage.services.bedrock_provider import _detect_family

        with pytest.raises(ConfigurationError, match="Unknown Bedrock model family"):
            _detect_family("unknown.model-v1:0")
