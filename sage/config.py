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
    default_generation_provider: str = "openai"
    default_generation_model: str = "gpt-4o"
    default_embedding_provider: str = "openai"
    default_embedding_model: str = "text-embedding-3-small"
    default_vision_provider: str = "openai"
    default_vision_model: str = "gpt-4o"
    default_temperature: float = 0.7

    # SSR Configuration
    ssr_softmax_temperature: float = 0.5  # Temperature for softmax in SSR mapping

    # Processing Configuration
    batch_size: int = 10  # Number of personas to process in parallel
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
            "anthropic.claude-3-opus-20240229-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-3-5-sonnet-20240620-v1:0",
        ],
        "embedding": [
            "amazon.titan-embed-text-v2:0",
            "amazon.titan-embed-text-v1",
        ],
        "vision": [
            "anthropic.claude-3-opus-20240229-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-3-5-sonnet-20240620-v1:0",
        ],
    },
}
