"""Configuration and environment variables for the Synthetic Consumer Testing API."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # AWS/Bedrock Configuration
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")

    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Default LLM Settings
    default_generation_provider: str = os.getenv("DEFAULT_GENERATION_PROVIDER", "openai")
    default_generation_model: str = os.getenv("DEFAULT_GENERATION_MODEL", "gpt-4o")
    default_embedding_provider: str = os.getenv("DEFAULT_EMBEDDING_PROVIDER", "openai")
    default_embedding_model: str = os.getenv("DEFAULT_EMBEDDING_MODEL", "text-embedding-3-small")
    default_vision_provider: str = os.getenv("DEFAULT_VISION_PROVIDER", "openai")
    default_vision_model: str = os.getenv("DEFAULT_VISION_MODEL", "gpt-4o")
    default_temperature: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))

    # SSR Configuration
    # Temperature for PMF sharpening: p(r,T) ∝ p(r)^(1/T)
    # Paper uses T=1 (no sharpening). Lower T = sharper distribution.
    ssr_softmax_temperature: float = 1.0

    # Processing Configuration
    batch_size: int = int(os.getenv("BATCH_SIZE", "10"))
    concurrency_limit: int = int(os.getenv("CONCURRENCY_LIMIT", "20"))
    max_tokens: int = 500  # Max tokens for LLM responses

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Supported models by provider
SUPPORTED_MODELS = {
    "openai": {
        "generation": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo",
        ],
        "embedding": [
            "text-embedding-3-small",
            "text-embedding-3-large",
            "text-embedding-ada-002",
        ],
        "vision": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
        ],
    },
    "bedrock": {
        "generation": [
            # EU inference profiles (for eu-central-1 region)
            "eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
            "eu.anthropic.claude-sonnet-4-20250514-v1:0",
            "eu.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "eu.anthropic.claude-haiku-4-5-20251001-v1:0",
            # Direct model IDs (available in eu-central-1)
            "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
        ],
        "embedding": [
            "amazon.titan-embed-text-v2:0",
            "amazon.titan-embed-text-v1",
        ],
        "vision": [
            # EU inference profiles (for eu-central-1 region)
            "eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
            "eu.anthropic.claude-sonnet-4-20250514-v1:0",
            "eu.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "eu.anthropic.claude-haiku-4-5-20251001-v1:0",
            # Direct model IDs (available in eu-central-1)
            "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
        ],
    },
}
