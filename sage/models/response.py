"""Pydantic models for API response validation."""

from typing import Any

from pydantic import BaseModel


class ResultSummary(BaseModel):
    """Summary of the concept test result."""

    passed: bool
    composite_score: float
    threshold: float
    margin: float
    reason: str


class CriteriaBreakdown(BaseModel):
    """Breakdown of scoring for a single question."""

    question_id: str
    weight: float
    raw_mean: float
    normalized: float
    contribution: float


class QuestionMetrics(BaseModel):
    """Statistical metrics for a single question."""

    n: int
    mean: float
    median: float
    std_dev: float
    top_2_box: float
    bottom_2_box: float
    distribution: dict[str, int]


class ProviderInfo(BaseModel):
    """Information about providers used."""

    generation: str
    embedding: str
    vision: str


class Meta(BaseModel):
    """Metadata about the request processing."""

    request_id: str
    concept_name: str
    processing_time_ms: int
    providers: ProviderInfo | None = None


class MinimalResponse(BaseModel):
    """Minimal response (verbose=false)."""

    passed: bool
    composite_score: float
    threshold: float


class FullResponse(BaseModel):
    """Full response (verbose=true)."""

    result: ResultSummary
    filters_applied: list[str]
    personas_total: int
    personas_matched: int
    criteria_breakdown: list[CriteriaBreakdown]
    metrics: dict[str, QuestionMetrics]
    dataset: list[dict[str, Any]] | None = None  # if output_dataset=true
    meta: Meta
