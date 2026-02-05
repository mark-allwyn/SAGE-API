"""Amazon Bedrock provider implementations for generation, embedding, and vision.

Supports multiple model families: Anthropic Claude, Amazon Nova, Mistral, Meta Llama.
The model family is detected from the model ID and the appropriate API format is used.
"""

import asyncio
import base64
import json
from collections import OrderedDict
from functools import partial
from typing import TYPE_CHECKING

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from ..config import get_settings
from ..exceptions import ConfigurationError, ProviderError
from .llm_provider import EmbeddingProvider, GenerationProvider, VisionProvider

if TYPE_CHECKING:
    from .video_downloader import VideoSource


def _detect_family(model_id: str) -> str:
    """Detect the model family from a Bedrock model ID."""
    model_lower = model_id.lower()
    if "anthropic" in model_lower or "claude" in model_lower:
        return "anthropic"
    if "nova" in model_lower:
        return "nova"
    if "mistral" in model_lower or "pixtral" in model_lower:
        return "mistral"
    if "meta" in model_lower or "llama" in model_lower:
        return "llama"
    if "cohere" in model_lower:
        return "cohere"
    if "titan" in model_lower:
        return "titan"
    if "twelvelabs" in model_lower or "pegasus" in model_lower:
        return "twelvelabs"
    raise ConfigurationError(f"Unknown Bedrock model family: {model_id}")


class BedrockGenerationProvider(GenerationProvider):
    """Amazon Bedrock provider for text generation.

    Supports Anthropic Claude, Amazon Nova, Mistral, and Meta Llama models.
    """

    def __init__(self, model: str = "eu.anthropic.claude-sonnet-4-5-20250929-v1:0"):
        settings = get_settings()
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region,
            config=Config(read_timeout=300),
        )
        self.model = model
        self.family = _detect_family(model)

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """Generate text response using the appropriate API format for the model."""
        body = self._build_request(system_prompt, user_prompt, temperature)

        try:
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
            return self._parse_response(response_body)
        except (ClientError, BotoCoreError) as e:
            raise ProviderError("bedrock", str(e)) from e
        except (KeyError, json.JSONDecodeError) as e:
            raise ProviderError("bedrock", f"Failed to parse response: {e}") from e

    def _build_request(
        self, system_prompt: str, user_prompt: str, temperature: float
    ) -> dict:
        if self.family == "anthropic":
            return {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "temperature": temperature,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_prompt}],
            }
        if self.family == "nova":
            return {
                "system": [{"text": system_prompt}],
                "messages": [
                    {"role": "user", "content": [{"text": user_prompt}]}
                ],
                "inferenceConfig": {
                    "max_new_tokens": 500,
                    "temperature": temperature,
                },
            }
        if self.family == "mistral":
            return {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 500,
                "temperature": temperature,
            }
        if self.family == "llama":
            prompt = (
                f"<|begin_of_text|>"
                f"<|start_header_id|>system<|end_header_id|>\n{system_prompt}<|eot_id|>"
                f"<|start_header_id|>user<|end_header_id|>\n{user_prompt}<|eot_id|>"
                f"<|start_header_id|>assistant<|end_header_id|>\n"
            )
            return {
                "prompt": prompt,
                "max_gen_len": 500,
                "temperature": temperature,
            }
        raise ConfigurationError(f"Unsupported generation family: {self.family}")

    def _parse_response(self, response_body: dict) -> str:
        if self.family == "anthropic":
            return response_body["content"][0]["text"]
        if self.family == "nova":
            return response_body["output"]["message"]["content"][0]["text"]
        if self.family == "mistral":
            return response_body["choices"][0]["message"]["content"]
        if self.family == "llama":
            return response_body["generation"]
        raise ConfigurationError(f"Unsupported generation family: {self.family}")


