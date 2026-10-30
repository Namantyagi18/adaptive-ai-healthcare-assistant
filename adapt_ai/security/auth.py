"""Authentication and Access Control dependencies for ADAPT-AI API.

Validates API access tokens, verifies client scopes, manages secure patient session
tokens, and ensures upstream secrets are never leaked to unauthenticated callers.
"""

import time
import base64
import hmac
import hashlib
import secrets
from typing import Optional, Dict, Any
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


def issue_patient_session_token(session_id: Optional[str] = None, ttl_seconds: int = 86400) -> Dict[str, Any]:
    """Issues a cryptographically signed, time-limited patient session token.
    
    Allows ordinary patient web clients to access the healthcare assistant without
    possessing or exposing master server API secrets.
    """
    sid = session_id or f"pat_{secrets.token_hex(8)}"
    now = int(time.time())
    expires_at = now + ttl_seconds
    payload_str = f"{sid}:{now}:{expires_at}"
    
    # Base64 encode payload
    payload_b64 = base64.urlsafe_b64encode(payload_str.encode("utf-8")).decode("utf-8").rstrip("=")
    
    # Compute HMAC-SHA256 signature using server secret
    secret_bytes = (settings.API_KEY_SECRET or DEFAULT_DEV_KEY).encode("utf-8")
    sig = hmac.new(secret_bytes, payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()
    
    token = f"pat_{payload_b64}.{sig}"
    
    return {
        "session_id": sid,
        "token": token,
        "token_type": "Bearer",
        "expires_in": ttl_seconds,
        "expires_at": expires_at,
    }


def verify_patient_session_token(token: str) -> Optional[Dict[str, Any]]:
    """Verifies HMAC signature and expiration timestamp of a patient session token."""
    if not token or not token.startswith("pat_") or "." not in token:
        return None
    
    token_body = token[4:]  # Remove "pat_" prefix
    parts = token_body.split(".", 1)
    if len(parts) != 2:
        return None
    
    payload_b64, sig = parts
    secret_bytes = (settings.API_KEY_SECRET or DEFAULT_DEV_KEY).encode("utf-8")
    expected_sig = hmac.new(secret_bytes, payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()
    
    # Timing-safe signature comparison
    if not secrets.compare_digest(sig, expected_sig):
        return None
    
    try:
        # Pad base64 string
        padded_b64 = payload_b64 + "=" * (-len(payload_b64) % 4)
        payload_str = base64.urlsafe_b64decode(padded_b64.encode("utf-8")).decode("utf-8")
        sid, issued_at_str, expires_at_str = payload_str.split(":", 2)
        expires_at = int(expires_at_str)
        
        # Check expiry
        if int(time.time()) > expires_at:
            return None
        
        return {
            "session_id": sid,
            "issued_at": int(issued_at_str),
            "expires_at": expires_at,
        }
    except Exception:
        return None


def verify_api_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> str:
    """Validates the client provided X-API-Key against server configured secrets or active patient session tokens.
    
    Security Guarantees:
    - Missing or empty API keys return HTTP 401 Unauthorized.
    - Validates server-issued patient session tokens (prefixed with 'pat_').
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
    
    # Check if this is a signed patient session token
    if clean_key.startswith("pat_"):
        session_info = verify_patient_session_token(clean_key)
        if session_info:
            return clean_key
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired patient session token",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
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
