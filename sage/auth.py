"""API key authentication for multi-client access."""

import json
import logging
from pathlib import Path

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import get_settings

logger = logging.getLogger(__name__)

_bearer_scheme = HTTPBearer(auto_error=False)

# Cache for env-var-based keys (parsed once, cleared via _clear_keys_cache)
_env_keys_cache: dict[str, str] | None = None
_env_keys_loaded: bool = False


def _load_keys_from_env() -> dict[str, str] | None:
    """Parse API keys from SAGE_API_KEYS env var (JSON string).

    Returns None if the env var is empty.
    Raises ValueError if the JSON is invalid.
    """
    global _env_keys_cache, _env_keys_loaded

    if _env_keys_loaded:
        return _env_keys_cache

    raw = get_settings().api_keys
    if not raw.strip():
        _env_keys_loaded = True
        _env_keys_cache = None
        return None

    try:
        keys = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"SAGE_API_KEYS contains invalid JSON: {e}") from e

    if not isinstance(keys, dict):
        raise ValueError("SAGE_API_KEYS must be a JSON object mapping keys to client names")

    _env_keys_cache = keys
    _env_keys_loaded = True
    return keys


def _load_keys_from_file(path: str) -> dict[str, str] | None:
    """Read and parse API keys from a JSON file.

    Called per-request for hot-reload support. The file is tiny so
    the I/O overhead is negligible.

    Returns None if the file is empty or missing.
    Raises ValueError if the JSON is invalid.
    """
    file_path = Path(path)
    if not file_path.is_file():
        logger.warning("API keys file not found: %s", path)
        return None

    text = file_path.read_text().strip()
    if not text:
        return None

    try:
        keys = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"API keys file contains invalid JSON: {e}") from e

    if not isinstance(keys, dict):
        raise ValueError("API keys file must be a JSON object mapping keys to client names")

    return keys


def get_api_keys() -> dict[str, str] | None:
    """Load API keys, trying env var first, then file.

    Returns None if neither source is configured.
    """
    # Env var takes priority
    env_keys = _load_keys_from_env()
    if env_keys is not None:
        return env_keys

    # Fall back to file (re-read each call for hot-reload)
    file_path = get_settings().api_keys_file
    if file_path.strip():
        return _load_keys_from_file(file_path)

    return None


async def verify_api_key(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> str | None:
    """FastAPI dependency that verifies the Bearer token against loaded API keys.

    Returns the client name if authenticated, or None if auth is disabled.
    Raises 401 if auth is enabled but the token is missing or invalid.
    """
    from fastapi import HTTPException

    keys = get_api_keys()

    # Auth disabled - no keys configured
    if keys is None:
        return None

    # Auth enabled but no token provided
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Provide a Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    client_name = keys.get(token)

    if client_name is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return client_name


def _clear_keys_cache() -> None:
    """Clear the cached env-var keys. Used by tests."""
    global _env_keys_cache, _env_keys_loaded
    _env_keys_cache = None
    _env_keys_loaded = False
