"""Model Adapter Factory for ADAPT-AI."""

from adapt_ai.config import settings
from adapt_ai.adapters.base import BaseModelAdapter
from adapt_ai.adapters.hosted_adapter import HostedModelAdapter
from adapt_ai.adapters.local_adapter import LocalModelAdapter
from adapt_ai.adapters.mock_eval_adapter import MockEvalAdapter
from adapt_ai.security.phi_sanitizer import logger


def get_model_adapter(override_provider: str = None) -> BaseModelAdapter:
    """Instantiates and returns the configured model adapter.
    
    When 'hosted' is selected, returns HostedModelAdapter. If an API key is not configured,
    the adapter will raise an explicit ProviderError upon inference rather than silently
    falling back to mock responses.
    
    When 'mock_eval' is explicitly requested, returns MockEvalAdapter for testing.
    """
    provider = (override_provider or settings.MODEL_PROVIDER).lower()

    if provider == "hosted":
        if not settings.is_hosted_key_configured:
            logger.warning(
                f"HOSTED_API_KEY is not configured (or contains placeholder). Hosted adapter ({settings.HOSTED_PROVIDER_TYPE}) "
                "will require a valid key in .env to execute live inference."
            )
        return HostedModelAdapter(
            api_key=settings.HOSTED_API_KEY,
            api_base=settings.HOSTED_API_BASE or "https://generativelanguage.googleapis.com/v1beta/openai",
            model_name=settings.HOSTED_MODEL_NAME or "gemini-1.5-flash",
            provider_type=settings.HOSTED_PROVIDER_TYPE or "google",
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
            max_retries=settings.MAX_RETRIES,
        )

    elif provider == "local":
        adapter = LocalModelAdapter(
            endpoint=settings.LOCAL_MODEL_ENDPOINT,
            model_name=settings.LOCAL_MODEL_NAME,
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
            max_retries=settings.MAX_RETRIES,
        )
        if not adapter.is_healthy():
            logger.warning(
                f"Local model endpoint at {settings.LOCAL_MODEL_ENDPOINT} is not reachable. "
                "Falling back to MockEvalAdapter for testing."
            )
            return MockEvalAdapter(model_name="mock-fallback-local-offline")
        return adapter

    elif provider in ("mock_eval", "eval", "mock", "test"):
        return MockEvalAdapter()

    else:
        logger.warning(f"Unrecognized provider '{provider}'. Defaulting to MockEvalAdapter.")
        return MockEvalAdapter()