class BedrockEmbeddingProvider(EmbeddingProvider):
    """Amazon Bedrock provider for embeddings.

    Supports Amazon Titan (v1, v2) and Cohere Embed models.
    """

    _embed_semaphore: asyncio.Semaphore | None = None

    def __init__(self, model: str = "amazon.titan-embed-text-v2:0"):
        settings = get_settings()
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region,
        )
        self.model = model
        self.family = _detect_family(model)
        self._cache: OrderedDict[tuple[str, ...], list[list[float]]] = OrderedDict()
        self._max_cache_size = 256

    @classmethod
    def _get_semaphore(cls) -> asyncio.Semaphore:
        if cls._embed_semaphore is None:
            cls._embed_semaphore = asyncio.Semaphore(10)
        return cls._embed_semaphore

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts."""
        if self.family == "cohere":
            return await self._embed_cohere_batch(texts)
        # Parallelize Titan requests with concurrency limit
        sem = self._get_semaphore()

        async def _limited_embed(text: str) -> list[float]:
            async with sem:
                return await self.embed_single(text)

        embeddings = await asyncio.gather(
            *[_limited_embed(text) for text in texts]
        )
        return list(embeddings)

    async def embed_single(self, text: str) -> list[float]:
        """Embed a single text."""
        if self.family == "cohere":
            results = await self._embed_cohere_batch([text])
            return results[0]
        return await self._embed_titan(text)

    async def _embed_titan(self, text: str) -> list[float]:
        """Embed using Amazon Titan."""
        payload: dict = {"inputText": text}

        # Titan v2 supports dimensions and normalize params; v1 does not
        if "v2" in self.model:
            payload["dimensions"] = 1024
            payload["normalize"] = True

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                partial(
                    self.client.invoke_model,
                    modelId=self.model,
                    body=json.dumps(payload),
                ),
            )
            response_body = json.loads(response["body"].read())
            return response_body["embedding"]
        except (ClientError, BotoCoreError) as e:
            raise ProviderError("bedrock", str(e)) from e
        except (KeyError, json.JSONDecodeError) as e:
            raise ProviderError("bedrock", f"Failed to parse response: {e}") from e

    async def _embed_cohere_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed using Cohere (supports batch natively)."""
        payload = {
            "texts": texts,
            "input_type": "search_document",
        }

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                partial(
                    self.client.invoke_model,
                    modelId=self.model,
                    body=json.dumps(payload),
                ),
            )
            response_body = json.loads(response["body"].read())
            return response_body["embeddings"]
        except (ClientError, BotoCoreError) as e:
            raise ProviderError("bedrock", str(e)) from e
        except (KeyError, json.JSONDecodeError) as e:
            raise ProviderError("bedrock", f"Failed to parse response: {e}") from e

    async def embed_with_cache(self, texts: list[str]) -> list[list[float]]:
        """Embed texts with LRU caching."""
        cache_key = tuple(texts)
        if cache_key in self._cache:
            self._cache.move_to_end(cache_key)
        else:
            self._cache[cache_key] = await self.embed(texts)
            if len(self._cache) > self._max_cache_size:
                self._cache.popitem(last=False)
        return self._cache[cache_key]


