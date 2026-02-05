"""Tests for the FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from sage.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestHealthEndpoint:
    """Test the health check endpoint."""

    def test_health_check(self, client):
        """Test that health check returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestInfoEndpoint:
    """Test the info endpoint."""

    def test_api_info(self, client):
        """Test that info endpoint returns API information."""
        response = client.get("/info")

        assert response.status_code == 200
        data = response.json()

        assert "name" in data
        assert "version" in data
        assert "default_settings" in data


class TestModelsEndpoint:
    """Test the models endpoint."""

    def test_list_models(self, client):
        """Test that models endpoint returns supported models."""
        response = client.get("/models")

        assert response.status_code == 200
        data = response.json()

        # Check structure
        assert "openai" in data
        assert "bedrock" in data

        # Check OpenAI models
        assert "generation" in data["openai"]
        assert "embedding" in data["openai"]
        assert "vision" in data["openai"]


class TestRequestValidation:
    """Test request validation for the test-concept endpoint."""

    def test_missing_personas(self, client):
        """Test that empty personas list is rejected."""
        response = client.post(
            "/test-concept",
            json={
                "personas": [],
                "concept": {
                    "name": "Test",
                    "content": [{"type": "text", "data": "Test content"}],
                },
                "survey_config": {
                    "questions": [
                        {
                            "id": "q1",
                            "text": "Test?",
                            "weight": 1.0,
                            "ssr_reference_sets": [["a", "b", "c", "d", "e"]] * 6,
                        }
                    ]
                },
                "threshold": 0.7,
            },
        )

        assert response.status_code == 422

    def test_missing_persona_id(self, client):
        """Test that personas without persona_id are rejected."""
        response = client.post(
            "/test-concept",
            json={
                "personas": [{"age": 30}],  # Missing persona_id
                "concept": {
                    "name": "Test",
                    "content": [{"type": "text", "data": "Test content"}],
                },
                "survey_config": {
                    "questions": [
                        {
                            "id": "q1",
                            "text": "Test?",
                            "weight": 1.0,
                            "ssr_reference_sets": [["a", "b", "c", "d", "e"]] * 6,
                        }
                    ]
                },
                "threshold": 0.7,
            },
        )

        assert response.status_code == 422

    def test_duplicate_persona_ids(self, client):
        """Test that duplicate persona_ids are rejected."""
        response = client.post(
            "/test-concept",
            json={
                "personas": [
                    {"persona_id": "p1", "age": 30},
                    {"persona_id": "p1", "age": 40},  # Duplicate
                ],
                "concept": {
                    "name": "Test",
                    "content": [{"type": "text", "data": "Test content"}],
                },
                "survey_config": {
                    "questions": [
                        {
                            "id": "q1",
                            "text": "Test?",
                            "weight": 1.0,
                            "ssr_reference_sets": [["a", "b", "c", "d", "e"]] * 6,
                        }
                    ]
                },
                "threshold": 0.7,
            },
        )

        assert response.status_code == 422

    def test_weights_not_summing_to_one(self, client):
        """Test that question weights not summing to 1 are rejected."""
        response = client.post(
            "/test-concept",
            json={
                "personas": [{"persona_id": "p1", "age": 30}],
                "concept": {
                    "name": "Test",
                    "content": [{"type": "text", "data": "Test content"}],
                },
                "survey_config": {
                    "questions": [
                        {
                            "id": "q1",
                            "text": "Test?",
                            "weight": 0.5,  # Should be 1.0
                            "ssr_reference_sets": [["a", "b", "c", "d", "e"]] * 6,
                        }
                    ]
                },
                "threshold": 0.7,
            },
        )

        assert response.status_code == 422

    def test_invalid_reference_sets_count(self, client):
        """Test that wrong number of reference sets is rejected."""
        response = client.post(
            "/test-concept",
            json={
                "personas": [{"persona_id": "p1", "age": 30}],
                "concept": {
                    "name": "Test",
                    "content": [{"type": "text", "data": "Test content"}],
                },
                "survey_config": {
                    "questions": [
                        {
                            "id": "q1",
                            "text": "Test?",
                            "weight": 1.0,
                            "ssr_reference_sets": [["a", "b", "c", "d", "e"]] * 5,  # Should be 6
                        }
                    ]
                },
                "threshold": 0.7,
            },
        )

        assert response.status_code == 422

    def test_invalid_anchor_count(self, client):
        """Test that wrong number of anchors per set is rejected."""
        response = client.post(
            "/test-concept",
            json={
                "personas": [{"persona_id": "p1", "age": 30}],
                "concept": {
                    "name": "Test",
                    "content": [{"type": "text", "data": "Test content"}],
                },
                "survey_config": {
                    "questions": [
                        {
                            "id": "q1",
                            "text": "Test?",
                            "weight": 1.0,
                            "ssr_reference_sets": [["a", "b", "c", "d"]] * 6,  # Should be 5 each
                        }
                    ]
                },
                "threshold": 0.7,
            },
        )

        assert response.status_code == 422

    def test_threshold_out_of_range(self, client):
        """Test that threshold outside 0-1 is rejected."""
        response = client.post(
            "/test-concept",
            json={
                "personas": [{"persona_id": "p1", "age": 30}],
                "concept": {
                    "name": "Test",
                    "content": [{"type": "text", "data": "Test content"}],
                },
                "survey_config": {
                    "questions": [
                        {
                            "id": "q1",
                            "text": "Test?",
                            "weight": 1.0,
                            "ssr_reference_sets": [["a", "b", "c", "d", "e"]] * 6,
                        }
                    ]
                },
                "threshold": 1.5,  # Out of range
            },
        )

        assert response.status_code == 422

    def test_invalid_provider(self, client):
        """Test that invalid provider is rejected."""
        response = client.post(
            "/test-concept",
            json={
                "personas": [{"persona_id": "p1", "age": 30}],
                "concept": {
                    "name": "Test",
                    "content": [{"type": "text", "data": "Test content"}],
                },
                "survey_config": {
                    "questions": [
                        {
                            "id": "q1",
                            "text": "Test?",
                            "weight": 1.0,
                            "ssr_reference_sets": [["a", "b", "c", "d", "e"]] * 6,
                        }
                    ]
                },
                "threshold": 0.7,
                "options": {
                    "generation_provider": "invalid_provider",
                },
            },
        )

        assert response.status_code == 422


