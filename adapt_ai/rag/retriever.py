"""Medical Evidence Retriever and Contradiction Detection Engine.

Analyzes retrieved medical passages to evaluate sufficiency, detect conflicting
guidelines, and format verified source citations.
"""

from typing import List, Tuple, Dict, Any
from adapt_ai.config import settings
from adapt_ai.models.schemas import EvidenceReference, EvidenceSufficiency
from adapt_ai.rag.embeddings import EmbeddingEngine
from adapt_ai.rag.vector_store import VectorStore
from adapt_ai.security.phi_sanitizer import logger


class MedicalRetriever:
    """Orchestrates embedding lookup, similarity ranking, and evidence verification."""

    def __init__(self, vector_store: VectorStore, embedding_engine: EmbeddingEngine):
        self.vector_store = vector_store
        self.embedding_engine = embedding_engine

    def retrieve(
        self,
        query: str,
        top_k: int = None,
        threshold: float = None
    ) -> Tuple[List[EvidenceReference], EvidenceSufficiency, str]:
        """Retrieves passages and classifies evidence sufficiency and contradiction.
        
        Returns:
            Tuple[List[EvidenceReference], EvidenceSufficiency, str]:
                - citations: List of formatted evidence objects
                - sufficiency: SUFFICIENT, INSUFFICIENT, or CONTRADICTORY
                - diagnostic_note: Explanation of retrieval confidence
        """
        k = top_k or settings.RAG_TOP_K
        dim = self.vector_store.get_embedding_dimension()

        # Determine calibrated threshold based on vector space dimension
        if threshold is not None:
            thresh = threshold
        elif dim >= 1024:
            # Dense neural embeddings (e.g. Gemini 3,072-dim) have baseline cosine ~0.50-0.60
            thresh = max(settings.RAG_SIMILARITY_THRESHOLD, 0.65)
        else:
            # Low-dimensional hash/mock evaluation embeddings (dim < 1024)
            thresh = min(settings.RAG_SIMILARITY_THRESHOLD, 0.20)

        query_vec = self.embedding_engine.embed_query(query)
        try:
            raw_results = self.vector_store.similarity_search(query_vec, top_k=k, threshold=thresh)
        except ValueError as e:
            logger.error(f"Semantic search failed due to dimension mismatch: {e}")
            return (
                [],
                EvidenceSufficiency.INSUFFICIENT,
                f"Knowledge base vector mismatch: {str(e)}"
            )

        if not raw_results:
            return (
                [],
                EvidenceSufficiency.INSUFFICIENT,
                f"No authoritative guideline passages met the required similarity threshold ({thresh:.2f}) for this query."
            )

        top_score = raw_results[0][1]
        sufficiency_threshold = 0.68 if dim >= 1024 else 0.25
        if top_score < sufficiency_threshold:
            return (
                [],
                EvidenceSufficiency.INSUFFICIENT,
                f"Weak semantic match (top score: {top_score:.2f}); evidence does not directly answer the specific clinical question."
            )

        citations: List[EvidenceReference] = []
        for chunk_meta, score in raw_results:
            text = chunk_meta["text"]
            # Preserve full clinically relevant passage text (up to 1200 chars)
            excerpt = text[:1200] + "..." if len(text) > 1200 else text
            citations.append(
                EvidenceReference(
                    doc_id=chunk_meta["doc_id"],
                    title=chunk_meta["title"],
                    source=chunk_meta["source"],
                    chunk_id=chunk_meta["chunk_id"],
                    relevance_score=score,
                    excerpt=excerpt
                )
            )

        # Check for contradictory or diverging guidance
        sufficiency, note = self._detect_contradictions(raw_results, query)
        if sufficiency == EvidenceSufficiency.INSUFFICIENT:
            return [], sufficiency, note

        return citations, sufficiency, note

    def _detect_contradictions(
        self,
        results: List[Tuple[Dict[str, Any], float]],
        query: str
    ) -> Tuple[EvidenceSufficiency, str]:
        """Heuristic check for clinical divergence or contrasting indications."""
        if not results:
            return EvidenceSufficiency.INSUFFICIENT, "No evidence retrieved."

        # Check if any retrieved document is in the evolving/contradictory evidence category
        has_evolving_doc = any(
            "contradictory" in r[0].get("category", "").lower() or "evolving" in r[0].get("category", "").lower()
            for r in results
        )

        if len(results) < 2:
            if has_evolving_doc:
                text = results[0][0]["text"].lower()
                if ("recommends against" in text or "not recommended" in text) and "recommended" in text:
                    return (
                        EvidenceSufficiency.CONTRADICTORY,
                        "Guideline evidence displays divergent recommendations or conditional indications across retrieved sources."
                    )
            return EvidenceSufficiency.SUFFICIENT, "Authoritative guideline evidence is sufficient."

        # Verify whether results share clinical domains before asserting contradiction
        categories = [r[0].get("category", "") for r in results]
        unique_categories = set(categories)

        # If retrieved passages are from disparate specialties and none are evolving evidence,
        # they are distinct clinical conditions rather than contradictory guidance
        if not has_evolving_doc and len(unique_categories) == len(results):
            return EvidenceSufficiency.SUFFICIENT, "Authoritative guideline evidence is sufficient."

        texts = [r[0]["text"].lower() for r in results]
        has_recommended = any("recommend" in t or "indicated" in t or "first-line" in t for t in texts)
        has_not_recommended = any(
            "not recommended" in t or "contraindicated" in t or "insufficient benefit" in t or "recommends against" in t
            for t in texts
        )

        if (has_evolving_doc or len(unique_categories) < len(results)) and has_recommended and has_not_recommended:
            return (
                EvidenceSufficiency.CONTRADICTORY,
                "Guideline evidence displays divergent recommendations or conditional indications across retrieved sources."
            )

        return EvidenceSufficiency.SUFFICIENT, "Authoritative guideline evidence is sufficient."

