"""Report generator for creating markdown reports from test results."""

from typing import Any

from ..models.request import Concept, Question
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
        questions: list[Question] | None = None,
        concept: Concept | None = None,
    ) -> str:
        """Generate a markdown report from test results."""
        sections = [
            self._generate_header(concept_name),
            self._generate_overview(meta, personas_total, personas_matched, filters_applied),
            self._generate_concept_description(concept),
            self._generate_result_summary(result),
            self._generate_criteria_breakdown(criteria_breakdown),
            self._generate_insights(metrics),
            self._generate_metrics_table(metrics),
            self._generate_distribution_analysis(metrics),
        ]

        if dataset:
            sections.append(self._generate_sample_responses(dataset, questions))

        sections.append(self._generate_conclusions(result, metrics))
        sections.append(self._generate_dataset_summary(personas_matched, questions, dataset))

        if questions:
            sections.append(self._generate_appendix(questions))

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
            f"| **Experiment ID** | `{meta.request_id}` |",
            f"| **Concept Name** | {meta.concept_name} |",
            f"| **Personas Tested** | {personas_matched} of {personas_total} |",
            f"| **Processing Time** | {processing_time_sec:.1f}s (~{processing_time_min:.1f} min) |",
        ]

        if meta.providers:
            gen_provider, gen_model = meta.providers.generation.split("/", 1)
            emb_provider, emb_model = meta.providers.embedding.split("/", 1)
            vis_provider, vis_model = meta.providers.vision.split("/", 1)

            lines.append(f"| **Generation Model** | `{gen_model}` ({gen_provider}) |")
            lines.append(f"| **Embedding Model** | `{emb_model}` ({emb_provider}) |")
            lines.append(f"| **Vision Model** | `{vis_model}` ({vis_provider}) |")

        if filters_applied:
            lines.append(f"| **Filters** | {', '.join(filters_applied)} |")

        lines.append("\n---\n")
        return "\n".join(lines)

    def _generate_concept_description(self, concept: Concept | None) -> str:
        """Generate concept description section."""
        if not concept:
            return ""

        content_types = [c.type for c in concept.content]
        has_text = "text" in content_types
        has_image = "image" in content_types

        if has_text and has_image:
            concept_type = "Text + Image"
        elif has_image:
            concept_type = "Image"
        else:
            concept_type = "Text"

        lines = [
            "## Concept Description\n",
            f"**Concept:** {concept.name}",
            f"**Format:** {concept_type} ({len(concept.content)} content items)\n",
        ]

        # Include text content
        text_items = [c.data for c in concept.content if c.type == "text"]
        for text in text_items:
            # Truncate very long concept text
            if len(text) > 500:
                text = text[:497] + "..."
            lines.append(f"> {text}\n")

        if has_image:
            image_count = sum(1 for c in concept.content if c.type == "image")
            lines.append(f"*{image_count} image(s) included in concept stimulus.*\n")

        lines.append("---\n")
        return "\n".join(lines)

    def _generate_result_summary(self, result: ResultSummary) -> str:
        """Generate result summary section."""
        status = "PASSED" if result.passed else "FAILED"
        margin_pct = abs(result.margin) * 100

        if margin_pct < 5:
            strength = "Marginal"
        elif margin_pct < 15:
            strength = "Moderate"
        else:
            strength = "Clear"

        margin_sign = "+" if result.margin >= 0 else ""
        verdict_action = "exceeded" if result.passed else "fell short"

        lines = [
            f"## Overall Result: {status} ({strength})\n",
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
        sorted_metrics = sorted(
            metrics.items(),
            key=lambda x: x[1].mean,
            reverse=True,
        )

        strengths = sorted_metrics[:3]
        weaknesses = sorted_metrics[-2:]

        lines = [
            "## Key Insights\n",
            "### Strengths\n",
        ]

        for i, (qid, m) in enumerate(strengths, 1):
            spread = "tight" if m.std_dev < 0.3 else "moderate" if m.std_dev < 0.6 else "wide"
            lines.append(
                f"{i}. **{qid}** ({m.mean:.2f}) - "
                f"Top 2 box: {m.top_2_box*100:.0f}%, "
                f"median: {m.median:.2f}, "
                f"{spread} spread (std: {m.std_dev:.2f})\n"
            )

        lines.append("\n### Weaknesses\n")

        for i, (qid, m) in enumerate(weaknesses, 1):
            spread = "tight" if m.std_dev < 0.3 else "moderate" if m.std_dev < 0.6 else "wide"
            lines.append(
                f"{i}. **{qid}** ({m.mean:.2f}) - "
                f"Bottom 2 box: {m.bottom_2_box*100:.0f}%, "
                f"median: {m.median:.2f}, "
                f"{spread} spread (std: {m.std_dev:.2f})\n"
            )

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

    def _generate_distribution_analysis(self, metrics: dict[str, QuestionMetrics]) -> str:
        """Generate distribution analysis across all questions."""
        # Aggregate distributions across all questions
        total_dist: dict[str, int] = {}
        for m in metrics.values():
            for rating, count in m.distribution.items():
                total_dist[rating] = total_dist.get(rating, 0) + count

        total_responses = sum(total_dist.values())
        if total_responses == 0:
            return ""

        labels = {
            "1": "Strongly Negative",
            "2": "Negative",
            "3": "Neutral",
            "4": "Positive",
            "5": "Strongly Positive",
        }

        lines = [
            "### Distribution Analysis (All Questions Combined)\n",
            "| Rating | Count | Percentage |",
            "|--------|-------|------------|",
        ]

        for rating in ["1", "2", "3", "4", "5"]:
            count = total_dist.get(rating, 0)
            pct = (count / total_responses * 100) if total_responses > 0 else 0
            label = labels.get(rating, rating)
            lines.append(f"| {rating} ({label}) | {count} | {pct:.1f}% |")

        # Interpret the distribution
        positive = total_dist.get("4", 0) + total_dist.get("5", 0)
        negative = total_dist.get("1", 0) + total_dist.get("2", 0)
        neutral = total_dist.get("3", 0)
        pos_pct = positive / total_responses * 100
        neg_pct = negative / total_responses * 100
        neu_pct = neutral / total_responses * 100

        lines.append("")
        if pos_pct > neg_pct * 2:
            sentiment = "predominantly positive"
        elif neg_pct > pos_pct * 2:
            sentiment = "predominantly negative"
        elif neu_pct > 40:
            sentiment = "largely neutral with limited polarisation"
        else:
            sentiment = "mixed"

        lines.append(
            f"Overall sentiment is {sentiment}, with {pos_pct:.0f}% positive, "
            f"{neu_pct:.0f}% neutral, and {neg_pct:.0f}% negative responses.\n"
        )

        lines.append("---\n")
        return "\n".join(lines)

    def _generate_sample_responses(
        self,
        dataset: list[dict[str, Any]],
        questions: list[Question] | None = None,
        num_samples: int = 5,
    ) -> str:
        """Generate sample responses section with demographic cross-section."""
        lines = ["## Sample Responses\n"]

        # Select a diverse cross-section by spacing evenly through the dataset
        step = max(1, len(dataset) // num_samples)
        samples = [dataset[i * step] for i in range(min(num_samples, len(dataset)))]

        for persona in samples:
            persona_id = persona.get("persona_id", "Unknown")
            age = persona.get("age", "?")
            gender = persona.get("gender", "?")
            country = persona.get("country", "?")
            education = persona.get("education", "?")

            lines.append(f"### {persona_id} ({age}y, {gender}, {country}, {education})\n")

            text_fields = [k for k in persona.keys() if k.endswith("_text")]

            for field in text_fields[:2]:
                qid = field.replace("_text", "")
                mean_field = f"{qid}_mean"
                text = persona.get(field, "")
                mean = persona.get(mean_field, 0)

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
        """Generate conclusions section with 5 findings."""
        sorted_metrics = sorted(
            metrics.items(),
            key=lambda x: x[1].mean,
            reverse=True,
        )

        strongest = sorted_metrics[0]
        weakest = sorted_metrics[-1]

        status = "passed" if result.passed else "failed"
        margin_pct = abs(result.margin) * 100

        # Calculate overall mean
        overall_mean = sum(m.mean for m in metrics.values()) / len(metrics)

        # Find most polarised metric (highest std dev)
        most_polarised = max(metrics.items(), key=lambda x: x[1].std_dev)

        lines = [
            "## Conclusions\n",
            f"1. **Overall Result**: The concept {status} with a composite score of "
            f"{result.composite_score:.3f} against a threshold of {result.threshold:.2f} "
            f"(margin: {margin_pct:.1f}%). The overall mean across all metrics is {overall_mean:.2f}/5.\n",
            f"2. **Strongest Metric**: {strongest[0]} scored {strongest[1].mean:.2f} "
            f"with {strongest[1].top_2_box*100:.0f}% top 2 box and "
            f"median {strongest[1].median:.2f}.\n",
            f"3. **Weakest Metric**: {weakest[0]} scored {weakest[1].mean:.2f} "
            f"with {weakest[1].bottom_2_box*100:.0f}% bottom 2 box and "
            f"median {weakest[1].median:.2f}.\n",
            f"4. **Response Consistency**: {most_polarised[0]} showed the most variation "
            f"(std dev: {most_polarised[1].std_dev:.2f}), suggesting differing reactions "
            f"across personas.\n",
        ]

        if result.passed:
            lines.append(
                "5. **Recommendation**: The concept meets the threshold criteria. "
                "Consider addressing the weakest metrics to further strengthen the concept "
                "before proceeding to market.\n"
            )
        else:
            gap = abs(result.margin)
            if gap < 0.05:
                lines.append(
                    "5. **Recommendation**: The concept narrowly missed the threshold. "
                    "Minor refinements to the weakest metrics could bring it to a passing score. "
                    "Consider targeted iteration rather than a full rework.\n"
                )
            else:
                lines.append(
                    "5. **Recommendation**: The concept did not meet the threshold by a significant margin. "
                    "Focus on improving the weakest metrics and consider concept refinement "
                    "or alternative creative directions.\n"
                )

        return "\n".join(lines)

    def _generate_dataset_summary(
        self,
        personas_matched: int,
        questions: list[Question] | None,
        dataset: list[dict[str, Any]] | None,
    ) -> str:
        """Generate dataset summary section."""
        num_questions = len(questions) if questions else 0

        lines = [
            "---\n",
            "## Dataset Summary\n",
            f"The full dataset contains {personas_matched} persona responses with:",
            f"- Raw text responses for all {num_questions} questions",
            "- 5-point probability distributions (PMF) from SSR scoring",
            "- Mean Likert scores (1-5) for each question",
        ]

        if dataset and len(dataset) > 0:
            demo_keys = [
                k for k in dataset[0].keys()
                if not k.endswith(("_text", "_pmf", "_mean"))
                and k not in ("persona_id", "matched_filter")
            ]
            if demo_keys:
                lines.append(f"- Demographics: {', '.join(demo_keys)}")

        lines.append("")
        return "\n".join(lines)

    def _generate_appendix(self, questions: list[Question]) -> str:
        """Generate appendix with survey questions and response scales."""
        lines = [
            "---\n",
            "## Appendix: Survey Questions and Response Scales\n",
        ]

        for i, q in enumerate(questions, 1):
            lines.append(f"### Q{i}: {q.id}")
            lines.append(f'**"{q.text}"**\n')

            if q.ssr_reference_sets and len(q.ssr_reference_sets) > 0:
                # Use first reference set as the scale labels
                scale = q.ssr_reference_sets[0]
                lines.append("| Score | Response |")
                lines.append("|-------|----------|")
                for score, label in enumerate(scale, 1):
                    lines.append(f"| {score} | {label} |")
                lines.append("")

        return "\n".join(lines)
