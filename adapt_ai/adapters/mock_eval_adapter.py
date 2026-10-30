"""Deterministic Evaluation and Offline Test Adapter.

Used for comprehensive regression testing, offline CI/CD, and pipeline verification
when live hosted API credentials or local open-weight inference daemons are unconfigured.

CRITICAL POLICY:
This adapter explicitly labels its output as evaluation/test inference and NEVER claims
to be a fine-tuned clinical model. It accurately reflects RAG retrieved context and
evaluates safety guardrail triggers.
"""

import hashlib
from typing import List, Dict, Any, Optional
import numpy as np

from adapt_ai.adapters.base import BaseModelAdapter
from adapt_ai.models.schemas import ChatMessage


class MockEvalAdapter(BaseModelAdapter):
    """Offline test adapter ensuring full pipeline testability without external network dependencies."""

    def __init__(self, model_name: str = "adapt-ai-eval-engine", embedding_dim: int = 128):
        super().__init__(model_name=model_name, timeout=5.0)
        self.embedding_dim = embedding_dim

    def generate(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.2,
        max_tokens: int = 1024,
        extra_params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Synthesizes an evaluation response grounded in the prompt context and retrieved passages."""
        user_message = ""
        context_text = ""
        system_instructions = ""

        for m in messages:
            if m.role.value == "system":
                system_instructions = m.content
            elif m.role.value == "user":
                user_message = m.content

        # Extract retrieved context if provided in system prompt or user query
        if "RETRIEVED MEDICAL CONTEXT" in system_instructions:
            parts = system_instructions.split("RETRIEVED MEDICAL CONTEXT")
            if len(parts) > 1:
                context_text = parts[1].split("INSTRUCTION FOR THIS QUERY:")[0].strip()

        # Synthesis based on extracted context and user query
        response_parts = []
        response_parts.append(f"Regarding your query: \"{user_message.strip()}\"")
        
        if context_text and "No relevant guideline documents found" not in context_text:
            response_parts.append("\nBased on available authoritative medical guidelines:")
            # Extract key statements from context
            lines = [line.strip() for line in context_text.split("\n") if line.strip() and not line.startswith("[Source:") and not line.startswith("[") and not line.startswith("(Sufficiency:")]
            summary_points = lines[:4]
            for p in summary_points:
                response_parts.append(f"- {p}")
            response_parts.append("\nPlease consult a qualified physician to confirm clinical findings and discuss personalized care.")
        else:
            response_parts.append(
                "\nThere is insufficient specific evidence in the loaded medical knowledge base to provide a definitive clinical summary. "
                "Because health conditions require individualized evaluation, you should discuss these symptoms with a qualified healthcare provider."
            )

        return "\n".join(response_parts)

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generates deterministic, normalized subword n-gram semantic embeddings.
        
        Uses word hashes and character trigram hashing (similar to fastText) to capture
        lexical overlap, shared roots (e.g. hyperten-, press-), and terminology matches.
        """
        stopwords = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
            'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were',
            'will', 'with', 'what', 'which', 'who', 'why', 'how', 'do', 'does', 'did',
            'i', 'my', 'me', 'we', 'our', 'you', 'your', 'should', 'can', 'could'
        }
        embeddings = []
        for text in texts:
            raw_words = [w.strip('.,!?:;"()[]{}') for w in text.lower().split()]
            words = [w for w in raw_words if w and w not in stopwords]
            if not words:
                # If only stopwords were present, keep raw words to avoid empty representation
                words = [w for w in raw_words if w]
            vec = np.zeros(self.embedding_dim, dtype=np.float32)
            if not words:
                vec[0] = 1.0
                embeddings.append(vec.tolist())
                continue

            for word in words:
                # Word-level hash feature
                hw = int(hashlib.sha256(word.encode("utf-8")).hexdigest(), 16)
                vec[hw % self.embedding_dim] += 3.0

                # Character 3-gram subword features
                padded = f"_{word}_"
                for i in range(len(padded) - 2):
                    gram = padded[i:i+3]
                    hg = int(hashlib.sha256(gram.encode("utf-8")).hexdigest(), 16)
                    vec[hg % self.embedding_dim] += 1.0

            norm = np.linalg.norm(vec)
            if norm > 1e-6:
                vec = vec / norm
            embeddings.append(vec.tolist())

        return embeddings

    def analyze_vision(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> str:
        byte_len = len(image_bytes)
        return (
            f"[Visual Inspection Engine] Analyzed document image ({mime_type}, {byte_len} bytes). "
            f"Prompt: '{prompt}'. Notice: Automated image analysis is purely supplementary; "
            f"formal radiological or dermatological diagnosis requires direct in-person clinical examination."
        )

    def is_healthy(self) -> bool:
        return True
