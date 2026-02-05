"""Pydantic models for API response validation."""

from typing import Any

from pydantic import BaseModel, Field


class ResultSummary(BaseModel):
    """Summary of the concept test result."""

    passed: bool
    composite_score: float = Field(ge=0, le=1)
    threshold: float = Field(ge=0, le=1)
    margin: float
    reason: str


class CriteriaBreakdown(BaseModel):
    """Breakdown of scoring for a single question."""

    question_id: str
    weight: float = Field(ge=0, le=1)
    raw_mean: float = Field(ge=1, le=5)
    normalized: float = Field(ge=0, le=1)
    contribution: float = Field(ge=0)


class QuestionMetrics(BaseModel):
    """Statistical metrics for a single question."""

    n: int = Field(ge=0)
    mean: float = Field(ge=1, le=5)
    median: float = Field(ge=1, le=5)
    std_dev: float = Field(ge=0)
    top_2_box: float = Field(ge=0, le=1)
    bottom_2_box: float = Field(ge=0, le=1)
    distribution: dict[str, int]


class ProviderInfo(BaseModel):
    """Information about providers used."""

    generation: str
    embedding: str
    vision: str
    video: str | None = None


class Meta(BaseModel):
    """Metadata about the request processing."""

    request_id: str
    concept_name: str
    processing_time_ms: int = Field(ge=0)
    providers: ProviderInfo | None = None


class MinimalResponse(BaseModel):
    """Minimal response (verbose=false)."""

    passed: bool
    composite_score: float = Field(ge=0, le=1)
    threshold: float = Field(ge=0, le=1)


class FullResponse(BaseModel):
    """Full response (verbose=true)."""

    result: ResultSummary
    filters_applied: list[str]
    personas_total: int
    personas_matched: int
    criteria_breakdown: list[CriteriaBreakdown]
    metrics: dict[str, QuestionMetrics]
    dataset: list[dict[str, Any]] | None = None  # if output_dataset=true
    report: str | None = None  # if include_report=true
    meta: Meta
