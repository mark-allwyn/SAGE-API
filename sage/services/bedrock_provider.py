"""Amazon Bedrock provider implementations for generation, embedding, and vision."""

import asyncio
import json
from functools import partial

import boto3
from botocore.config import Config

from .llm_provider import EmbeddingProvider, GenerationProvider, VisionProvider


class BedrockGenerationProvider(GenerationProvider):
    """Amazon Bedrock provider for text generation (Claude models)."""

    CLAUDE_MODELS = [
        "anthropic.claude-3-opus-20240229-v1:0",
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
    ]

    def __init__(self, model: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        """
        Initialize Bedrock generation provider.

        Args:
            model: Bedrock model identifier
        """
        self.client = boto3.client(
            "bedrock-runtime",
            config=Config(read_timeout=300),
        )
        self.model = model

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """Generate text response using Bedrock Claude."""
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
        }

        # Run synchronous boto3 call in executor
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            partial(
                self.client.invoke_model,
                modelId=self.model,
                body=json.dumps(body),
            ),
        )

        response_body = json.loads(response["body"].read())
        return response_body["content"][0]["text"]


class BedrockEmbeddingProvider(EmbeddingProvider):
    """Amazon Bedrock provider for embeddings (Titan)."""

    def __init__(self, model: str = "amazon.titan-embed-text-v2:0"):
        """
        Initialize Bedrock embedding provider.

        Args:
            model: Bedrock embedding model identifier
        """
        self.client = boto3.client("bedrock-runtime")
        self.model = model
        self._cache: dict[tuple[str, ...], list[list[float]]] = {}

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts (Titan processes one at a time)."""
        embeddings = []
        for text in texts:
            emb = await self.embed_single(text)
            embeddings.append(emb)
        return embeddings

    async def embed_single(self, text: str) -> list[float]:
        """Embed a single text."""
        body = json.dumps(
            {
                "inputText": text,
                "dimensions": 1024,  # Titan v2 supports 256, 512, 1024
                "normalize": True,
            }
        )

        # Run synchronous boto3 call in executor
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            partial(
                self.client.invoke_model,
                modelId=self.model,
                body=body,
            ),
        )

        response_body = json.loads(response["body"].read())
        return response_body["embedding"]

    async def embed_with_cache(self, texts: list[str]) -> list[list[float]]:
        """Embed texts with caching."""
        cache_key = tuple(texts)
        if cache_key not in self._cache:
            self._cache[cache_key] = await self.embed(texts)
        return self._cache[cache_key]


class BedrockVisionProvider(VisionProvider):
    """Amazon Bedrock provider for vision (Claude multimodal)."""

    def __init__(self, model: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        """
        Initialize Bedrock vision provider.

        Args:
            model: Bedrock vision-capable model identifier
        """
        self.client = boto3.client(
            "bedrock-runtime",
            config=Config(read_timeout=300),
        )
        self.model = model

    async def generate_with_images(
        self,
        system_prompt: str,
        user_prompt: str,
        images: list[dict],
        temperature: float = 0.7,
    ) -> str:
        """Generate text response with images using Bedrock Claude."""
        # Build multimodal content for Claude
        content: list[dict] = []

        # Add images
        for img in images:
            content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": img["media_type"],
                        "data": img["data"],
                    },
                }
            )

        # Add text prompt
        content.append({"type": "text", "text": user_prompt})

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [{"role": "user", "content": content}],
        }

        # Run synchronous boto3 call in executor
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            partial(
                self.client.invoke_model,
                modelId=self.model,
                body=json.dumps(body),
            ),
        )

        response_body = json.loads(response["body"].read())
        return response_body["content"][0]["text"]
