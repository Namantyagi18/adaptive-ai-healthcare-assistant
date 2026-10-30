"""Domain exceptions for ADAPT-AI platform."""

from typing import Optional, Dict, Any


class AdaptAIException(Exception):
    """Base exception for all ADAPT-AI domain errors."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ProviderError(AdaptAIException):
    """Raised when an upstream model inference provider encounters an error or timeout."""
    def __init__(self, message: str, provider: str, status_code: Optional[int] = None):
        super().__init__(message, {"provider": provider, "status_code": status_code})
        self.provider = provider
        self.status_code = status_code


class RateLimitExceededError(AdaptAIException):
    """Raised when client exceeds designated sliding window rate limits."""
    def __init__(self, retry_after: float):
        super().__init__(f"Rate limit exceeded. Please retry after {retry_after} seconds.")
        self.retry_after = retry_after


class SafetyViolationError(AdaptAIException):
    """Raised when an attempt to bypass clinical guardrails is detected."""
    def __init__(self, reason: str, category: str):
        super().__init__(f"Safety guardrail triggered: {reason}", {"category": category})
        self.category = category


class ResourceInsufficientError(AdaptAIException):
    """Raised when available computing hardware is inadequate for the requested training or inference."""
    def __init__(self, required: str, available: str):
        super().__init__(
            f"Insufficient compute resources. Required: {required}, Available: {available}",
            {"required": required, "available": available}
        )


class InvalidDocumentError(AdaptAIException):
    """Raised when a document or image fails format validation or security quarantine."""
    def __init__(self, reason: str):
        super().__init__(f"Invalid document: {reason}")

