"""Report generator for creating markdown reports from test results."""

from typing import Any

from ..models.response import CriteriaBreakdown, Meta, QuestionMetrics, ResultSummary


class ReportGenerator:
    """Generates markdown reports from concept test results."""

    def generate_report(
        self,
        result: ResultSummary,
        concept_name: str,
        personas_total: int,
        personas_matched: int,
        criteria_breakdown: list[CriteriaBreakdown],
        metrics: dict[str, QuestionMetrics],
        meta: Meta,
        dataset: list[dict[str, Any]] | None = None,
        filters_applied: list[str] | None = None,
    ) -> str:
        """
        Generate a markdown report from test results.

        Args:
            result: Result summary with pass/fail and scores
            concept_name: Name of the concept tested
            personas_total: Total number of personas
            personas_matched: Number of personas after filtering
            criteria_breakdown: Breakdown by question
            metrics: Metrics per question
            meta: Request metadata
            dataset: Optional dataset with raw responses
            filters_applied: Optional list of filters

        Returns:
            Markdown formatted report string
        """
        sections = [
            self._generate_header(concept_name),
            self._generate_overview(meta, personas_total, personas_matched, filters_applied),
            self._generate_result_summary(result),
            self._generate_criteria_breakdown(criteria_breakdown),
            self._generate_insights(metrics),
            self._generate_metrics_table(metrics),
        ]

        if dataset:
            sections.append(self._generate_sample_responses(dataset))

        sections.append(self._generate_conclusions(result, metrics))

        return "\n".join(sections)

    def _generate_header(self, concept_name: str) -> str:
        """Generate report header."""
        return f"# Concept Test Report: {concept_name}\n"

    def _generate_overview(
        self,
        meta: Meta,
        personas_total: int,
        personas_matched: int,
        filters_applied: list[str] | None,
    ) -> str:
        """Generate test overview section."""
        processing_time_sec = meta.processing_time_ms / 1000
        processing_time_min = meta.processing_time_ms / 60000

        lines = [
            "## Test Overview\n",
            "| Field | Value |",
            "|-------|-------|",
            f"| **Concept Name** | {meta.concept_name} |",
            f"| **Personas Tested** | {personas_matched} of {personas_total} |",
            f"| **Processing Time** | {processing_time_sec:.1f}s (~{processing_time_min:.1f} min) |",
        ]

        if meta.providers:
            lines.append(f"| **Generation Provider** | {meta.providers.generation} |")
            lines.append(f"| **Embedding Provider** | {meta.providers.embedding} |")
            if "vision" in meta.providers.vision.lower() or "gpt-4" in meta.providers.vision.lower():
                lines.append(f"| **Vision Provider** | {meta.providers.vision} |")

        if filters_applied:
            lines.append(f"| **Filters** | {', '.join(filters_applied)} |")

        lines.append("\n---\n")
        return "\n".join(lines)

    def _generate_result_summary(self, result: ResultSummary) -> str:
        """Generate result summary section."""
        status = "PASSED" if result.passed else "FAILED"
        margin_sign = "+" if result.margin >= 0 else ""
        margin_pct = abs(result.margin) * 100
        verdict_action = "exceeded" if result.passed else "missed"

        lines = [
            f"## Overall Result: {status}\n",
            "| Metric | Value |",
            "|--------|-------|",
            f"| **Composite Score** | {result.composite_score:.3f} |",
            f"| **Threshold** | {result.threshold:.2f} |",
            f"| **Margin** | {margin_sign}{result.margin:.3f} |",
            f"| **Verdict** | **{status}** ({verdict_action} by {margin_pct:.1f}%) |",
            "\n---\n",
        ]
        return "\n".join(lines)

    def _generate_criteria_breakdown(self, breakdown: list[CriteriaBreakdown]) -> str:
        """Generate criteria breakdown table."""
        lines = [
            "## Criteria Breakdown\n",
            "| Question | Weight | Raw Mean | Normalized | Contribution |",
            "|----------|--------|----------|------------|--------------|",
        ]

        for c in breakdown:
            lines.append(
                f"| {c.question_id} | {c.weight*100:.0f}% | {c.raw_mean:.2f} | "
                f"{c.normalized:.3f} | {c.contribution:.3f} |"
            )

        lines.append("\n---\n")
        return "\n".join(lines)

    def _generate_insights(self, metrics: dict[str, QuestionMetrics]) -> str:
        """Generate key insights section with strengths and weaknesses."""
        # Sort metrics by mean score
        sorted_metrics = sorted(
            metrics.items(),
            key=lambda x: x[1].mean,
            reverse=True,
        )

        # Top 3 strengths and bottom 2 weaknesses
        strengths = sorted_metrics[:3]
        weaknesses = sorted_metrics[-2:]

        lines = [
            "## Key Insights\n",
            "### Strengths\n",
        ]

        for i, (qid, m) in enumerate(strengths, 1):
            lines.append(f"{i}. **{qid}** ({m.mean:.2f}) - Top 2 box: {m.top_2_box*100:.0f}%\n")

        lines.append("\n### Weaknesses\n")

        for i, (qid, m) in enumerate(weaknesses, 1):
            lines.append(f"{i}. **{qid}** ({m.mean:.2f}) - Bottom 2 box: {m.bottom_2_box*100:.0f}%\n")

        lines.append("\n---\n")
        return "\n".join(lines)

    def _generate_metrics_table(self, metrics: dict[str, QuestionMetrics]) -> str:
        """Generate detailed metrics table."""
        lines = [
            "## Metrics Summary\n",
            "| Question | Mean | Median | Std Dev | Top 2 Box | Bottom 2 Box |",
            "|----------|------|--------|---------|-----------|--------------|",
        ]

        for qid, m in metrics.items():
            lines.append(
                f"| {qid} | {m.mean:.2f} | {m.median:.2f} | {m.std_dev:.2f} | "
                f"{m.top_2_box*100:.0f}% | {m.bottom_2_box*100:.0f}% |"
            )

        lines.append("\n---\n")
        return "\n".join(lines)

    def _generate_sample_responses(
        self,
        dataset: list[dict[str, Any]],
        num_samples: int = 3,
    ) -> str:
        """Generate sample responses section."""
        lines = ["## Sample Responses\n"]

        # Get first N personas from dataset
        samples = dataset[:num_samples]

        for persona in samples:
            # Build persona header
            persona_id = persona.get("persona_id", "Unknown")
            age = persona.get("age", "?")
            gender = persona.get("gender", "?")
            income = persona.get("income", "?")
            location = persona.get("location", "?")
            interests = persona.get("interests", [])

            lines.append(f"### {persona_id} ({age}y, {gender}, {income} income, {location})")
            if interests:
                lines.append(f"*Interests: {", ".join(interests)}*\n")

            # Find question fields (those ending in _text)
            text_fields = [k for k in persona.keys() if k.endswith("_text")]

            # Show first 2 responses
            for field in text_fields[:2]:
                qid = field.replace("_text", "")
                mean_field = f"{qid}_mean"
                text = persona.get(field, "")
                mean = persona.get(mean_field, 0)

                # Truncate long responses
                if len(text) > 300:
                    text = text[:297] + "..."

                lines.append(f"**{qid}** ({mean:.2f}):")
                lines.append(f'> "{text}"\n')

            lines.append("---\n")

        return "\n".join(lines)

    def _generate_conclusions(
        self,
        result: ResultSummary,
        metrics: dict[str, QuestionMetrics],
    ) -> str:
        """Generate conclusions section."""
        sorted_metrics = sorted(
            metrics.items(),
            key=lambda x: x[1].mean,
            reverse=True,
        )

        strongest = sorted_metrics[0]
        weakest = sorted_metrics[-1]

        status = "passed" if result.passed else "failed"
        margin_pct = abs(result.margin) * 100

        lines = [
            "## Conclusions\n",
            f"1. **Overall Result**: The concept {status} with a composite score of "
            f"{result.composite_score:.3f} against a threshold of {result.threshold:.2f} "
            f"(margin: {margin_pct:.1f}%).\n",
            f"2. **Strongest Metric**: {strongest[0]} scored {strongest[1].mean:.2f} "
            f"with {strongest[1].top_2_box*100:.0f}% top 2 box.\n",
            f"3. **Weakest Metric**: {weakest[0]} scored {weakest[1].mean:.2f} "
            f"with {weakest[1].bottom_2_box*100:.0f}% bottom 2 box.\n",
        ]

        # Add recommendation based on result
        if result.passed:
            lines.append(
                "4. **Recommendation**: The concept meets the threshold criteria. "
                "Consider addressing the weakest metrics to further strengthen the concept.\n"
            )
        else:
            lines.append(
                "4. **Recommendation**: The concept did not meet the threshold. "
                "Focus on improving the weakest metrics and consider concept refinement.\n"
            )

        return "\n".join(lines)