class TestErrorHandling:
    """Test error handling for invalid model configurations."""

    def test_invalid_model_for_provider(self, client):
        """Test that an invalid model for a valid provider is rejected."""
        response = client.post(
            "/test-concept",
            json={
                "personas": [{"persona_id": "p1", "age": 30}],
                "concept": {
                    "name": "Test",
                    "content": [{"type": "text", "data": "Test content"}],
                },
                "survey_config": {
                    "questions": [
                        {
                            "id": "q1",
                            "text": "Test?",
                            "weight": 1.0,
                            "ssr_reference_sets": [["a", "b", "c", "d", "e"]] * 6,
                        }
                    ]
                },
                "threshold": 0.7,
                "options": {
                    "generation_provider": "openai",
                    "generation_model": "nonexistent-model",
                    "embedding_provider": "openai",
                    "embedding_model": "text-embedding-3-small",
                    "vision_provider": "openai",
                    "vision_model": "gpt-4o",
                },
            },
        )

        assert response.status_code == 422

    def test_embedding_model_used_for_generation(self, client):
        """Test that using an embedding model for generation is rejected."""
        response = client.post(
            "/test-concept",
            json={
                "personas": [{"persona_id": "p1", "age": 30}],
                "concept": {
                    "name": "Test",
                    "content": [{"type": "text", "data": "Test content"}],
                },
                "survey_config": {
                    "questions": [
                        {
                            "id": "q1",
                            "text": "Test?",
                            "weight": 1.0,
                            "ssr_reference_sets": [["a", "b", "c", "d", "e"]] * 6,
                        }
                    ]
                },
                "threshold": 0.7,
                "options": {
                    "generation_provider": "openai",
                    "generation_model": "text-embedding-3-small",
                    "embedding_provider": "openai",
                    "embedding_model": "text-embedding-3-small",
                    "vision_provider": "openai",
                    "vision_model": "gpt-4o",
                },
            },
        )

        assert response.status_code == 422
