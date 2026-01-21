"""Tests for the scoring engine."""

import pytest

from sage.models.request import Question
from sage.services.scoring_engine import ScoringEngine


@pytest.fixture
def scoring_engine():
    return ScoringEngine()


@pytest.fixture
def sample_questions():
    """Create sample questions with weights summing to 1."""
    return [
        Question(
            id="q1",
            text="Question 1",
            weight=0.5,
            ssr_reference_sets=[["a1", "a2", "a3", "a4", "a5"]] * 6,
        ),
        Question(
            id="q2",
            text="Question 2",
            weight=0.3,
            ssr_reference_sets=[["b1", "b2", "b3", "b4", "b5"]] * 6,
        ),
        Question(
            id="q3",
            text="Question 3",
            weight=0.2,
            ssr_reference_sets=[["c1", "c2", "c3", "c4", "c5"]] * 6,
        ),
    ]


@pytest.fixture
def sample_responses():
    """Create sample responses for testing."""
    return [
        {
            "persona_id": "p1",
            "responses": {
                "q1": {"raw_text": "text1", "pmf": [0.1, 0.2, 0.3, 0.3, 0.1], "mean": 4.0},
                "q2": {"raw_text": "text2", "pmf": [0.05, 0.1, 0.2, 0.4, 0.25], "mean": 4.5},
                "q3": {"raw_text": "text3", "pmf": [0.2, 0.3, 0.3, 0.15, 0.05], "mean": 3.0},
            },
        },
        {
            "persona_id": "p2",
            "responses": {
                "q1": {"raw_text": "text4", "pmf": [0.05, 0.1, 0.3, 0.35, 0.2], "mean": 3.5},
                "q2": {"raw_text": "text5", "pmf": [0.1, 0.15, 0.25, 0.3, 0.2], "mean": 3.8},
                "q3": {"raw_text": "text6", "pmf": [0.15, 0.25, 0.35, 0.2, 0.05], "mean": 2.5},
            },
        },
        {
            "persona_id": "p3",
            "responses": {
                "q1": {"raw_text": "text7", "pmf": [0.02, 0.08, 0.2, 0.4, 0.3], "mean": 4.2},
                "q2": {"raw_text": "text8", "pmf": [0.05, 0.1, 0.15, 0.35, 0.35], "mean": 4.3},
                "q3": {"raw_text": "text9", "pmf": [0.1, 0.2, 0.3, 0.25, 0.15], "mean": 3.2},
            },
        },
    ]


class TestScoringEngine:
    """Test cases for ScoringEngine."""

    def test_calculate_metrics_basic(
        self, scoring_engine, sample_responses, sample_questions
    ):
        """Test basic metrics calculation."""
        match_flags = [True, True, True]
        metrics = scoring_engine.calculate_metrics(
            sample_responses, sample_questions, match_flags
        )

        assert "q1" in metrics
        assert "q2" in metrics
        assert "q3" in metrics

        # Check q1 metrics
        q1_metrics = metrics["q1"]
        assert q1_metrics.n == 3
        assert q1_metrics.mean == pytest.approx((4.0 + 3.5 + 4.2) / 3, rel=0.01)

    def test_calculate_metrics_with_filter(
        self, scoring_engine, sample_responses, sample_questions
    ):
        """Test metrics calculation with filtering."""
        # Only include first two personas
        match_flags = [True, True, False]
        metrics = scoring_engine.calculate_metrics(
            sample_responses, sample_questions, match_flags
        )

        # Check that only 2 personas are counted
        assert metrics["q1"].n == 2

    def test_calculate_metrics_no_matches(
        self, scoring_engine, sample_responses, sample_questions
    ):
        """Test that no matches raises error."""
        match_flags = [False, False, False]

        with pytest.raises(ValueError, match="No personas matched"):
            scoring_engine.calculate_metrics(
                sample_responses, sample_questions, match_flags
            )

    def test_calculate_metrics_distribution(
        self, scoring_engine, sample_responses, sample_questions
    ):
        """Test that distribution is calculated correctly."""
        match_flags = [True, True, True]
        metrics = scoring_engine.calculate_metrics(
            sample_responses, sample_questions, match_flags
        )

        # Distribution should have keys 1-5
        for q_id in ["q1", "q2", "q3"]:
            dist = metrics[q_id].distribution
            assert all(str(i) in dist for i in range(1, 6))

    def test_calculate_metrics_top_bottom_box(
        self, scoring_engine, sample_responses, sample_questions
    ):
        """Test top 2 box and bottom 2 box calculations."""
        match_flags = [True, True, True]
        metrics = scoring_engine.calculate_metrics(
            sample_responses, sample_questions, match_flags
        )

        # top_2_box should be between 0 and 1
        # bottom_2_box should be between 0 and 1
        for q_id in ["q1", "q2", "q3"]:
            assert 0 <= metrics[q_id].top_2_box <= 1
            assert 0 <= metrics[q_id].bottom_2_box <= 1

    def test_calculate_composite_score(
        self, scoring_engine, sample_responses, sample_questions
    ):
        """Test composite score calculation."""
        match_flags = [True, True, True]
        metrics = scoring_engine.calculate_metrics(
            sample_responses, sample_questions, match_flags
        )

        composite, breakdown = scoring_engine.calculate_composite_score(
            metrics, sample_questions
        )

        # Composite should be between 0 and 1
        assert 0 <= composite <= 1

        # Breakdown should have entry for each question
        assert len(breakdown) == 3

        # Weights should sum to 1
        total_weight = sum(b.weight for b in breakdown)
        assert total_weight == pytest.approx(1.0, rel=0.01)

        # Contributions should sum to composite
        total_contribution = sum(b.contribution for b in breakdown)
        assert total_contribution == pytest.approx(composite, rel=0.01)

    def test_normalization(self, scoring_engine):
        """Test that normalization maps 1-5 to 0-1."""
        # Mean of 1 should normalize to 0
        # Mean of 5 should normalize to 1
        # Mean of 3 should normalize to 0.5

        assert (1 - 1) / 4 == 0.0
        assert (5 - 1) / 4 == 1.0
        assert (3 - 1) / 4 == 0.5

    def test_evaluate_threshold_pass(self, scoring_engine):
        """Test threshold evaluation for passing score."""
        result = scoring_engine.evaluate_threshold(0.75, 0.70)

        assert result.passed is True
        assert result.composite_score == 0.75
        assert result.threshold == 0.70
        assert result.margin == pytest.approx(0.05, rel=0.01)
        assert "PASS" in result.reason

    def test_evaluate_threshold_fail(self, scoring_engine):
        """Test threshold evaluation for failing score."""
        result = scoring_engine.evaluate_threshold(0.65, 0.70)

        assert result.passed is False
        assert result.composite_score == 0.65
        assert result.threshold == 0.70
        assert result.margin == pytest.approx(-0.05, rel=0.01)
        assert "FAIL" in result.reason

    def test_evaluate_threshold_exact_match(self, scoring_engine):
        """Test threshold evaluation when score exactly matches threshold."""
        result = scoring_engine.evaluate_threshold(0.70, 0.70)

        assert result.passed is True
        assert result.margin == pytest.approx(0.0, abs=0.001)
