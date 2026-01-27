"""Tests for the SSR engine and embedding utilities."""

import pytest

from sage.utils.embeddings import cosine_similarity, softmax


def normalize_pmf(values: list[float], temperature: float = 1.0) -> list[float]:
    """
    Normalize values to PMF using the paper's methodology (equation 8).

    This is the correct approach: direct normalization, NOT softmax.
    p(r) ∝ adjusted_similarity, with optional temperature: p(r,T) ∝ p(r)^(1/T)
    """
    epsilon = 1e-10
    adjusted = [v + epsilon for v in values]

    if temperature != 1.0:
        adjusted = [a ** (1.0 / temperature) for a in adjusted]

    total = sum(adjusted)
    return [a / total for a in adjusted]


class TestEmbeddingUtilities:
    """Test cases for embedding utility functions."""

    def test_cosine_similarity_identical(self):
        """Test cosine similarity of identical vectors."""
        vec = [1.0, 2.0, 3.0]
        sim = cosine_similarity(vec, vec)
        assert sim == pytest.approx(1.0, rel=1e-6)

    def test_cosine_similarity_orthogonal(self):
        """Test cosine similarity of orthogonal vectors."""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [0.0, 1.0, 0.0]
        sim = cosine_similarity(vec1, vec2)
        assert sim == pytest.approx(0.0, abs=1e-6)

    def test_cosine_similarity_opposite(self):
        """Test cosine similarity of opposite vectors."""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [-1.0, -2.0, -3.0]
        sim = cosine_similarity(vec1, vec2)
        assert sim == pytest.approx(-1.0, rel=1e-6)

    def test_cosine_similarity_zero_vector(self):
        """Test cosine similarity with zero vector."""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [0.0, 0.0, 0.0]
        sim = cosine_similarity(vec1, vec2)
        assert sim == 0.0

    def test_softmax_uniform_input(self):
        """Test softmax with uniform input (legacy function)."""
        values = [1.0, 1.0, 1.0, 1.0, 1.0]
        result = softmax(values)

        assert len(result) == 5
        assert sum(result) == pytest.approx(1.0, rel=1e-6)
        # All should be equal for uniform input
        assert all(v == pytest.approx(0.2, rel=1e-6) for v in result)

    def test_softmax_sums_to_one(self):
        """Test that softmax always sums to 1 (legacy function)."""
        values = [0.1, 0.5, 0.3, 0.8, 0.2]
        result = softmax(values)

        assert sum(result) == pytest.approx(1.0, rel=1e-6)

    def test_softmax_temperature_effect(self):
        """Test that lower temperature creates sharper distribution (legacy function)."""
        values = [0.1, 0.3, 0.5, 0.7, 0.9]

        # Low temperature - sharper
        sharp = softmax(values, temperature=0.1)
        # High temperature - smoother
        smooth = softmax(values, temperature=2.0)

        # The max value should be higher with low temperature
        assert max(sharp) > max(smooth)
        # The variance should be higher with low temperature
        import numpy as np
        assert np.var(sharp) > np.var(smooth)

    def test_softmax_preserves_order(self):
        """Test that softmax preserves relative ordering (legacy function)."""
        values = [0.1, 0.5, 0.3, 0.9, 0.2]
        result = softmax(values)

        # Index 3 should have highest probability (value 0.9)
        max_idx = result.index(max(result))
        assert max_idx == 3

        # Index 0 should have lowest probability (value 0.1)
        min_idx = result.index(min(result))
        assert min_idx == 0


