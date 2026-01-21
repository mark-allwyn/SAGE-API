"""Scoring engine for aggregating scores and evaluating against threshold."""

from typing import Any

import numpy as np

from ..models.request import Question
from ..models.response import CriteriaBreakdown, QuestionMetrics, ResultSummary


class ScoringEngine:
    """Aggregate scores and evaluate against threshold."""

    def calculate_metrics(
        self,
        responses: list[dict[str, Any]],
        questions: list[Question],
        match_flags: list[bool],
    ) -> dict[str, QuestionMetrics]:
        """
        Calculate metrics for each question using only matched personas.

        Args:
            responses: List of response dictionaries from personas
            questions: List of survey questions
            match_flags: Boolean list indicating which personas matched filters

        Returns:
            Dictionary mapping question_id to QuestionMetrics
        """
        metrics = {}

        for question in questions:
            q_id = question.id

            # Get means for matched personas only
            means = [
                r["responses"][q_id]["mean"]
                for r, matched in zip(responses, match_flags)
                if matched
            ]

            if not means:
                raise ValueError("No personas matched the filters")

            # Convert means to discrete Likert for distribution
            discrete = [round(m) for m in means]
            # Clamp to valid Likert range
            discrete = [max(1, min(5, d)) for d in discrete]

            metrics[q_id] = QuestionMetrics(
                n=len(means),
                mean=round(float(np.mean(means)), 2),
                median=round(float(np.median(means)), 2),
                std_dev=round(float(np.std(means)), 2),
                top_2_box=round(sum(1 for m in means if m >= 4) / len(means), 2),
                bottom_2_box=round(sum(1 for m in means if m <= 2) / len(means), 2),
                distribution={str(i): discrete.count(i) for i in range(1, 6)},
            )

        return metrics

    def calculate_composite_score(
        self,
        metrics: dict[str, QuestionMetrics],
        questions: list[Question],
    ) -> tuple[float, list[CriteriaBreakdown]]:
        """
        Calculate composite score and breakdown.

        The composite score is a weighted sum of normalized scores.
        Normalization maps Likert scale (1-5) to (0-1).

        Args:
            metrics: Dictionary of QuestionMetrics by question_id
            questions: List of survey questions

        Returns:
            composite_score: Weighted sum of normalized scores (0-1)
            breakdown: Per-question breakdown
        """
        breakdown = []
        composite = 0.0

        for question in questions:
            q_id = question.id
            raw_mean = metrics[q_id].mean

            # Normalize: (mean - 1) / 4 maps 1-5 to 0-1
            normalized = (raw_mean - 1) / 4

            # Apply weight
            contribution = normalized * question.weight
            composite += contribution

            breakdown.append(
                CriteriaBreakdown(
                    question_id=q_id,
                    weight=question.weight,
                    raw_mean=raw_mean,
                    normalized=round(normalized, 3),
                    contribution=round(contribution, 3),
                )
            )

        return round(composite, 3), breakdown

    def evaluate_threshold(
        self,
        composite_score: float,
        threshold: float,
    ) -> ResultSummary:
        """
        Evaluate composite score against threshold.

        Args:
            composite_score: Weighted normalized score (0-1)
            threshold: Pass/fail threshold (0-1)

        Returns:
            ResultSummary with pass/fail determination
        """
        passed = composite_score >= threshold
        margin = round(composite_score - threshold, 3)

        if passed:
            reason = f"PASS: Composite score {composite_score} meets threshold {threshold}"
        else:
            reason = f"FAIL: Composite score {composite_score} is below threshold {threshold}"

        return ResultSummary(
            passed=passed,
            composite_score=composite_score,
            threshold=threshold,
            margin=margin,
            reason=reason,
        )
