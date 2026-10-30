"""Embedding generation service for RAG vector search."""

from typing import List, Optional
import numpy as np
from adapt_ai.adapters.base import BaseModelAdapter
from adapt_ai.adapters.mock_eval_adapter import MockEvalAdapter
from adapt_ai.security.phi_sanitizer import logger


class EmbeddingEngine:
    """Computes dense vector representations for medical text passages."""

    def __init__(self, adapter: Optional[BaseModelAdapter] = None, fallback_dim: int = 128):
        self.adapter = adapter or MockEvalAdapter(embedding_dim=fallback_dim)
        self.fallback_dim = fallback_dim

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """Returns normalized 2D numpy array of embeddings (shape: [num_texts, dim])."""
        if not texts:
            return np.empty((0, self.fallback_dim), dtype=np.float32)
        try:
            raw_embeddings = self.adapter.embed(texts)
            arr = np.array(raw_embeddings, dtype=np.float32)
            # Ensure unit normalization for cosine similarity
            norms = np.linalg.norm(arr, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            return arr / norms
        except Exception as e:
            logger.warning(f"Embedding generation via adapter failed ({e}); using deterministic fallback.")
            fallback = MockEvalAdapter(embedding_dim=self.fallback_dim)
            raw_fallback = fallback.embed(texts)
            arr = np.array(raw_fallback, dtype=np.float32)
            norms = np.linalg.norm(arr, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            return arr / norms

    def embed_query(self, query: str) -> np.ndarray:
        """Embeds a single query into a 1D normalized numpy array."""
        embeddings = self.embed_documents([query])
        return embeddings[0]

    def get_embedding_dim(self) -> int:
        """Probes the active adapter to determine its vector dimension."""
        try:
            vec = self.embed_query("probe")
            return int(vec.shape[0])
        except Exception as e:
            logger.warning(f"Unable to probe embedding dimension ({e}); defaulting to {self.fallback_dim}.")
            return self.fallback_dim

