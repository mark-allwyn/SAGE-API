"""Custom exception types for the SAGE API."""


class SageError(Exception):
    """Base exception for all SAGE errors."""


class ProviderError(SageError):
    """Raised when a provider API call fails (maps to HTTP 502)."""

    def __init__(self, provider: str, message: str):
        self.provider = provider
        super().__init__(f"{provider}: {message}")


class ValidationError(SageError):
    """Raised for domain validation errors (maps to HTTP 400)."""


class ConfigurationError(SageError):
    """Raised for misconfiguration errors (maps to HTTP 500)."""
