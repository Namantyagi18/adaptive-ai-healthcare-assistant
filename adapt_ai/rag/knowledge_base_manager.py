"""Knowledge Base Manager for seeding, indexing, and dynamically updating medical guidelines."""

from typing import List, Dict, Any
from adapt_ai.models.schemas import IngestionItem, IngestionResponse
from adapt_ai.rag.document_parser import DocumentParser
from adapt_ai.rag.chunker import MedicalChunker
from adapt_ai.rag.embeddings import EmbeddingEngine
from adapt_ai.rag.vector_store import VectorStore
from adapt_ai.rag.knowledge_base.curated_guidelines import CURATED_MEDICAL_GUIDELINES
from adapt_ai.security.phi_sanitizer import logger


class KnowledgeBaseManager:
    """Coordinates document ingestion, chunking, embedding, and vector store indexing."""

    def __init__(
        self,
        vector_store: VectorStore,
        chunker: MedicalChunker,
        embedding_engine: EmbeddingEngine
    ):
        self.vector_store = vector_store
        self.chunker = chunker
        self.embedding_engine = embedding_engine

    def ingest_documents(self, documents: List[IngestionItem]) -> IngestionResponse:
        """Processes and indexes a batch of medical documents into the vector store."""
        indexed_count = 0
        skipped_duplicates = 0
        total_chunks_created = 0

        for doc_item in documents:
            try:
                parsed = DocumentParser.parse(doc_item)
                if self.vector_store.has_document_hash(parsed["content_hash"]):
                    logger.info(f"Document '{doc_item.title}' already indexed (hash {parsed['content_hash'][:8]}). Skipping duplicate.")
                    skipped_duplicates += 1
                    continue

                chunks = self.chunker.chunk_document(parsed)
                if not chunks:
                    continue

                chunk_texts = [c["text"] for c in chunks]
                embeddings = self.embedding_engine.embed_documents(chunk_texts)

                inserted = self.vector_store.add_document(parsed, chunks, embeddings)
                if inserted:
                    indexed_count += 1
                    total_chunks_created += len(chunks)
                else:
                    skipped_duplicates += 1
            except Exception as e:
                logger.error(f"Error ingesting document '{doc_item.title}': {e}")

        stats = self.vector_store.get_stats()
        return IngestionResponse(
            status="success",
            documents_indexed=indexed_count,
            chunks_created=total_chunks_created,
            duplicates_skipped=skipped_duplicates,
            total_vectors_in_store=stats["total_chunks"]
        )

    def seed_defaults_if_empty(self) -> IngestionResponse:
        """Seeds curated medical guidelines if empty or re-indexes if a dimension mismatch is detected."""
        stats = self.vector_store.get_stats()
        if stats["total_chunks"] == 0:
            logger.info("Vector store is empty. Seeding default curated medical guidelines...")
            return self.ingest_documents(CURATED_MEDICAL_GUIDELINES)

        # Check for dimension mismatch on existing vectors
        stored_dim = stats.get("embedding_dimension", 0)
        active_dim = self.embedding_engine.get_embedding_dim()
        if stored_dim > 0 and active_dim > 0 and stored_dim != active_dim:
            logger.warning(
                f"Vector store dimension mismatch detected (stored: {stored_dim}, active: {active_dim}). "
                f"Initiating safe re-indexing of existing medical documents..."
            )
            reindex_res = self.reindex_all(include_curated=True)
            new_stats = self.vector_store.get_stats()
            return IngestionResponse(
                status="reindexed_after_dimension_mismatch",
                documents_indexed=reindex_res.get("curated_guidelines_added", 0),
                chunks_created=reindex_res.get("chunks_reindexed", 0),
                duplicates_skipped=0,
                total_vectors_in_store=new_stats["total_chunks"]
            )

        # Ingest any newly added or missing curated medical guidelines
        missing_curated = []
        for item in CURATED_MEDICAL_GUIDELINES:
            c_hash = DocumentParser.compute_content_hash(item.content.strip())
            if not self.vector_store.has_document_hash(c_hash):
                missing_curated.append(item)

        if missing_curated:
            logger.info(f"Ingesting {len(missing_curated)} newly added curated guideline(s)...")
            return self.ingest_documents(missing_curated)

        logger.info(f"Vector store already contains {stats['total_chunks']} chunks (dim: {stored_dim}). All curated guidelines are present.")
        return IngestionResponse(
            status="already_seeded",
            documents_indexed=0,
            chunks_created=0,
            duplicates_skipped=len(CURATED_MEDICAL_GUIDELINES),
            total_vectors_in_store=stats["total_chunks"]
        )

    def reindex_all(self, batch_size: int = 16, include_curated: bool = True) -> Dict[str, Any]:
        """Safely re-indexes all existing documents and chunks using the active embedding model.
        
        Preserves all source documents, categories, titles, provenance, and chunk text.
        Updates the dense vector representations in-place.
        """
        existing_chunks = self.vector_store.get_all_chunks()
        reindexed_count = 0

        if existing_chunks:
            logger.info(f"Re-indexing {len(existing_chunks)} existing chunks in vector store...")
            # Process in batches to respect API limits
            for i in range(0, len(existing_chunks), batch_size):
                batch = existing_chunks[i:i + batch_size]
                texts = [c["text"] for c in batch]
                embeddings = self.embedding_engine.embed_documents(texts)
                chunk_embeddings = [
                    (batch[j]["chunk_id"], embeddings[j])
                    for j in range(len(batch))
                ]
                self.vector_store.update_chunk_embeddings(chunk_embeddings, reload_memory=False)
                reindexed_count += len(chunk_embeddings)

            # Reload memory index after all chunks are updated
            self.vector_store._load_memory_index()

        curated_ingested = 0
        if include_curated:
            # Ingest any missing curated medical guidelines
            resp = self.ingest_documents(CURATED_MEDICAL_GUIDELINES)
            curated_ingested = resp.documents_indexed

        stats = self.vector_store.get_stats()
        return {
            "status": "success",
            "chunks_reindexed": reindexed_count,
            "curated_guidelines_added": curated_ingested,
            "total_documents": stats["total_documents"],
            "total_chunks": stats["total_chunks"],
            "embedding_dimension": stats["embedding_dimension"]
        }

