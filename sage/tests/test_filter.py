"""Tests for the filter engine."""

import pytest

from sage.services.filter_engine import FilterEngine


@pytest.fixture
def filter_engine():
    return FilterEngine()


@pytest.fixture
def sample_personas():
    return [
        {"persona_id": "p1", "age": 25, "gender": "F", "income": "high", "region": "North"},
        {"persona_id": "p2", "age": 35, "gender": "M", "income": "medium", "region": "South"},
        {"persona_id": "p3", "age": 45, "gender": "F", "income": "low", "region": "East"},
        {"persona_id": "p4", "age": 55, "gender": "M", "income": "high", "region": "West"},
        {"persona_id": "p5", "age": 30, "gender": "F", "income": "medium", "region": "North"},
    ]


class TestFilterEngine:
    """Test cases for FilterEngine."""

    def test_no_filters(self, filter_engine, sample_personas):
        """Test that no filters returns all personas."""
        filtered, match_flags = filter_engine.apply_filters(sample_personas, [])

        assert len(filtered) == 5
        assert all(match_flags)

    def test_equality_filter_string(self, filter_engine, sample_personas):
        """Test equality filter with string value."""
        filtered, match_flags = filter_engine.apply_filters(
            sample_personas, ["gender=F"]
        )

        assert len(filtered) == 3
        assert match_flags == [True, False, True, False, True]

    def test_equality_filter_numeric(self, filter_engine, sample_personas):
        """Test equality filter with numeric value."""
        filtered, match_flags = filter_engine.apply_filters(
            sample_personas, ["age=35"]
        )

        assert len(filtered) == 1
        assert filtered[0]["persona_id"] == "p2"

    def test_greater_than_filter(self, filter_engine, sample_personas):
        """Test greater than filter."""
        filtered, match_flags = filter_engine.apply_filters(
            sample_personas, ["age>40"]
        )

        assert len(filtered) == 2
        persona_ids = [p["persona_id"] for p in filtered]
        assert "p3" in persona_ids
        assert "p4" in persona_ids

    def test_greater_than_or_equal_filter(self, filter_engine, sample_personas):
        """Test greater than or equal filter."""
        filtered, match_flags = filter_engine.apply_filters(
            sample_personas, ["age>=45"]
        )

        assert len(filtered) == 2

    def test_less_than_filter(self, filter_engine, sample_personas):
        """Test less than filter."""
        filtered, match_flags = filter_engine.apply_filters(
            sample_personas, ["age<30"]
        )

        assert len(filtered) == 1
        assert filtered[0]["persona_id"] == "p1"

    def test_less_than_or_equal_filter(self, filter_engine, sample_personas):
        """Test less than or equal filter."""
        filtered, match_flags = filter_engine.apply_filters(
            sample_personas, ["age<=30"]
        )

        assert len(filtered) == 2

    def test_not_equal_filter(self, filter_engine, sample_personas):
        """Test not equal filter."""
        filtered, match_flags = filter_engine.apply_filters(
            sample_personas, ["gender!=M"]
        )

        assert len(filtered) == 3

    def test_in_filter(self, filter_engine, sample_personas):
        """Test 'in' membership filter."""
        filtered, match_flags = filter_engine.apply_filters(
            sample_personas, ["region in [North,South]"]
        )

        assert len(filtered) == 3
        regions = [p["region"] for p in filtered]
        assert all(r in ["North", "South"] for r in regions)

    def test_multiple_filters(self, filter_engine, sample_personas):
        """Test multiple filters (AND logic)."""
        filtered, match_flags = filter_engine.apply_filters(
            sample_personas, ["gender=F", "age>=30"]
        )

        assert len(filtered) == 2
        # Should be p3 (age=45, F) and p5 (age=30, F)
        persona_ids = [p["persona_id"] for p in filtered]
        assert "p3" in persona_ids
        assert "p5" in persona_ids

    def test_missing_field_returns_false(self, filter_engine):
        """Test that filtering on missing field returns False."""
        personas = [{"persona_id": "p1", "age": 25}]
        filtered, match_flags = filter_engine.apply_filters(personas, ["income=high"])

        assert len(filtered) == 0
        assert match_flags == [False]

    def test_invalid_filter_expression(self, filter_engine, sample_personas):
        """Test that invalid filter expression raises error."""
        with pytest.raises(ValueError, match="Invalid filter expression"):
            filter_engine.apply_filters(sample_personas, ["invalid"])

    def test_validate_filters_valid(self, filter_engine):
        """Test validation of valid filters."""
        filters = ["age>=30", "gender=F", "region in [North,South]"]
        errors = filter_engine.validate_filters(filters)
        assert len(errors) == 0

    def test_validate_filters_invalid(self, filter_engine):
        """Test validation of invalid filters."""
        filters = ["invalid", "age>=", "=value"]
        errors = filter_engine.validate_filters(filters)
        assert len(errors) == 3
