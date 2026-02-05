"""Tests for model validation in the Options model."""

import pytest
from pydantic import ValidationError

from sage.models.request import Options


class TestValidModelCombinations:
    """Test that valid provider+model combos are accepted."""

    def test_openai_defaults(self):
        opts = Options(
            generation_provider="openai",
            generation_model="gpt-4o",
            embedding_provider="openai",
            embedding_model="text-embedding-3-small",
            vision_provider="openai",
            vision_model="gpt-4o",
        )
        assert opts.generation_model == "gpt-4o"

    def test_bedrock_defaults(self):
        opts = Options(
            generation_provider="bedrock",
            generation_model="eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
            embedding_provider="bedrock",
            embedding_model="amazon.titan-embed-text-v2:0",
            vision_provider="bedrock",
            vision_model="eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
        )
        assert opts.generation_provider == "bedrock"

    def test_cross_provider_mixing(self):
        """OpenAI for generation, Bedrock for embedding is valid."""
        opts = Options(
            generation_provider="openai",
            generation_model="gpt-4o",
            embedding_provider="bedrock",
            embedding_model="amazon.titan-embed-text-v2:0",
            vision_provider="openai",
            vision_model="gpt-4o",
        )
        assert opts.embedding_provider == "bedrock"


class TestInvalidModelCombinations:
    """Test that invalid provider+model combos are rejected."""

    def test_nonexistent_generation_model(self):
        with pytest.raises(ValidationError, match="generation_model"):
            Options(
                generation_provider="openai",
                generation_model="gpt-99",
                embedding_provider="openai",
                embedding_model="text-embedding-3-small",
                vision_provider="openai",
                vision_model="gpt-4o",
            )

    def test_nonexistent_embedding_model(self):
        with pytest.raises(ValidationError, match="embedding_model"):
            Options(
                generation_provider="openai",
                generation_model="gpt-4o",
                embedding_provider="openai",
                embedding_model="nonexistent-embed",
                vision_provider="openai",
                vision_model="gpt-4o",
            )

    def test_nonexistent_vision_model(self):
        with pytest.raises(ValidationError, match="vision_model"):
            Options(
                generation_provider="openai",
                generation_model="gpt-4o",
                embedding_provider="openai",
                embedding_model="text-embedding-3-small",
                vision_provider="openai",
                vision_model="nonexistent-vision",
            )

    def test_wrong_capability_embedding_as_generation(self):
        """An embedding model should not be accepted for generation."""
        with pytest.raises(ValidationError, match="generation_model"):
            Options(
                generation_provider="openai",
                generation_model="text-embedding-3-small",
                embedding_provider="openai",
                embedding_model="text-embedding-3-small",
                vision_provider="openai",
                vision_model="gpt-4o",
            )

    def test_wrong_capability_generation_as_embedding(self):
        """A generation model should not be accepted for embedding."""
        with pytest.raises(ValidationError, match="embedding_model"):
            Options(
                generation_provider="openai",
                generation_model="gpt-4o",
                embedding_provider="openai",
                embedding_model="gpt-4o",
                vision_provider="openai",
                vision_model="gpt-4o",
            )

    def test_bedrock_model_on_openai_provider(self):
        """A Bedrock model ID should not be accepted for OpenAI provider."""
        with pytest.raises(ValidationError, match="generation_model"):
            Options(
                generation_provider="openai",
                generation_model="eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
                embedding_provider="openai",
                embedding_model="text-embedding-3-small",
                vision_provider="openai",
                vision_model="gpt-4o",
            )
