"""Shared pytest fixtures for the test suite."""

import json

import pytest
from fastapi.testclient import TestClient

from sage.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def valid_test_request():
    """Create a valid test-concept request payload."""
    return {
        "personas": [
            {"persona_id": "p1", "age": 30, "gender": "F", "income": "high"},
            {"persona_id": "p2", "age": 45, "gender": "M", "income": "medium"},
        ],
        "concept": {
            "name": "Test Product",
            "content": [{"type": "text", "data": "A revolutionary new product."}],
        },
        "survey_config": {
            "questions": [
                {
                    "id": "q1",
                    "text": "How likely are you to purchase this product?",
                    "weight": 1.0,
                    "ssr_reference_sets": [
                        [
                            "Definitely would not buy",
                            "Probably would not buy",
                            "Might or might not buy",
                            "Probably would buy",
                            "Definitely would buy",
                        ]
                    ]
                    * 6,
                }
            ]
        },
        "threshold": 0.7,
        "options": {
            "generation_provider": "openai",
            "generation_model": "gpt-4o",
            "embedding_provider": "openai",
            "embedding_model": "text-embedding-3-small",
            "vision_provider": "openai",
            "vision_model": "gpt-4o",
        },
    }


@pytest.fixture
def api_keys_file(tmp_path):
    """Create a temporary API keys file for testing."""
    keys = {"test-key-valid": "test-client", "test-key-admin": "admin-client"}
    keys_path = tmp_path / "test_keys.json"
    keys_path.write_text(json.dumps(keys))
    return str(keys_path)


@pytest.fixture
def enable_auth(monkeypatch, api_keys_file):
    """Enable auth via file-based keys and return a valid key."""
    from sage.auth import _clear_keys_cache
    from sage.config import get_settings

    monkeypatch.setattr(get_settings(), "api_keys_file", api_keys_file)
    monkeypatch.setattr(get_settings(), "api_keys", "")
    _clear_keys_cache()
    return "test-key-valid"


@pytest.fixture
def sample_personas():
    """Create sample personas for testing."""
    return [
        {"persona_id": "p1", "age": 25, "gender": "F", "income": "high", "region": "North"},
        {"persona_id": "p2", "age": 35, "gender": "M", "income": "medium", "region": "South"},
        {"persona_id": "p3", "age": 45, "gender": "F", "income": "low", "region": "East"},
        {"persona_id": "p4", "age": 55, "gender": "M", "income": "high", "region": "West"},
        {"persona_id": "p5", "age": 30, "gender": "F", "income": "medium", "region": "North"},
    ]
