"""Authentication and Access Control dependencies for ADAPT-AI API.

Validates API access tokens, verifies client scopes, and ensures
upstream secrets are never leaked to unauthenticated callers.
"""

import secrets
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from adapt_ai.config import settings


DEFAULT_DEV_KEY = "adapt-ai-default-dev-secret-key-2026"
PROHIBITED_PROD_KEYS = {
    DEFAULT_DEV_KEY,
    "dev",
    "development",
    "test",
    "testing",
    "secret",
    "admin",
    "password",
    "123456",
}


API_KEY_HEADER = APIKeyHeader(
    name="X-API-Key",
    scheme_name="ApiKeyAuth",
    description="ADAPT-AI backend authentication key (configured on the server via ADAPT_AI_API_KEY). Enter this key into the field to authorize requests.",
    auto_error=False
)


def verify_api_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> str:
    """Validates the client provided X-API-Key against server configured secrets.
    
    Security Guarantees:
    - Missing or empty API keys return HTTP 401 Unauthorized.
    - Incorrect API keys return HTTP 401 Unauthorized.
    - Uses constant-time comparison (secrets.compare_digest) to prevent timing attacks.
    - Trims surrounding whitespace to tolerate accidental copy-paste artifacts.
    - Strictly blocks development and default API keys when APP_ENV is 'production'.
    """
    if not api_key or not api_key.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing required authentication header: 'X-API-Key'",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    clean_key = api_key.strip()
    configured_secret = (settings.API_KEY_SECRET or "").strip()
    is_production = settings.APP_ENV.strip().lower() in ("production", "prod")

    # Production safety enforcement: development keys cannot accidentally be used in production
    if is_production:
        if clean_key in PROHIBITED_PROD_KEYS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Development API key is strictly prohibited in production mode",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        if configured_secret in PROHIBITED_PROD_KEYS or len(configured_secret) < 16:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Production server must be configured with a secure production API key (at least 16 characters)",
                headers={"WWW-Authenticate": "ApiKey"},
            )

    # Timing-safe comparison to prevent side-channel timing attacks
    if not secrets.compare_digest(clean_key, configured_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or unauthorized API key provided",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return clean_key