class BedrockVisionProvider(VisionProvider):
    """Amazon Bedrock provider for vision/multimodal.

    Supports Anthropic Claude, Amazon Nova, Mistral Pixtral, and Twelve Labs Pegasus.
    Images are passed as dicts with 'data' (base64) and 'media_type' keys.
    Videos are passed via generate_with_video() for Pegasus models.
    """

    def __init__(self, model: str = "eu.anthropic.claude-sonnet-4-5-20250929-v1:0"):
        settings = get_settings()
        family = _detect_family(model)
        timeout = 600 if family == "twelvelabs" else 300
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region,
            config=Config(read_timeout=timeout),
        )
        self.model = model
        self.family = family

    async def generate_with_images(
        self,
        system_prompt: str,
        user_prompt: str,
        images: list[dict],
        temperature: float = 0.7,
    ) -> str:
        """Generate text response with images."""
        body = self._build_request(system_prompt, user_prompt, images, temperature)

        try:
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
            return self._parse_response(response_body)
        except (ClientError, BotoCoreError) as e:
            raise ProviderError("bedrock", str(e)) from e
        except (KeyError, json.JSONDecodeError) as e:
            raise ProviderError("bedrock", f"Failed to parse response: {e}") from e

    def _build_request(
        self,
        system_prompt: str,
        user_prompt: str,
        images: list[dict],
        temperature: float,
    ) -> dict:
        if self.family == "anthropic":
            content: list[dict] = []
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
            content.append({"type": "text", "text": user_prompt})
            return {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "temperature": temperature,
                "system": system_prompt,
                "messages": [{"role": "user", "content": content}],
            }

        if self.family == "nova":
            nova_content: list[dict] = []
            for img in images:
                # Derive format from media_type (e.g. "image/jpeg" -> "jpeg")
                fmt = img["media_type"].split("/")[-1]
                if fmt == "jpg":
                    fmt = "jpeg"
                nova_content.append(
                    {
                        "image": {
                            "format": fmt,
                            "source": {"bytes": img["data"]},
                        }
                    }
                )
            nova_content.append({"text": user_prompt})
            return {
                "system": [{"text": system_prompt}],
                "messages": [{"role": "user", "content": nova_content}],
                "inferenceConfig": {
                    "max_new_tokens": 500,
                    "temperature": temperature,
                },
            }

        if self.family == "mistral":
            mistral_content: list[dict] = []
            for img in images:
                data_uri = f"data:{img['media_type']};base64,{img['data']}"
                mistral_content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": data_uri},
                    }
                )
            mistral_content.append({"type": "text", "text": user_prompt})
            return {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": mistral_content},
                ],
                "max_tokens": 500,
                "temperature": temperature,
            }

        raise ConfigurationError(
            f"Vision not supported for model family: {self.family}"
        )

    def _parse_response(self, response_body: dict) -> str:
        if self.family == "anthropic":
            return response_body["content"][0]["text"]
        if self.family == "nova":
            return response_body["output"]["message"]["content"][0]["text"]
        if self.family == "mistral":
            return response_body["choices"][0]["message"]["content"]
        raise ConfigurationError(f"Unsupported vision family: {self.family}")

    async def generate_with_video(
        self,
        prompt: str,
        video_source: "VideoSource",
        temperature: float = 0.2,
    ) -> str:
        """Generate text response from a video using Twelve Labs Pegasus.

        Args:
            prompt: Combined system + user prompt (Pegasus uses single inputPrompt)
            video_source: Resolved VideoSource with base64 or S3 data
            temperature: Sampling temperature (Pegasus default 0.2)

        Returns:
            Generated text response
        """
        body = self._build_video_request(prompt, video_source, temperature)

        try:
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
            return self._parse_video_response(response_body)
        except (ClientError, BotoCoreError) as e:
            raise ProviderError("bedrock", str(e)) from e
        except (KeyError, json.JSONDecodeError) as e:
            raise ProviderError("bedrock", f"Failed to parse video response: {e}") from e

    def _build_video_request(
        self,
        prompt: str,
        video_source: "VideoSource",
        temperature: float,
    ) -> dict:
        """Build a Pegasus video request body."""
        from .video_downloader import VideoSource

        body: dict = {
            "inputPrompt": prompt,
            "temperature": temperature,
            "maxOutputTokens": 4096,
        }

        if video_source.source_type == "s3":
            s3_location: dict = {"uri": video_source.data}
            if video_source.s3_bucket_owner:
                s3_location["bucketOwner"] = video_source.s3_bucket_owner
            body["mediaSource"] = {"s3Location": s3_location}
        else:
            body["mediaSource"] = {"base64String": video_source.data}

        return body

    @staticmethod
    def _parse_video_response(response_body: dict) -> str:
        return response_body["message"]
