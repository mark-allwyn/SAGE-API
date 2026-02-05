"""Tests for the Orchestrator - filter-before-generate behavior."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from sage.models.request import (
    Concept,
    ContentItem,
    Options,
    Question,
    SurveyConfig,
    TestConceptRequest,
)
from sage.services.orchestrator import Orchestrator


def _make_request(personas, filters=None):
    """Build a TestConceptRequest with given personas and filters."""
    return TestConceptRequest(
        personas=personas,
        concept=Concept(
            name="Test",
            content=[ContentItem(type="text", data="A product.")],
        ),
        survey_config=SurveyConfig(
            questions=[
                Question(
                    id="q1",
                    text="Would you buy this?",
                    weight=1.0,
                    ssr_reference_sets=[["a", "b", "c", "d", "e"]] * 6,
                )
            ]
        ),
        threshold=0.7,
        filters=filters or [],
        options=Options(
            generation_provider="openai",
            generation_model="gpt-4o",
            embedding_provider="openai",
            embedding_model="text-embedding-3-small",
            vision_provider="openai",
            vision_model="gpt-4o",
        ),
    )


def _mock_response(persona_id):
    """Create a mock persona response dict."""
    return {
        "persona_id": persona_id,
        "responses": {
            "q1": {"raw_text": "Great product", "pmf": [0.1, 0.1, 0.2, 0.3, 0.3], "mean": 3.6}
        },
    }


class TestFilterBeforeGenerate:
    """Test that filters are applied before LLM generation."""

    @pytest.mark.asyncio
    async def test_filters_reduce_personas_before_generation(self):
        personas = [
            {"persona_id": "p1", "age": 25, "gender": "F"},
            {"persona_id": "p2", "age": 45, "gender": "M"},
            {"persona_id": "p3", "age": 35, "gender": "F"},
        ]
        request = _make_request(personas, filters=["gender=F"])

        orchestrator = Orchestrator()

        with patch.object(
            orchestrator, "_generate_all_responses", new_callable=AsyncMock
        ) as mock_gen:
            mock_gen.return_value = [_mock_response("p1"), _mock_response("p3")]

            result = await orchestrator.process_request(request)

            # Should only pass 2 matched personas to generation, not all 3
            call_args = mock_gen.call_args
            generated_personas = call_args[0][2]  # 3rd positional arg is personas
            assert len(generated_personas) == 2
            assert all(p["gender"] == "F" for p in generated_personas)

    @pytest.mark.asyncio
    async def test_no_filter_passes_all_personas(self):
        personas = [
            {"persona_id": "p1", "age": 25},
            {"persona_id": "p2", "age": 45},
        ]
        request = _make_request(personas, filters=[])

        orchestrator = Orchestrator()

        with patch.object(
            orchestrator, "_generate_all_responses", new_callable=AsyncMock
        ) as mock_gen:
            mock_gen.return_value = [_mock_response("p1"), _mock_response("p2")]

            result = await orchestrator.process_request(request)

            call_args = mock_gen.call_args
            generated_personas = call_args[0][2]
            assert len(generated_personas) == 2

    @pytest.mark.asyncio
    async def test_empty_filter_result_raises(self):
        personas = [
            {"persona_id": "p1", "age": 25},
        ]
        request = _make_request(personas, filters=["age>100"])

        orchestrator = Orchestrator()

        with pytest.raises(ValueError, match="No personas matched"):
            await orchestrator.process_request(request)

    @pytest.mark.asyncio
    async def test_personas_total_reflects_pre_filter_count(self):
        personas = [
            {"persona_id": "p1", "age": 25, "gender": "F"},
            {"persona_id": "p2", "age": 45, "gender": "M"},
            {"persona_id": "p3", "age": 35, "gender": "F"},
        ]
        request = _make_request(personas, filters=["gender=F"])
        request.verbose = True

        orchestrator = Orchestrator()

        with patch.object(
            orchestrator, "_generate_all_responses", new_callable=AsyncMock
        ) as mock_gen:
            mock_gen.return_value = [_mock_response("p1"), _mock_response("p3")]

            result = await orchestrator.process_request(request)

            assert result.personas_total == 3
            assert result.personas_matched == 2
