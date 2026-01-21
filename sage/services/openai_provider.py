"""OpenAI provider implementations for generation, embedding, and vision."""

from openai import AsyncOpenAI

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
        self._cache: dict[tuple[str, ...], list[list[float]]] = {}

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts."""
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [d.embedding for d in response.data]

    async def embed_single(self, text: str) -> list[float]:
        """Embed a single text."""
        response = await self.client.embeddings.create(
            model=self.model,
            input=text,
        )
        return response.data[0].embedding

    async def embed_with_cache(self, texts: list[str]) -> list[list[float]]:
        """Embed texts with caching (for anchor texts)."""
        cache_key = tuple(texts)
        if cache_key not in self._cache:
            self._cache[cache_key] = await self.embed(texts)
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
