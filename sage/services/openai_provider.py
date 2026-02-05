"""OpenAI provider implementations for generation, embedding, and vision."""

from collections import OrderedDict

from openai import APIError, AsyncOpenAI

from ..exceptions import ProviderError
from .llm_provider import EmbeddingProvider, GenerationProvider, VisionProvider


class OpenAIGenerationProvider(GenerationProvider):
    """OpenAI provider for text generation."""

    def __init__(self, model: str = "gpt-4o"):
        """
        Initialize OpenAI generation provider.

        Args:
            model: OpenAI model identifier
        """
        self.client = AsyncOpenAI()
        self.model = model

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """Generate text response using OpenAI."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=500,
            )
            return response.choices[0].message.content or ""
        except APIError as e:
            raise ProviderError("openai", str(e)) from e


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI provider for embeddings."""

    def __init__(self, model: str = "text-embedding-3-small"):
        """
        Initialize OpenAI embedding provider.

        Args:
            model: OpenAI embedding model identifier
        """
        self.client = AsyncOpenAI()
        self.model = model
        self._cache: OrderedDict[tuple[str, ...], list[list[float]]] = OrderedDict()
        self._max_cache_size = 256

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts."""
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=texts,
            )
            return [d.embedding for d in response.data]
        except APIError as e:
            raise ProviderError("openai", str(e)) from e

    async def embed_single(self, text: str) -> list[float]:
        """Embed a single text."""
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=text,
            )
            return response.data[0].embedding
        except APIError as e:
            raise ProviderError("openai", str(e)) from e

    async def embed_with_cache(self, texts: list[str]) -> list[list[float]]:
        """Embed texts with LRU caching (for anchor texts)."""
        cache_key = tuple(texts)
        if cache_key in self._cache:
            self._cache.move_to_end(cache_key)
        else:
            self._cache[cache_key] = await self.embed(texts)
            if len(self._cache) > self._max_cache_size:
                self._cache.popitem(last=False)
        return self._cache[cache_key]


class OpenAIVisionProvider(VisionProvider):
    """OpenAI provider for vision (multimodal) tasks."""

    def __init__(self, model: str = "gpt-4o"):
        """
        Initialize OpenAI vision provider.

        Args:
            model: OpenAI vision-capable model identifier
        """
        self.client = AsyncOpenAI()
        self.model = model

    async def generate_with_images(
        self,
        system_prompt: str,
        user_prompt: str,
        images: list[dict],
        temperature: float = 0.7,
    ) -> str:
        """Generate text response with images using OpenAI."""
        # Build multimodal content
        content: list[dict] = []

        # Add images first
        for img in images:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{img['media_type']};base64,{img['data']}"},
                }
            )

        # Add text prompt
        content.append({"type": "text", "text": user_prompt})

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content},
                ],
                temperature=temperature,
                max_tokens=500,
            )
            return response.choices[0].message.content or ""
        except APIError as e:
            raise ProviderError("openai", str(e)) from e
