"""Local Model Provider Adapter for open-weight models (Ollama, vLLM, LMDeploy)."""

import base64
from typing import List, Dict, Any, Optional
import requests

from adapt_ai.adapters.base import BaseModelAdapter
from adapt_ai.adapters.retry_handler import execute_with_retry
from adapt_ai.models.schemas import ChatMessage
from adapt_ai.models.exceptions import ProviderError
from adapt_ai.security.phi_sanitizer import logger


class LocalModelAdapter(BaseModelAdapter):
    """Adapter for locally hosted open-weight models running on Ollama, vLLM, or LMDeploy."""

    def __init__(
        self,
        endpoint: str = "http://localhost:11434/v1",
        model_name: str = "med-llama3-8b",
        timeout: float = 30.0,
        max_retries: int = 2,
    ):
        super().__init__(model_name=model_name, timeout=timeout)
        self.endpoint = endpoint.rstrip("/")
        self.max_retries = max_retries

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

        def _call():
            url = f"{self.endpoint}/chat/completions"
            resp = requests.post(url, json=payload, timeout=self.timeout)
            if resp.status_code != 200:
                raise ProviderError(
                    f"Local inference server returned status {resp.status_code}: {resp.text}",
                    provider="local-model",
                    status_code=resp.status_code
                )
            return resp.json()["choices"][0]["message"]["content"]

        return execute_with_retry(
            _call,
            max_retries=self.max_retries,
            provider_name="local-open-weight"
        )

    def embed(self, texts: List[str]) -> List[List[float]]:
        payload = {
            "model": self.model_name,
            "input": texts
        }

        def _call():
            url = f"{self.endpoint}/embeddings"
            resp = requests.post(url, json=payload, timeout=self.timeout)
            if resp.status_code != 200:
                raise ProviderError(
                    f"Local embedding server returned {resp.status_code}: {resp.text}",
                    provider="local-model",
                    status_code=resp.status_code
                )
            return [item["embedding"] for item in resp.json()["data"]]

        return execute_with_retry(
            _call,
            max_retries=self.max_retries,
            provider_name="local-embeddings"
        )

    def analyze_vision(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> str:
        b64_img = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64_img}"}}
                    ]
                }
            ],
            "max_tokens": 512,
        }

        def _call():
            url = f"{self.endpoint}/chat/completions"
            resp = requests.post(url, json=payload, timeout=self.timeout)
            if resp.status_code != 200:
                raise ProviderError(
                    f"Local vision model returned {resp.status_code}: {resp.text}",
                    provider="local-model",
                    status_code=resp.status_code
                )
            return resp.json()["choices"][0]["message"]["content"]

        return execute_with_retry(
            _call,
            max_retries=self.max_retries,
            provider_name="local-vision"
        )

    def is_healthy(self) -> bool:
        try:
            url = f"{self.endpoint}/models"
            resp = requests.get(url, timeout=3.0)
            return resp.status_code == 200
        except Exception:
            return False

