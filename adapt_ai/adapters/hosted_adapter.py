"""Hosted Model Provider Adapter (Google Gemini / OpenAI / Generic OpenAI-compatible).

Supports Google's officially supported OpenAI-compatible REST endpoint
(https://generativelanguage.googleapis.com/v1beta/openai/) as well as standard OpenAI endpoints.
"""

import base64
import json
from typing import List, Dict, Any, Optional, Tuple
import requests

from adapt_ai.adapters.base import BaseModelAdapter
from adapt_ai.adapters.retry_handler import execute_with_retry
from adapt_ai.models.schemas import ChatMessage
from adapt_ai.models.exceptions import ProviderError
from adapt_ai.security.phi_sanitizer import logger


class HostedModelAdapter(BaseModelAdapter):
    """Adapter for hosted LLM APIs using standard HTTPS REST calls.
    
    Protects server credentials, validates upstream requests, and returns
    structured errors without falling back silently to mock responses.
    """

    def __init__(
        self,
        api_key: Optional[str],
        api_base: str = "https://generativelanguage.googleapis.com/v1beta/openai",
        model_name: str = "gemini-1.5-flash",
        provider_type: str = "google",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        super().__init__(model_name=model_name, timeout=timeout)
        self.api_key = api_key
        self.api_base = api_base.rstrip("/")
        self.provider_type = provider_type.lower()
        self.max_retries = max_retries

    def is_configured(self) -> bool:
        """Returns True if a non-empty, non-placeholder API key is configured."""
        if not self.api_key or not self.api_key.strip():
            return False
        clean = self.api_key.strip().lower()
        return clean not in ("", "your_gemini_api_key_here", "your_api_key_here", "placeholder", "<api_key>", "none")

    def _headers(self) -> Dict[str, str]:
        """Constructs authentication and content headers for the hosted provider."""
        if not self.is_configured():
            raise ProviderError(
                f"Hosted model adapter ({self.provider_type}) requires a valid API key configured on the server. "
                "HOSTED_API_KEY in your .env file is currently missing or contains a placeholder value. "
                "Please configure a valid API key from Google AI Studio in your server-side .env file.",
                provider=self.provider_type,
                status_code=401
            )
        headers = {
            "Authorization": f"Bearer {self.api_key.strip()}",
            "Content-Type": "application/json"
        }
        # For Google Gemini endpoints, also supply x-goog-api-key header for maximum compatibility
        if self.provider_type in ("google", "gemini"):
            headers["x-goog-api-key"] = self.api_key.strip()
        return headers

    def _parse_error(self, resp: requests.Response) -> Tuple[str, int]:
        """Extracts and sanitizes error message and status code from upstream response.
        
        Guarantees that raw secrets or internal query params are never reflected.
        Categorizes error into clear user-actionable diagnostics.
        """
        raw_msg = ""
        status_code = resp.status_code
        try:
            err_json = resp.json()
            if "error" in err_json:
                err_data = err_json["error"]
                if isinstance(err_data, dict):
                    raw_msg = err_data.get("message", "")
                    details = err_data.get("details", [])
                    # Check for API_KEY_INVALID in Google error details
                    for d in details:
                        if isinstance(d, dict) and d.get("reason") == "API_KEY_INVALID":
                            return (
                                f"Upstream AI provider ({self.provider_type}) authentication failed: The configured API key is invalid or lacks access. Please verify HOSTED_API_KEY in your .env file.",
                                401
                            )
                else:
                    raw_msg = str(err_data)
        except Exception:
            raw_msg = resp.text

        msg_lower = (raw_msg or "").lower()

        # 1. Invalid or missing API key
        if status_code in (400, 401, 403) and any(term in msg_lower for term in ["api key", "api_key", "unauthenticated", "credential", "invalid api"]):
            return (
                f"Upstream AI provider ({self.provider_type}) authentication failed: The configured API key is invalid or lacks necessary permissions. Please verify HOSTED_API_KEY in your .env file.",
                401
            )

        # 2. Rate limit or quota exceeded
        if status_code == 429 or any(term in msg_lower for term in ["quota", "resource_exhausted", "rate limit", "too many requests"]):
            return (
                f"Upstream AI provider ({self.provider_type}) quota or rate limit exceeded. Please wait a moment before sending another request.",
                429
            )

        # 3. Model not found or unsupported
        if status_code == 404 or any(term in msg_lower for term in ["not found", "unsupported model", "is not found"]):
            return (
                f"Configured model '{self.model_name}' was not found on upstream provider ({self.provider_type}). Please verify HOSTED_MODEL_NAME in your configuration.",
                404
            )

        # 4. Upstream server overload or temporary unavailability
        if status_code in (500, 502, 503, 504):
            return (
                f"Upstream AI provider ({self.provider_type}) is temporarily unavailable (HTTP {status_code}). Please retry shortly.",
                503
            )

        # 5. Generic sanitized fallback
        sanitized_summary = (raw_msg[:200] if raw_msg else f"HTTP {status_code}").replace(self.api_key or "", "[REDACTED]")
        return (
            f"Upstream AI provider ({self.provider_type}) error: {sanitized_summary}",
            status_code
        )

    def _parse_error_response(self, resp: requests.Response) -> str:
        """Extracts descriptive error message from upstream JSON error payload if available."""
        msg, _ = self._parse_error(resp)
        return msg

    def generate(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.2,
        max_tokens: int = 1024,
        extra_params: Optional[Dict[str, Any]] = None,
    ) -> str:
        payload = {
            "model": self.model_name,
            "messages": [{"role": m.role.value, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if extra_params:
            payload.update(extra_params)

        def _call_api():
            url = f"{self.api_base}/chat/completions"
            try:
                resp = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            except requests.exceptions.Timeout as e:
                raise ProviderError(
                    f"Upstream AI provider ({self.provider_type}) request timed out after {self.timeout}s.",
                    provider=self.provider_type,
                    status_code=504
                ) from e
            except requests.exceptions.ConnectionError as e:
                raise ProviderError(
                    f"Upstream AI provider ({self.provider_type}) network connection failed. Unable to reach host.",
                    provider=self.provider_type,
                    status_code=503
                ) from e
            except requests.exceptions.RequestException as e:
                raise ProviderError(
                    f"Upstream AI provider ({self.provider_type}) request error: {str(e)}",
                    provider=self.provider_type,
                    status_code=502
                ) from e

            if resp.status_code != 200:
                err_msg, err_code = self._parse_error(resp)
                raise ProviderError(
                    err_msg,
                    provider=self.provider_type,
                    status_code=err_code
                )
            data = resp.json()
            choices = data.get("choices", [])
            if not choices:
                return ""
            msg = choices[0].get("message", {})
            return msg.get("content") or ""

        return execute_with_retry(
            _call_api,
            max_retries=self.max_retries,
            provider_name=f"hosted-{self.provider_type}"
        )

    def embed(self, texts: List[str]) -> List[List[float]]:
        # Configured or default embedding model depending on provider
        from adapt_ai.config import settings
        default_embed_model = (
            getattr(settings, "HOSTED_EMBEDDING_MODEL", None)
            or ("gemini-embedding-001" if self.provider_type in ("google", "gemini") else "text-embedding-3-small")
        )
        payload = {
            "model": default_embed_model,
            "input": texts
        }

        def _call_api():
            url = f"{self.api_base}/embeddings"
            try:
                resp = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            except requests.exceptions.Timeout as e:
                raise ProviderError(
                    f"Upstream AI provider ({self.provider_type}) embeddings timed out after {self.timeout}s.",
                    provider=self.provider_type,
                    status_code=504
                ) from e
            except requests.exceptions.ConnectionError as e:
                raise ProviderError(
                    f"Upstream AI provider ({self.provider_type}) embeddings connection failed.",
                    provider=self.provider_type,
                    status_code=503
                ) from e
            except requests.exceptions.RequestException as e:
                raise ProviderError(
                    f"Upstream AI provider ({self.provider_type}) embeddings error: {str(e)}",
                    provider=self.provider_type,
                    status_code=502
                ) from e

            if resp.status_code != 200:
                err_msg, err_code = self._parse_error(resp)
                raise ProviderError(
                    err_msg,
                    provider=self.provider_type,
                    status_code=err_code
                )
            data = resp.json()
            return [item["embedding"] for item in data["data"]]

        return execute_with_retry(
            _call_api,
            max_retries=self.max_retries,
            provider_name=f"hosted-{self.provider_type}-embeddings"
        )

    def analyze_vision(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> str:
        b64_img = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:{mime_type};base64,{b64_img}"
        
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.1
        }

        def _call_api():
            url = f"{self.api_base}/chat/completions"
            try:
                resp = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            except requests.exceptions.Timeout as e:
                raise ProviderError(
                    f"Upstream Vision API ({self.provider_type}) timed out after {self.timeout}s.",
                    provider=self.provider_type,
                    status_code=504
                ) from e
            except requests.exceptions.ConnectionError as e:
                raise ProviderError(
                    f"Upstream Vision API ({self.provider_type}) network connection failed.",
                    provider=self.provider_type,
                    status_code=503
                ) from e
            except requests.exceptions.RequestException as e:
                raise ProviderError(
                    f"Upstream Vision API ({self.provider_type}) error: {str(e)}",
                    provider=self.provider_type,
                    status_code=502
                ) from e

            if resp.status_code != 200:
                err_msg, err_code = self._parse_error(resp)
                raise ProviderError(
                    err_msg,
                    provider=self.provider_type,
                    status_code=err_code
                )
            data = resp.json()
            return data["choices"][0]["message"]["content"]

        return execute_with_retry(
            _call_api,
            max_retries=self.max_retries,
            provider_name=f"hosted-{self.provider_type}-vision"
        )

    def is_healthy(self) -> bool:
        """Verifies if the remote hosted API responds to a connectivity probe."""
        if not self.is_configured():
            return False
        try:
            url = f"{self.api_base}/models"
            resp = requests.get(url, headers=self._headers(), timeout=min(5.0, self.timeout))
            return resp.status_code == 200
        except Exception as e:
            logger.warning(f"Health check failed for {self.provider_type}: {e}")
            return False
