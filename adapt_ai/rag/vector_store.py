"""Persistent SQLite and NumPy vector store for medical knowledge retrieval.

Enforces document deduplication, provenance tracking, and fast cosine similarity search.
Enables real-time knowledge base updates without requiring model retraining.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

from adapt_ai.config import settings
from adapt_ai.security.phi_sanitizer import logger


class VectorStore:
    """Persistent vector database combining SQLite for metadata and NumPy for linear algebra."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (settings.VECTOR_INDEX_DIR / "medical_knowledge.db")
        self._init_db()
        self._load_memory_index()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        """Initializes database tables if not existing."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    doc_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    source TEXT NOT NULL,
                    category TEXT NOT NULL,
                    content_hash TEXT UNIQUE NOT NULL,
                    version TEXT,
                    url TEXT,
                    ingested_at REAL NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id TEXT PRIMARY KEY,
                    doc_id TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    source TEXT NOT NULL,
                    category TEXT NOT NULL,
                    text TEXT NOT NULL,
                    embedding BLOB NOT NULL,
                    FOREIGN KEY (doc_id) REFERENCES documents(doc_id) ON DELETE CASCADE
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def _load_memory_index(self) -> None:
        """Loads embeddings into in-memory NumPy matrix for low-latency similarity queries."""
        self.chunk_meta: List[Dict[str, Any]] = []
        embeddings_list: List[np.ndarray] = []

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT chunk_id, doc_id, chunk_index, title, source, category, text, embedding FROM chunks")
            rows = cursor.fetchall()
            for r in rows:
                chunk_id, doc_id, idx, title, src, cat, text, emb_blob = r
                emb_arr = np.frombuffer(emb_blob, dtype=np.float32)
                self.chunk_meta.append({
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "chunk_index": idx,
                    "title": title,
                    "source": src,
                    "category": cat,
                    "text": text
                })
                embeddings_list.append(emb_arr)
        finally:
            conn.close()

        if embeddings_list:
            dims = {e.shape[0] for e in embeddings_list}
            if len(dims) == 1:
                self.matrix = np.vstack(embeddings_list)
            else:
                # Mixed dimensions detected in database (e.g. during reindex migration)
                from collections import Counter
                dim_counts = Counter(e.shape[0] for e in embeddings_list)
                dominant_dim = dim_counts.most_common(1)[0][0]
                logger.warning(
                    f"Mixed vector dimensions detected in storage {dict(dim_counts)}. "
                    f"Filtering in-memory index to dominant dimension {dominant_dim}."
                )
                filtered_meta = []
                filtered_embs = []
                for meta, emb in zip(self.chunk_meta, embeddings_list):
                    if emb.shape[0] == dominant_dim:
                        filtered_meta.append(meta)
                        filtered_embs.append(emb)
                self.chunk_meta = filtered_meta
                self.matrix = np.vstack(filtered_embs)
        else:
            self.matrix = np.empty((0, 128), dtype=np.float32)
        logger.info(f"Loaded vector store index with {len(self.chunk_meta)} chunks.")

    def has_document_hash(self, content_hash: str) -> bool:
        """Checks if a document with the specified content hash is already stored."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM documents WHERE content_hash = ? LIMIT 1", (content_hash,))
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def add_document(
        self,
        doc_meta: Dict[str, Any],
        chunks: List[Dict[str, Any]],
        embeddings: np.ndarray
    ) -> bool:
        """Inserts a new guideline document and its chunk embeddings.
        
        Returns:
            bool: True if inserted, False if skipped as duplicate.
        """
        content_hash = doc_meta["content_hash"]
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT doc_id FROM documents WHERE content_hash = ?", (content_hash,))
            existing = cursor.fetchone()
            if existing:
                logger.info(f"Document '{doc_meta['title']}' already indexed (hash {content_hash[:8]}). Skipping duplicate.")
                return False

            cursor.execute(
                """
                INSERT INTO documents (doc_id, title, source, category, content_hash, version, url, ingested_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    doc_meta["doc_id"],
                    doc_meta["title"],
                    doc_meta["source"],
                    doc_meta["category"],
                    content_hash,
                    doc_meta.get("version", "1.0"),
                    doc_meta.get("url"),
                    doc_meta["ingested_at"]
                )
            )

            chunk_records = []
            for i, chunk in enumerate(chunks):
                emb_blob = embeddings[i].astype(np.float32).tobytes()
                chunk_records.append((
                    chunk["chunk_id"],
                    chunk["doc_id"],
                    chunk["chunk_index"],
                    chunk["title"],
                    chunk["source"],
                    chunk["category"],
                    chunk["text"],
                    emb_blob
                ))

            cursor.executemany(
                """
                INSERT INTO chunks (chunk_id, doc_id, chunk_index, title, source, category, text, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                chunk_records
            )
            conn.commit()
        finally:
            conn.close()

        # Refresh memory index
        self._load_memory_index()
        return True

    def similarity_search(
        self,
        query_vector: np.ndarray,
        top_k: int = 4,
        threshold: float = 0.2
    ) -> List[Tuple[Dict[str, Any], float]]:
        """Finds top-K most similar chunks using cosine similarity.
        
        Validates that the query vector dimension strictly matches the stored index dimension.
        Raises ValueError if a dimension mismatch is detected, prompting re-indexing.
        """
        if len(self.chunk_meta) == 0 or self.matrix.shape[0] == 0:
            return []

        # Validate vector dimensions strictly
        dim = self.matrix.shape[1]
        query_dim = query_vector.shape[0]
        if query_dim != dim:
            raise ValueError(
                f"Vector dimension mismatch: query vector has dimension {query_dim}, "
                f"but vector store index has dimension {dim}. Re-indexing is required."
            )

        qv = query_vector
        scores = np.dot(self.matrix, qv)
        ranked_indices = np.argsort(scores)[::-1]

        results = []
        for idx in ranked_indices:
            score = float(scores[idx])
            if score >= threshold:
                results.append((self.chunk_meta[idx], round(score, 4)))
            if len(results) >= top_k:
                break

        return results

    def get_embedding_dimension(self) -> int:
        """Returns the embedding vector dimension of the loaded index, or 0 if empty."""
        if hasattr(self, "matrix") and self.matrix is not None and self.matrix.shape[0] > 0:
            return int(self.matrix.shape[1])
        return 0

    def get_all_chunks(self) -> List[Dict[str, Any]]:
        """Returns metadata and text for all indexed chunks without loading raw blobs."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT chunk_id, doc_id, chunk_index, title, source, category, text FROM chunks ORDER BY doc_id, chunk_index"
            )
            rows = cursor.fetchall()
            return [
                {
                    "chunk_id": r[0],
                    "doc_id": r[1],
                    "chunk_index": r[2],
                    "title": r[3],
                    "source": r[4],
                    "category": r[5],
                    "text": r[6]
                }
                for r in rows
            ]
        finally:
            conn.close()

    def update_chunk_embeddings(
        self,
        chunk_embeddings: List[Tuple[str, np.ndarray]],
        reload_memory: bool = True
    ) -> int:
        """Safely updates embeddings for existing chunks in-place, preserving all metadata and documents.
        
        Args:
            chunk_embeddings: List of (chunk_id, embedding_array) tuples.
            reload_memory: Whether to refresh the in-memory numpy matrix immediately.
            
        Returns:
            int: Number of chunk embeddings updated.
        """
        if not chunk_embeddings:
            return 0

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            update_data = [
                (np.ascontiguousarray(emb, dtype=np.float32).tobytes(), chunk_id)
                for chunk_id, emb in chunk_embeddings
            ]
            cursor.executemany(
                "UPDATE chunks SET embedding = ? WHERE chunk_id = ?",
                update_data
            )
            conn.commit()
        finally:
            conn.close()

        # Refresh memory index with updated vectors if requested
        if reload_memory:
            self._load_memory_index()
        return len(chunk_embeddings)

    def get_stats(self) -> Dict[str, Any]:
        """Returns statistics on vector store size and indexed guidelines."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM documents")
            doc_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM chunks")
            chunk_count = cursor.fetchone()[0]
            cursor.execute("SELECT DISTINCT category FROM documents")
            categories = [r[0] for r in cursor.fetchall()]
        finally:
            conn.close()

        embedding_dim = self.get_embedding_dimension()

        return {
            "total_documents": doc_count,
            "total_chunks": chunk_count,
            "embedding_dimension": embedding_dim,
            "categories": sorted(categories)
        }

    def clear(self) -> None:
        """Flushes all stored documents and chunks."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chunks")
            cursor.execute("DELETE FROM documents")
            conn.commit()
        finally:
            conn.close()
        self._load_memory_index()

    def close(self) -> None:
        """Releases memory matrix."""
        self.chunk_meta = []
        self.matrix = np.empty((0, 128), dtype=np.float32)
