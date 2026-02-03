"""Orchestrator that coordinates the entire synthetic consumer testing pipeline."""

import asyncio
import logging
import time
import uuid
from typing import Any

from ..config import get_settings

logger = logging.getLogger(__name__)

from ..models.request import Concept, Question, TestConceptRequest
from ..models.response import FullResponse, Meta, MinimalResponse, ProviderInfo
from .filter_engine import FilterEngine
from .llm_service import LLMService
from .report_generator import ReportGenerator
from .scoring_engine import ScoringEngine
from .ssr_engine import SSREngine


class Orchestrator:
    """Coordinates the entire pipeline for concept testing."""

    def __init__(self):
        """Initialize orchestrator with filter, scoring, and report engines."""
        self.filter_engine = FilterEngine()
        self.scoring_engine = ScoringEngine()
        self.report_generator = ReportGenerator()
        self.settings = get_settings()

    async def process_request(
        self,
        request: TestConceptRequest,
    ) -> FullResponse | MinimalResponse:
        """
        Process a concept test request.

        Pipeline:
        1. Create LLM service with specified providers/models
        2. Generate responses for all personas
        3. Apply filters to personas
        4. Calculate metrics for filtered personas
        5. Calculate composite score
        6. Evaluate against threshold

        Args:
            request: TestConceptRequest with personas, concept, and config

        Returns:
            FullResponse if verbose=True, MinimalResponse otherwise
        """
        start_time = time.time()
        request_id = str(uuid.uuid4())[:8]

        logger.info(
            "[%s] Starting concept test: %s (%d personas, %d questions)",
            request_id,
            request.concept.name,
            len(request.personas),
            len(request.survey_config.questions),
        )

        # Validate filters
        filter_errors = self.filter_engine.validate_filters(request.filters)
        if filter_errors:
            raise ValueError(f"Invalid filters: {'; '.join(filter_errors)}")

        # Create LLM service with specified providers/models
        llm_service = LLMService(request.options)

        # Create SSR engine with the LLM service
        ssr_engine = SSREngine(
            llm_service,
            temperature=self.settings.ssr_softmax_temperature,
        )

        # Step 1: Generate responses for all personas
        responses = await self._generate_all_responses(
            llm_service,
            ssr_engine,
            request.personas,
            request.concept,
            request.survey_config.questions,
        )

        # Step 2: Apply filters
        _, match_flags = self.filter_engine.apply_filters(
            request.personas,
            request.filters,
        )
        personas_matched = sum(match_flags)

        if personas_matched == 0:
            raise ValueError("No personas matched the specified filters")

        # Step 3: Calculate metrics (using filtered personas)
        metrics = self.scoring_engine.calculate_metrics(
            responses,
            request.survey_config.questions,
            match_flags,
        )

        # Step 4: Calculate composite score
        composite_score, breakdown = self.scoring_engine.calculate_composite_score(
            metrics,
            request.survey_config.questions,
        )

        # Step 5: Evaluate threshold
        result = self.scoring_engine.evaluate_threshold(
            composite_score,
            request.threshold,
        )

        processing_time = int((time.time() - start_time) * 1000)

        logger.info(
            "[%s] Pipeline complete in %.1fs - composite score: %.3f",
            request_id,
            processing_time / 1000,
            composite_score,
        )

        # Build response based on verbose flag
        if not request.verbose:
            return MinimalResponse(
                passed=result.passed,
                composite_score=result.composite_score,
                threshold=result.threshold,
            )

        # Build full response
        response = FullResponse(
            result=result,
            filters_applied=request.filters,
            personas_total=len(request.personas),
            personas_matched=personas_matched,
            criteria_breakdown=breakdown,
            metrics=metrics,
            meta=Meta(
                request_id=request_id,
                concept_name=request.concept.name,
                processing_time_ms=processing_time,
                providers=ProviderInfo(
                    generation=f"{request.options.generation_provider}/{request.options.generation_model}",
                    embedding=f"{request.options.embedding_provider}/{request.options.embedding_model}",
                    vision=f"{request.options.vision_provider}/{request.options.vision_model}",
                ),
            ),
        )

        # Add dataset if requested
        if request.output_dataset:
            response.dataset = self._build_dataset(
                request.personas,
                responses,
                match_flags,
                request.survey_config.questions,
            )

        # Generate report if requested
        if request.include_report:
            response.report = self.report_generator.generate_report(
                result=result,
                concept_name=request.concept.name,
                personas_total=len(request.personas),
                personas_matched=personas_matched,
                criteria_breakdown=breakdown,
                metrics=metrics,
                meta=response.meta,
                dataset=response.dataset,
                filters_applied=request.filters if request.filters else None,
                questions=request.survey_config.questions,
                concept=request.concept,
            )

        return response

    async def _generate_all_responses(
        self,
        llm_service: LLMService,
        ssr_engine: SSREngine,
        personas: list[dict[str, Any]],
        concept: Concept,
        questions: list[Question],
    ) -> list[dict[str, Any]]:
        """
        Generate responses for all personas and questions.

        Processes personas in batches for efficiency and rate limiting.

        Args:
            llm_service: LLM service for generation
            ssr_engine: SSR engine for mapping to Likert
            personas: List of persona dictionaries
            concept: Product concept
            questions: Survey questions

        Returns:
            List of response dictionaries for each persona
        """
        total = len(personas)
        completed = 0
        semaphore = asyncio.Semaphore(self.settings.concurrency_limit)

        logger.info(
            "Processing %d personas (concurrency limit: %d)",
            total,
            self.settings.concurrency_limit,
        )

        async def _process_with_limit(persona):
            nonlocal completed
            async with semaphore:
                result = await self._process_single_persona(
                    llm_service, ssr_engine, persona, concept, questions
                )
                completed += 1
                logger.info(
                    "Persona %s complete (%d/%d)",
                    persona.get("persona_id", "?"),
                    completed,
                    total,
                )
                return result

        responses = await asyncio.gather(
            *[_process_with_limit(p) for p in personas]
        )

        return list(responses)

    async def _process_single_persona(
        self,
        llm_service: LLMService,
        ssr_engine: SSREngine,
        persona: dict[str, Any],
        concept: Concept,
        questions: list[Question],
    ) -> dict[str, Any]:
        """
        Process all questions for a single persona.

        For each question:
        1. Generate LLM response (uses vision provider if images present)
        2. Map response to Likert PMF using SSR

        Args:
            llm_service: LLM service for generation
            ssr_engine: SSR engine for mapping to Likert
            persona: Persona dictionary
            concept: Product concept
            questions: Survey questions

        Returns:
            Response dictionary with persona_id and responses
        """
        async def _process_question(question: Question):
            raw_text = await llm_service.generate_response(persona, concept, question)
            pmf, mean = await ssr_engine.map_response_to_likert(
                raw_text,
                question.ssr_reference_sets,
            )
            return question.id, {
                "raw_text": raw_text,
                "pmf": [round(p, 3) for p in pmf],
                "mean": round(mean, 2),
            }

        results = await asyncio.gather(*[_process_question(q) for q in questions])

        persona_responses: dict[str, Any] = {
            "persona_id": persona["persona_id"],
            "responses": {q_id: data for q_id, data in results},
        }

        return persona_responses

    def _build_dataset(
        self,
        personas: list[dict[str, Any]],
        responses: list[dict[str, Any]],
        match_flags: list[bool],
        questions: list[Question],
    ) -> list[dict[str, Any]]:
        """
        Build flat dataset with personas + results.

        Args:
            personas: List of persona dictionaries
            responses: List of response dictionaries
            match_flags: Boolean flags for filter matches
            questions: Survey questions

        Returns:
            Flat dataset with persona attributes and response data
        """
        dataset = []

        for persona, response, matched in zip(personas, responses, match_flags):
            row = {**persona, "matched_filter": matched}

            for question in questions:
                q_id = question.id
                q_response = response["responses"][q_id]
                row[f"{q_id}_text"] = q_response["raw_text"]
                row[f"{q_id}_pmf"] = q_response["pmf"]
                row[f"{q_id}_mean"] = q_response["mean"]

            dataset.append(row)

        return dataset
