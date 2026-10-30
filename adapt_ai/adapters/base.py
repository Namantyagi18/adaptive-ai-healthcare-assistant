"""Abstract base interface for model adapters in ADAPT-AI."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from adapt_ai.models.schemas import ChatMessage


class BaseModelAdapter(ABC):
    """Provider-independent interface for language and vision models.
    
    Guarantees that downstream clinical services can interact with hosted APIs
    or local open-weight models interchangeably.
    """

    def __init__(self, model_name: str, timeout: float = 30.0):
        self.model_name = model_name
        self.timeout = timeout

    @abstractmethod
    def generate(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.2,
        max_tokens: int = 1024,
        extra_params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Generates a text completion given a conversation history."""
        pass

    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generates normalized vector embeddings for a list of text passages."""
        pass

    @abstractmethod
    def analyze_vision(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> str:
        """Performs visual inspection or multimodal document understanding."""
        pass

    @abstractmethod
    def is_healthy(self) -> bool:
        """Verifies operational connectivity and availability of the model provider."""
        pass

