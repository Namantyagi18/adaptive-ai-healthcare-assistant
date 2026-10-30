"""Resilience and retry handler for LLM network communications.

Implements exponential backoff, jitter, and standardized exception mapping.
"""

import time
import random
from typing import Callable, Any
from adapt_ai.models.exceptions import ProviderError
from adapt_ai.security.phi_sanitizer import logger


def execute_with_retry(
    func: Callable[..., Any],
    max_retries: int = 3,
    backoff_factor: float = 1.5,
    provider_name: str = "upstream_llm",
    *args,
    **kwargs
) -> Any:
    """Executes a callable with exponential backoff on transient errors."""
    attempt = 0
    last_exception = None

    while attempt < max_retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            attempt += 1
            last_exception = e
            
            # Extract HTTP status code if present on the exception
            status_code = getattr(e, "status_code", None) or (
                getattr(e, "response", None) and getattr(e.response, "status_code", None)
            )

            # Fatal client/auth/config errors (400, 401, 403, 404) must NOT be retried
            if status_code in (400, 401, 403, 404):
                logger.error(f"Provider {provider_name} request failed with non-retryable status {status_code}: {e}")
                if isinstance(e, ProviderError):
                    raise e
                raise ProviderError(
                    f"Configuration/Authentication error with {provider_name}: {str(e)}",
                    provider=provider_name,
                    status_code=status_code
                ) from e
            
            if attempt >= max_retries:
                logger.error(f"Provider {provider_name} failed after {max_retries} attempts: {str(e)}")
                break
            
            sleep_duration = (backoff_factor ** attempt) + random.uniform(0.1, 0.4)
            logger.warning(
                f"Attempt {attempt}/{max_retries} failed for {provider_name}: {str(e)}. "
                f"Retrying in {sleep_duration:.2f}s..."
            )
            time.sleep(sleep_duration)

    status_code = getattr(last_exception, "status_code", None)
    if isinstance(last_exception, ProviderError):
        raise last_exception

    raise ProviderError(
        f"Failed to communicate with {provider_name} after {max_retries} retries: {str(last_exception)}",
        provider=provider_name,
        status_code=status_code
    ) from last_exception
