"""Tests for the SSR engine and embedding utilities."""

import pytest

from sage.utils.embeddings import cosine_similarity, softmax


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
        """Test softmax with uniform input."""
        values = [1.0, 1.0, 1.0, 1.0, 1.0]
        result = softmax(values)

        assert len(result) == 5
        assert sum(result) == pytest.approx(1.0, rel=1e-6)
        # All should be equal for uniform input
        assert all(v == pytest.approx(0.2, rel=1e-6) for v in result)

    def test_softmax_sums_to_one(self):
        """Test that softmax always sums to 1."""
        values = [0.1, 0.5, 0.3, 0.8, 0.2]
        result = softmax(values)

        assert sum(result) == pytest.approx(1.0, rel=1e-6)

    def test_softmax_temperature_effect(self):
        """Test that lower temperature creates sharper distribution."""
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
        """Test that softmax preserves relative ordering."""
        values = [0.1, 0.5, 0.3, 0.9, 0.2]
        result = softmax(values)

        # Index 3 should have highest probability (value 0.9)
        max_idx = result.index(max(result))
        assert max_idx == 3

        # Index 0 should have lowest probability (value 0.1)
        min_idx = result.index(min(result))
        assert min_idx == 0


class TestSSRMapping:
    """Test cases for SSR mapping logic."""

    def test_pmf_sums_to_one(self):
        """Test that PMF from SSR sums to 1."""
        # This would require mocking the LLM service
        # For now, test the mathematical properties
        similarities = [0.7, 0.75, 0.8, 0.85, 0.9]
        min_sim = min(similarities)
        adjusted = [s - min_sim for s in similarities]

        # Add epsilon to minimum
        epsilon = 0.01
        min_idx = similarities.index(min_sim)
        adjusted[min_idx] = epsilon

        pmf = softmax(adjusted, temperature=0.5)

        assert sum(pmf) == pytest.approx(1.0, rel=1e-6)
        assert all(p >= 0 for p in pmf)

    def test_higher_similarity_higher_probability(self):
        """Test that higher similarity leads to higher probability."""
        similarities = [0.6, 0.7, 0.8, 0.9, 0.95]
        min_sim = min(similarities)
        adjusted = [s - min_sim for s in similarities]
        adjusted[0] = 0.01  # epsilon for minimum

        pmf = softmax(adjusted, temperature=0.5)

        # Last element (highest similarity) should have highest probability
        assert pmf[4] == max(pmf)
        # First element (lowest similarity) should have lowest probability
        assert pmf[0] == min(pmf)

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
