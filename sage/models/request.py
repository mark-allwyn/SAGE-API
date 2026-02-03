"""Pydantic models for API request validation."""

from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..config import get_settings


class ContentItem(BaseModel):
    """Content item for a product concept (text or image)."""

    type: str  # "image" or "text"
    data: str  # base64 for image, string for text
    label: str | None = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ("image", "text"):
            raise ValueError('type must be "image" or "text"')
        return v


class Concept(BaseModel):
    """Product concept to be tested."""

    name: str
    content: list[ContentItem]
    metadata: dict[str, Any] | None = None

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: list[ContentItem]) -> list[ContentItem]:
        if len(v) == 0:
            raise ValueError("At least one content item is required")
        return v


class Question(BaseModel):
    """Survey question with SSR reference sets."""

    id: str
    text: str
    weight: float
    ssr_reference_sets: list[list[str]]  # 6 sets of 5 anchors

    @field_validator("ssr_reference_sets")
    @classmethod
    def validate_reference_sets(cls, v: list[list[str]]) -> list[list[str]]:
        if len(v) != 6:
            raise ValueError("Must have exactly 6 reference sets")
        for i, ref_set in enumerate(v):
            if len(ref_set) != 5:
                raise ValueError(f"Reference set {i} must have exactly 5 anchors")
        return v

    @field_validator("weight")
    @classmethod
    def validate_weight(cls, v: float) -> float:
        if v < 0 or v > 1:
            raise ValueError("Weight must be between 0 and 1")
        return v


class SurveyConfig(BaseModel):
    """Survey configuration with questions."""

    questions: list[Question]

    @field_validator("questions")
    @classmethod
    def validate_weights(cls, v: list[Question]) -> list[Question]:
        if len(v) == 0:
            raise ValueError("At least one question is required")
        total_weight = sum(q.weight for q in v)
        if not (0.99 <= total_weight <= 1.01):
            raise ValueError(f"Question weights must sum to 1.0, got {total_weight}")
        return v


def _settings():
    return get_settings()


class Options(BaseModel):
    """Configuration options for LLM providers and models."""

    # LLM Generation Settings
    generation_provider: str = Field(default_factory=lambda: _settings().default_generation_provider)
    generation_model: str = Field(default_factory=lambda: _settings().default_generation_model)
    generation_temperature: float = Field(default_factory=lambda: _settings().default_temperature)

    # Embedding Settings (for SSR)
    embedding_provider: str = Field(default_factory=lambda: _settings().default_embedding_provider)
    embedding_model: str = Field(default_factory=lambda: _settings().default_embedding_model)

    # Vision Settings (for image processing)
    vision_provider: str = Field(default_factory=lambda: _settings().default_vision_provider)
    vision_model: str = Field(default_factory=lambda: _settings().default_vision_model)

    @field_validator("generation_provider", "embedding_provider", "vision_provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        if v not in ("openai", "bedrock"):
            raise ValueError('provider must be "openai" or "bedrock"')
        return v

    @field_validator("generation_temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        if v < 0 or v > 2:
            raise ValueError("Temperature must be between 0 and 2")
        return v


class TestConceptRequest(BaseModel):
    """Request model for testing a product concept."""

    personas: list[dict[str, Any]]  # Flexible schema, only persona_id required
    concept: Concept
    survey_config: SurveyConfig
    threshold: float = Field(ge=0, le=1)
    filters: list[str] = []
    verbose: bool = True
    output_dataset: bool = False
    include_report: bool = False
    options: Options = Options()

    @field_validator("personas")
    @classmethod
    def validate_personas(cls, v: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if len(v) == 0:
            raise ValueError("At least one persona is required")
        ids = [p.get("persona_id") for p in v]
        if None in ids:
            raise ValueError("All personas must have a persona_id")
        if len(ids) != len(set(ids)):
            raise ValueError("All persona_ids must be unique")
        return v
