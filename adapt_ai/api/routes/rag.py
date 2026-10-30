"""RAG Engine and Knowledge Base Management Endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Security, Query
from adapt_ai.models.schemas import IngestionRequest, IngestionResponse, EvidenceReference
from adapt_ai.rag.knowledge_base_manager import KnowledgeBaseManager
from adapt_ai.rag.vector_store import VectorStore
from adapt_ai.rag.chunker import MedicalChunker
from adapt_ai.rag.embeddings import EmbeddingEngine
from adapt_ai.adapters.factory import get_model_adapter
from adapt_ai.security.auth import verify_api_key


router = APIRouter(prefix="/rag", tags=["RAG Knowledge Engine"])


def get_kb_manager() -> KnowledgeBaseManager:
    store = VectorStore()
    chunker = MedicalChunker()
    adapter = get_model_adapter()
    engine = EmbeddingEngine(adapter)
    return KnowledgeBaseManager(store, chunker, engine)


@router.post("/ingest", response_model=IngestionResponse, summary="Ingest Approved Medical Guidelines")
def ingest_guidelines(
    req: IngestionRequest,
    api_key: str = Security(verify_api_key),
    kb_mgr: KnowledgeBaseManager = Depends(get_kb_manager)
):
    """Parses, dedups, chunks, embeds, and indexes authoritative medical documents."""
    return kb_mgr.ingest_documents(req.documents)


@router.get("/stats", summary="Knowledge Base Statistics")
def get_knowledge_base_stats(api_key: str = Security(verify_api_key)):
    """Returns the total number of indexed guidelines, chunk vectors, and clinical categories."""
    store = VectorStore()
    return store.get_stats()


@router.get("/search", summary="Semantic Vector Search")
def search_passages(
    q: str = Query(..., min_length=2, description="Search query"),
    top_k: int = Query(4, ge=1, le=20),
    threshold: float = Query(0.2, ge=0.0, le=1.0),
    api_key: str = Security(verify_api_key)
):
    """Retrieves relevant guideline passages directly from the vector store."""
    adapter = get_model_adapter()
    engine = EmbeddingEngine(adapter)
    store = VectorStore()
    query_vec = engine.embed_query(q)
    try:
        results = store.similarity_search(query_vec, top_k=top_k, threshold=threshold)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "query": q,
        "results_found": len(results),
        "passages": [
            {
                "chunk_id": r[0]["chunk_id"],
                "doc_id": r[0]["doc_id"],
                "title": r[0]["title"],
                "source": r[0]["source"],
                "category": r[0]["category"],
                "text": r[0]["text"],
                "similarity_score": r[1]
            }
            for r in results
        ]
    }


@router.post("/reindex", summary="Re-index Knowledge Base Embeddings")
def reindex_knowledge_base(
    api_key: str = Security(verify_api_key),
    kb_mgr: KnowledgeBaseManager = Depends(get_kb_manager)
):
    """Safely re-computes dense vector embeddings for all indexed documents/chunks using the active model."""
    return kb_mgr.reindex_all()

