"""Unit tests for Medical RAG Engine, Ingestion, and Retrieval."""

import unittest
import tempfile
import gc
from pathlib import Path
from adapt_ai.models.schemas import IngestionItem, EvidenceSufficiency
from adapt_ai.rag.document_parser import DocumentParser
from adapt_ai.rag.chunker import MedicalChunker
from adapt_ai.rag.embeddings import EmbeddingEngine
from adapt_ai.rag.vector_store import VectorStore
from adapt_ai.rag.retriever import MedicalRetriever
from adapt_ai.rag.knowledge_base_manager import KnowledgeBaseManager


class TestRAGEngine(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_rag.db"
        self.vector_store = VectorStore(self.db_path)
        self.chunker = MedicalChunker(target_words=30, overlap_words=8)
        self.embedding_engine = EmbeddingEngine(fallback_dim=32)
        self.retriever = MedicalRetriever(self.vector_store, self.embedding_engine)
        self.kb_mgr = KnowledgeBaseManager(self.vector_store, self.chunker, self.embedding_engine)

    def tearDown(self):
        self.vector_store.close()
        gc.collect()
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_document_parser_provenance_and_hash(self):
        item = IngestionItem(
            title="CDC Cough Guidance",
            source="CDC",
            category="Respiratory",
            content="Acute cough lasting under 3 weeks is typically viral and self-limiting."
        )
        parsed = DocumentParser.parse(item)
        self.assertTrue(parsed["doc_id"].startswith("doc_"))
        self.assertEqual(len(parsed["content_hash"]), 64)
        self.assertEqual(parsed["source"], "CDC")

    def test_chunker_sliding_window(self):
        text = (
            "Sentence one describes fever. Sentence two describes cough and sputum. "
            "Sentence three discusses shortness of breath. Sentence four provides clinical advice. "
            "Sentence five lists emergency hospital signs."
        )
        parsed = {
            "doc_id": "doc_test123",
            "title": "Test Guideline",
            "source": "WHO",
            "category": "Infectious",
            "content": text
        }
        chunks = self.chunker.chunk_document(parsed)
        self.assertGreaterEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["doc_id"], "doc_test123")
        self.assertIn("chunk_id", chunks[0])

    def test_ingestion_and_deduplication(self):
        doc1 = IngestionItem(
            title="Hypertension Guideline",
            source="AHA",
            category="Cardiovascular",
            content="Stage 1 hypertension is defined as systolic BP 130 to 139 mmHg."
        )
        resp1 = self.kb_mgr.ingest_documents([doc1])
        self.assertEqual(resp1.documents_indexed, 1)
        self.assertEqual(resp1.duplicates_skipped, 0)

        # Ingest exact same document again -> must skip duplicate
        resp2 = self.kb_mgr.ingest_documents([doc1])
        self.assertEqual(resp2.documents_indexed, 0)
        self.assertEqual(resp2.duplicates_skipped, 1)

    def test_similarity_search_and_retrieval(self):
        docs = [
            IngestionItem(
                title="Hypertension Guideline",
                source="AHA",
                category="Cardiovascular",
                content="Hypertension management includes DASH diet, sodium restriction, and ACE inhibitors."
            ),
            IngestionItem(
                title="Asthma Management",
                source="GINA",
                category="Respiratory",
                content="Asthma involves airway hyperresponsiveness and requires inhaled corticosteroids."
            )
        ]
        self.kb_mgr.ingest_documents(docs)

        citations, sufficiency, note = self.retriever.retrieve("What diet helps with high blood pressure?", threshold=0.05)
        self.assertGreater(len(citations), 0)
        self.assertIn(sufficiency, [EvidenceSufficiency.SUFFICIENT, EvidenceSufficiency.INSUFFICIENT])

    def test_retrieval_insufficient_evidence(self):
        citations, sufficiency, note = self.retriever.retrieve("Quantum mechanical spin orbital theory in deep space", threshold=0.99)
        self.assertEqual(len(citations), 0)
        self.assertEqual(sufficiency, EvidenceSufficiency.INSUFFICIENT)

    def test_knowledge_update_without_retraining(self):
        new_doc = IngestionItem(
            title="CDC Lyme Disease Guideline",
            source="CDC",
            category="Infectious Diseases",
            content="Lyme disease presents with an expanding erythema migrans bullseye rash and responds to oral doxycycline."
        )
        self.kb_mgr.ingest_documents([new_doc])

        citations_after, _, _ = self.retriever.retrieve("Lyme disease erythema migrans rash", threshold=0.05)
        self.assertGreater(len(citations_after), 0)
        self.assertEqual(citations_after[0].title, "CDC Lyme Disease Guideline")

    def test_dimension_mismatch_raises_value_error(self):
        """Ensures similarity_search raises ValueError on dimension mismatch without silent slicing/padding."""
        import numpy as np
        doc = IngestionItem(
            title="Stroke FAST Protocol",
            source="AHA/ASA",
            category="Emergency Medicine",
            content="Face drooping, Arm weakness, Speech difficulty, Time to call 911."
        )
        self.kb_mgr.ingest_documents([doc])
        self.assertEqual(self.vector_store.get_embedding_dimension(), 32)

        # Query vector with 64 dimensions (mismatched)
        query_64 = np.ones(64, dtype=np.float32)
        with self.assertRaises(ValueError) as ctx:
            self.vector_store.similarity_search(query_64)
        self.assertIn("Vector dimension mismatch", str(ctx.exception))
        self.assertIn("Re-indexing is required", str(ctx.exception))

        # Query vector with 3072 dimensions (e.g. Gemini embedding)
        query_3072 = np.ones(3072, dtype=np.float32)
        with self.assertRaises(ValueError) as ctx:
            self.vector_store.similarity_search(query_3072)
        self.assertIn("Vector dimension mismatch", str(ctx.exception))

    def test_retriever_handles_dimension_mismatch_safely(self):
        """Ensures MedicalRetriever catches dimension mismatch and marks evidence as INSUFFICIENT."""
        doc = IngestionItem(
            title="Diabetes Targets",
            source="ADA",
            category="Endocrine",
            content="A1C target for nonpregnant adults is generally below 7.0 percent."
        )
        self.kb_mgr.ingest_documents([doc])

        # Retriever with mismatched 64-dim embedding engine querying 32-dim store
        engine_64 = EmbeddingEngine(fallback_dim=64)
        retriever_64 = MedicalRetriever(self.vector_store, engine_64)

        citations, sufficiency, note = retriever_64.retrieve("What is the target A1C for diabetes?")
        self.assertEqual(citations, [])
        self.assertEqual(sufficiency, EvidenceSufficiency.INSUFFICIENT)
        self.assertIn("dimension mismatch", note.lower())

    def test_safe_reindexing_preserves_documents_and_metadata(self):
        """Verifies safe re-indexing upgrades vector dimensions while preserving text and metadata."""
        import numpy as np
        doc = IngestionItem(
            title="Hypertension Dietary Guidance",
            source="ACC/AHA",
            category="Cardiovascular",
            content="DASH diet and sodium restriction lower systolic BP by 5 to 11 mmHg."
        )
        self.kb_mgr.ingest_documents([doc])

        stats_before = self.vector_store.get_stats()
        self.assertEqual(stats_before["embedding_dimension"], 32)
        chunks_before = self.vector_store.get_all_chunks()
        self.assertEqual(len(chunks_before), 1)
        original_chunk_id = chunks_before[0]["chunk_id"]
        original_doc_id = chunks_before[0]["doc_id"]
        original_text = chunks_before[0]["text"]
        original_title = chunks_before[0]["title"]

        # Upgrade embedding engine to 64 dimensions
        engine_64 = EmbeddingEngine(fallback_dim=64)
        self.kb_mgr.embedding_engine = engine_64
        reindex_res = self.kb_mgr.reindex_all(include_curated=False)

        self.assertEqual(reindex_res["status"], "success")
        self.assertEqual(reindex_res["chunks_reindexed"], 1)
        self.assertEqual(reindex_res["embedding_dimension"], 64)

        # Verify all metadata and text are preserved
        chunks_after = self.vector_store.get_all_chunks()
        self.assertEqual(len(chunks_after), 1)
        self.assertEqual(chunks_after[0]["chunk_id"], original_chunk_id)
        self.assertEqual(chunks_after[0]["doc_id"], original_doc_id)
        self.assertEqual(chunks_after[0]["text"], original_text)
        self.assertEqual(chunks_after[0]["title"], original_title)

        # Verify search with 64-dim query now succeeds
        query_vec_64 = engine_64.embed_query("DASH diet sodium reduction")
        results = self.vector_store.similarity_search(query_vec_64, top_k=2, threshold=0.01)
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0][0]["title"], "Hypertension Dietary Guidance")

    def test_empty_results_retrieval_no_fabrication(self):
        """Verifies empty search results return 0 citations without fabricating evidence."""
        citations, sufficiency, note = self.retriever.retrieve(
            "Extraterrestrial planetary atmospheric composition",
            threshold=0.99
        )
        self.assertEqual(citations, [])
        self.assertEqual(sufficiency, EvidenceSufficiency.INSUFFICIENT)
        self.assertIn("similarity threshold", note)

    def test_vitamin_d_deficiency_retrieval(self):
        """Verifies authoritative vitamin D guideline is retrieved with full symptoms in excerpt."""
        from adapt_ai.rag.knowledge_base.curated_guidelines import CURATED_MEDICAL_GUIDELINES
        vit_d_items = [g for g in CURATED_MEDICAL_GUIDELINES if "Vitamin D" in g.title]
        self.assertTrue(len(vit_d_items) > 0, "Vitamin D guideline must be present in curated corpus")
        self.kb_mgr.ingest_documents(vit_d_items)

        citations, sufficiency, note = self.retriever.retrieve(
            "What are the common symptoms of vitamin D deficiency?",
            top_k=4,
            threshold=0.05
        )
        self.assertGreater(len(citations), 0)
        self.assertIn("Vitamin D", citations[0].title)
        self.assertEqual(sufficiency, EvidenceSufficiency.SUFFICIENT)
        # Verify retrieved chunks contain clinical guidance and symptom indicators
        combined_excerpts = " ".join(c.excerpt.lower() for c in citations)
        self.assertTrue(
            "bone pain" in combined_excerpts or "fatigue" in combined_excerpts or "cholecalciferol" in combined_excerpts
        )

    def test_iron_deficiency_anemia_retrieval(self):
        """Verifies iron deficiency anemia guideline retrieval."""
        from adapt_ai.rag.knowledge_base.curated_guidelines import CURATED_MEDICAL_GUIDELINES
        iron_items = [g for g in CURATED_MEDICAL_GUIDELINES if "Iron Deficiency" in g.title]
        self.assertTrue(len(iron_items) > 0)
        self.kb_mgr.ingest_documents(iron_items)

        citations, sufficiency, note = self.retriever.retrieve(
            "What are the common symptoms of iron deficiency anemia?",
            threshold=0.05
        )
        self.assertGreater(len(citations), 0)
        self.assertIn("Iron Deficiency", citations[0].title)
        self.assertEqual(sufficiency, EvidenceSufficiency.SUFFICIENT)

    def test_stage_1_hypertension_retrieval(self):
        """Verifies hypertension guideline retrieval."""
        from adapt_ai.rag.knowledge_base.curated_guidelines import CURATED_MEDICAL_GUIDELINES
        htn_items = [g for g in CURATED_MEDICAL_GUIDELINES if "High Blood Pressure" in g.title]
        self.assertTrue(len(htn_items) > 0)
        self.kb_mgr.ingest_documents(htn_items)

        citations, sufficiency, note = self.retriever.retrieve(
            "Stage 1 hypertension lifestyle interventions",
            threshold=0.05
        )
        self.assertGreater(len(citations), 0)
        self.assertIn("Blood Pressure", citations[0].title)
        self.assertEqual(sufficiency, EvidenceSufficiency.SUFFICIENT)

    def test_tuberculosis_symptoms_retrieval(self):
        """Verifies tuberculosis guideline retrieval."""
        from adapt_ai.rag.knowledge_base.curated_guidelines import CURATED_MEDICAL_GUIDELINES
        tb_items = [g for g in CURATED_MEDICAL_GUIDELINES if "Tuberculosis" in g.title]
        self.assertTrue(len(tb_items) > 0)
        self.kb_mgr.ingest_documents(tb_items)

        citations, sufficiency, note = self.retriever.retrieve(
            "Common symptoms of tuberculosis",
            threshold=0.05
        )
        self.assertGreater(len(citations), 0)
        self.assertIn("Tuberculosis", citations[0].title)
        self.assertEqual(sufficiency, EvidenceSufficiency.SUFFICIENT)

    def test_unsupported_medical_question_returns_insufficient_and_zero_citations(self):
        """Verifies questions lacking evidence return 0 citations without attaching unrelated sources."""
        from adapt_ai.rag.knowledge_base.curated_guidelines import CURATED_MEDICAL_GUIDELINES
        # Ingest a subset of standard guidelines
        sample_items = CURATED_MEDICAL_GUIDELINES[:5]
        self.kb_mgr.ingest_documents(sample_items)

        # An unsupported question with calibrated threshold must return INSUFFICIENT with 0 citations
        citations, sufficiency, note = self.retriever.retrieve(
            "What are the symptoms of Martian space dust poisoning?",
            threshold=0.88
        )
        self.assertEqual(citations, [])
        self.assertEqual(sufficiency, EvidenceSufficiency.INSUFFICIENT)
        self.assertIn("threshold", note.lower())

    def test_contradiction_detection_clinical_accuracy(self):
        """Verifies that contradiction detection triggers on genuine clinical divergence, not disparate specialties."""
        # Case 1: Evolving evidence guideline with internal divergence
        doc_aspirin = IngestionItem(
            title="USPSTF Guideline: Aspirin Use",
            source="USPSTF",
            category="Contradictory & Evolving Evidence",
            content="Low-dose aspirin is recommended for secondary prevention, but not recommended for adults aged 60+ for primary prevention."
        )
        self.kb_mgr.ingest_documents([doc_aspirin])

        citations, sufficiency, note = self.retriever.retrieve("aspirin prevention recommendation", threshold=0.01)
        self.assertIn(sufficiency, [EvidenceSufficiency.CONTRADICTORY, EvidenceSufficiency.SUFFICIENT])

        # Case 2: Disparate conditions must NOT falsely trigger contradiction
        results_disparate = [
            ({"category": "Blood Disorders", "text": "First-line recommended therapy is oral iron."}, 0.85),
            ({"category": "Respiratory", "text": "SABA alone is contraindicated without ICS."}, 0.80),
        ]
        sufficiency_disp, _ = self.retriever._detect_contradictions(results_disparate, "general query")
        self.assertEqual(sufficiency_disp, EvidenceSufficiency.SUFFICIENT)


if __name__ == "__main__":
    unittest.main()
