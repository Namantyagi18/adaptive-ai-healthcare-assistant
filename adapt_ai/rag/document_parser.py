"""Document ingestion and metadata extraction pipeline for medical reference materials.

Preserves document provenance, prevents duplicate ingestions via cryptographic hashing,
and normalizes medical guidelines.
"""

import hashlib
import time
from typing import Dict, Any, Optional
from adapt_ai.models.schemas import IngestionItem
from adapt_ai.security.phi_sanitizer import logger


class DocumentParser:
    """Parses and sanitizes medical guidelines and reference materials."""

    @staticmethod
    def compute_content_hash(text: str) -> str:
        """Computes SHA-256 hash of normalized text to prevent duplicate indexing."""
        normalized = " ".join(text.lower().split())
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    @staticmethod
    def parse(item: IngestionItem) -> Dict[str, Any]:
        """Validates and creates an ingestion record with full provenance tracking."""
        cleaned_text = item.content.strip()
        if not cleaned_text:
            raise ValueError("Document content cannot be empty.")

        content_hash = DocumentParser.compute_content_hash(cleaned_text)
        doc_id = f"doc_{content_hash[:16]}"

        return {
            "doc_id": doc_id,
            "title": item.title.strip(),
            "source": item.source.strip(),
            "category": item.category.strip(),
            "content": cleaned_text,
            "content_hash": content_hash,
            "version": item.version or "1.0",
            "url": item.url,
            "ingested_at": time.time(),
        }

