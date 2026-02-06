"""Tests for API key authentication."""

import json

import pytest
from fastapi.testclient import TestClient

from sage.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestAuthDisabled:
    """When no keys are configured, all endpoints are accessible."""

    def test_health_no_auth(self, client, monkeypatch):
        """Health endpoint always returns 200."""
        from sage.auth import _clear_keys_cache
        from sage.config import get_settings

        monkeypatch.setattr(get_settings(), "api_keys", "")
        monkeypatch.setattr(get_settings(), "api_keys_file", "")
        _clear_keys_cache()

        response = client.get("/health")
        assert response.status_code == 200

    def test_info_no_auth_disabled(self, client, monkeypatch):
        """Info endpoint returns 200 when auth is disabled."""
        from sage.auth import _clear_keys_cache
        from sage.config import get_settings

        monkeypatch.setattr(get_settings(), "api_keys", "")
        monkeypatch.setattr(get_settings(), "api_keys_file", "")
        _clear_keys_cache()

        response = client.get("/info")
        assert response.status_code == 200

    def test_models_no_auth_disabled(self, client, monkeypatch):
        """Models endpoint returns 200 when auth is disabled."""
        from sage.auth import _clear_keys_cache
        from sage.config import get_settings

        monkeypatch.setattr(get_settings(), "api_keys", "")
        monkeypatch.setattr(get_settings(), "api_keys_file", "")
        _clear_keys_cache()

        response = client.get("/models")
        assert response.status_code == 200


class TestAuthEnabled:
    """When keys are configured, protected endpoints require valid tokens."""

    def test_health_stays_public(self, client, enable_auth):
        """Health endpoint remains public even with auth enabled."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_info_requires_auth(self, client, enable_auth):
        """Info endpoint returns 401 without auth header."""
        response = client.get("/info")
        assert response.status_code == 401

    def test_models_requires_auth(self, client, enable_auth):
        """Models endpoint returns 401 without auth header."""
        response = client.get("/models")
        assert response.status_code == 401

    def test_test_concept_requires_auth(self, client, enable_auth):
        """Test-concept endpoint returns 401 without auth header."""
        response = client.post("/test-concept", json={})
        assert response.status_code == 401

    def test_info_with_valid_key(self, client, enable_auth):
        """Info endpoint returns 200 with valid Bearer token."""
        valid_key = enable_auth
        response = client.get(
            "/info",
            headers={"Authorization": f"Bearer {valid_key}"},
        )
        assert response.status_code == 200

    def test_models_with_valid_key(self, client, enable_auth):
        """Models endpoint returns 200 with valid Bearer token."""
        valid_key = enable_auth
        response = client.get(
            "/models",
            headers={"Authorization": f"Bearer {valid_key}"},
        )
        assert response.status_code == 200

    def test_info_with_invalid_key(self, client, enable_auth):
        """Info endpoint returns 401 with unknown key."""
        response = client.get(
            "/info",
            headers={"Authorization": "Bearer sk-unknown-key"},
        )
        assert response.status_code == 401

    def test_client_name_in_response(self, client, enable_auth):
        """Successful auth does not leak client info in simple endpoints."""
        valid_key = enable_auth
        response = client.get(
            "/info",
            headers={"Authorization": f"Bearer {valid_key}"},
        )
        assert response.status_code == 200
        # Info endpoint returns a dict, not a response with meta
        data = response.json()
        assert "name" in data


class TestEnvVarPriority:
    """Env var keys take priority over file-based keys."""

    def test_env_var_overrides_file(self, client, monkeypatch, api_keys_file):
        """When both env var and file are set, env var keys are used."""
        from sage.auth import _clear_keys_cache
        from sage.config import get_settings

        env_keys = json.dumps({"env-key": "env-client"})
        monkeypatch.setattr(get_settings(), "api_keys", env_keys)
        monkeypatch.setattr(get_settings(), "api_keys_file", api_keys_file)
        _clear_keys_cache()

        # File key should not work
        response = client.get(
            "/info",
            headers={"Authorization": "Bearer test-key-valid"},
        )
        assert response.status_code == 401

        # Env var key should work
        response = client.get(
            "/info",
            headers={"Authorization": "Bearer env-key"},
        )
        assert response.status_code == 200


class TestInvalidConfig:
    """Invalid JSON in keys configuration raises errors."""

    def test_invalid_json_env_var(self, client, monkeypatch):
        """Invalid JSON in SAGE_API_KEYS raises ValueError."""
        from sage.auth import _clear_keys_cache
        from sage.config import get_settings

        monkeypatch.setattr(get_settings(), "api_keys", "not-valid-json")
        monkeypatch.setattr(get_settings(), "api_keys_file", "")
        _clear_keys_cache()

        with pytest.raises(ValueError, match="invalid JSON"):
            client.get("/info")

    def test_invalid_json_file(self, client, monkeypatch, tmp_path):
        """Invalid JSON in keys file raises ValueError."""
        from sage.auth import _clear_keys_cache
        from sage.config import get_settings

        bad_file = tmp_path / "bad_keys.json"
        bad_file.write_text("not-valid-json")

        monkeypatch.setattr(get_settings(), "api_keys", "")
        monkeypatch.setattr(get_settings(), "api_keys_file", str(bad_file))
        _clear_keys_cache()

        with pytest.raises(ValueError, match="invalid JSON"):
            client.get("/info")


class TestHotReload:
    """File-based keys support hot-reload without restart."""

    def test_new_key_works_immediately(self, client, monkeypatch, tmp_path):
        """Adding a key to the file makes it work on the next request."""
        from sage.auth import _clear_keys_cache
        from sage.config import get_settings

        keys_file = tmp_path / "keys.json"
        keys_file.write_text(json.dumps({"key-a": "client-a"}))

        monkeypatch.setattr(get_settings(), "api_keys", "")
        monkeypatch.setattr(get_settings(), "api_keys_file", str(keys_file))
        _clear_keys_cache()

        # key-a works
        response = client.get(
            "/info",
            headers={"Authorization": "Bearer key-a"},
        )
        assert response.status_code == 200

        # key-b doesn't work yet
        response = client.get(
            "/info",
            headers={"Authorization": "Bearer key-b"},
        )
        assert response.status_code == 401

        # Add key-b to the file
        keys_file.write_text(json.dumps({"key-a": "client-a", "key-b": "client-b"}))

        # key-b now works immediately
        response = client.get(
            "/info",
            headers={"Authorization": "Bearer key-b"},
        )
        assert response.status_code == 200