class TestSSRMapping:
    """Test cases for SSR mapping logic using paper's methodology."""

    def test_pmf_sums_to_one(self):
        """Test that PMF from SSR sums to 1."""
        # Following paper equation (8): p(r) ∝ γ(σ_r, t) - γ(σ_ℓ, t)
        similarities = [0.7, 0.75, 0.8, 0.85, 0.9]
        min_sim = min(similarities)
        adjusted = [s - min_sim for s in similarities]

        # Use direct normalization (paper methodology), not softmax
        pmf = normalize_pmf(adjusted)

        assert sum(pmf) == pytest.approx(1.0, rel=1e-6)
        assert all(p >= 0 for p in pmf)

    def test_higher_similarity_higher_probability(self):
        """Test that higher similarity leads to higher probability."""
        similarities = [0.6, 0.7, 0.8, 0.9, 0.95]
        min_sim = min(similarities)
        adjusted = [s - min_sim for s in similarities]

        # Use direct normalization (paper methodology)
        pmf = normalize_pmf(adjusted)

        # Last element (highest similarity) should have highest probability
        assert pmf[4] == max(pmf)
        # First element (lowest similarity) should have lowest probability
        assert pmf[0] == min(pmf)

    def test_paper_methodology_direct_proportionality(self):
        """Test that PMF is directly proportional to adjusted similarity (not exp).

        This is the key difference from softmax - with direct normalization,
        doubling the adjusted similarity doubles the probability.
        """
        # Simple case: adjusted similarities are 1, 2, 3, 4, 5
        adjusted = [1.0, 2.0, 3.0, 4.0, 5.0]
        pmf = normalize_pmf(adjusted)

        # Total is 15, so probabilities should be 1/15, 2/15, 3/15, 4/15, 5/15
        expected = [1/15, 2/15, 3/15, 4/15, 5/15]
        for actual, exp in zip(pmf, expected):
            assert actual == pytest.approx(exp, rel=1e-6)

    def test_temperature_sharpens_distribution(self):
        """Test that lower temperature creates sharper distribution."""
        adjusted = [0.1, 0.2, 0.3, 0.4, 0.5]

        # T=1 (paper default) - no sharpening
        pmf_t1 = normalize_pmf(adjusted, temperature=1.0)

        # T=0.5 - sharper (raises to power of 2)
        pmf_sharp = normalize_pmf(adjusted, temperature=0.5)

        # The max value should be higher with low temperature
        assert max(pmf_sharp) > max(pmf_t1)

        # The variance should be higher with low temperature
        import numpy as np
        assert np.var(pmf_sharp) > np.var(pmf_t1)

    def test_expected_value_calculation(self):
        """Test expected value (mean) calculation from PMF."""
        # Uniform distribution should give mean of 3
        pmf = [0.2, 0.2, 0.2, 0.2, 0.2]
        mean = sum((i + 1) * p for i, p in enumerate(pmf))
        assert mean == pytest.approx(3.0, rel=1e-6)

        # All probability on 5 should give mean of 5
        pmf = [0.0, 0.0, 0.0, 0.0, 1.0]
        mean = sum((i + 1) * p for i, p in enumerate(pmf))
        assert mean == pytest.approx(5.0, rel=1e-6)

        # All probability on 1 should give mean of 1
        pmf = [1.0, 0.0, 0.0, 0.0, 0.0]
        mean = sum((i + 1) * p for i, p in enumerate(pmf))
        assert mean == pytest.approx(1.0, rel=1e-6)

    def test_distinctive_vs_clustered_similarities(self):
        """Test that distinctive similarities produce spread PMF, not clustered at 3.0.

        This is the key test - before the fix, high similarities that are close
        together (e.g., 0.85-0.90) would produce PMF clustered around uniform.
        With the fix, even small differences should produce meaningful variation.
        """
        # Case 1: Similarities that clearly favor rating 5
        similarities_favor_5 = [0.70, 0.75, 0.80, 0.85, 0.95]
        min_sim = min(similarities_favor_5)
        adjusted = [s - min_sim for s in similarities_favor_5]
        pmf = normalize_pmf(adjusted)
        mean = sum((i + 1) * p for i, p in enumerate(pmf))

        # Should be closer to 5 than to 3
        assert mean > 3.5, f"Mean {mean} should be > 3.5 when similarities favor 5"

        # Case 2: Similarities that favor rating 1
        similarities_favor_1 = [0.95, 0.85, 0.80, 0.75, 0.70]
        min_sim = min(similarities_favor_1)
        adjusted = [s - min_sim for s in similarities_favor_1]
        pmf = normalize_pmf(adjusted)
        mean = sum((i + 1) * p for i, p in enumerate(pmf))

        # Should be closer to 1 than to 3
        assert mean < 2.5, f"Mean {mean} should be < 2.5 when similarities favor 1"
