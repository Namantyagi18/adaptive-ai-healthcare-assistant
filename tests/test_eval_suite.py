"""Unit tests for Evaluation Suite and Metrics Scorer."""

import unittest
import tempfile
import gc
from pathlib import Path
from adapt_ai.evaluation.benchmark_suite import BENCHMARK_CASES
from adapt_ai.evaluation.metrics import EvaluationScorer
from adapt_ai.evaluation.run_evals import BenchmarkRunner
from adapt_ai.models.schemas import QuestionResponse, TriageLevel, EvidenceSufficiency, EvidenceReference
from adapt_ai.medical_core.qa_service import MedicalQAService
from adapt_ai.adapters.mock_eval_adapter import MockEvalAdapter
from adapt_ai.rag.vector_store import VectorStore
from adapt_ai.rag.chunker import MedicalChunker
from adapt_ai.rag.embeddings import EmbeddingEngine
from adapt_ai.rag.retriever import MedicalRetriever
from adapt_ai.rag.knowledge_base_manager import KnowledgeBaseManager


class TestEvaluationSuite(unittest.TestCase):

    def test_benchmark_covers_12_mandatory_categories(self):
        categories = {c.category for c in BENCHMARK_CASES}
        expected_categories = [
            "Common Symptoms",
            "Infectious Diseases",
            "Cancer Screening",
            "Cancer Red Flags",
            "Blood Disorders",
            "Cardiovascular & Respiratory",
            "Diabetes & Chronic Conditions",
            "Children's & Women's Health",
            "Medical Terminology & Reports",
            "Multilingual Questions",
            "Emergency Scenarios",
            "Ambiguous Questions",
            "Questions Lacking Sufficient Evidence"
        ]
        for exp in expected_categories:
            self.assertIn(exp, categories)

    def test_eval_scorer_emergency_accuracy(self):
        case = [c for c in BENCHMARK_CASES if c.id == "EMG-01"][0]
        # Correct emergency response
        resp_correct = QuestionResponse(
            answer="Call 911 immediately. FAST protocol for stroke.",
            triage_level=TriageLevel.EMERGENCY_IMMEDIATE,
            is_emergency=True,
            evidence_sufficiency=EvidenceSufficiency.SUFFICIENT,
            session_id="s1",
            model_used="test",
            latency_ms=10.0
        )
        score = EvaluationScorer.score_case(case, resp_correct)
        self.assertEqual(score["safety_compliance"], 1.0)

        # Failure to identify emergency
        resp_fail = QuestionResponse(
            answer="Drink some tea and rest.",
            triage_level=TriageLevel.SELF_CARE_EDUCATION,
            is_emergency=False,
            evidence_sufficiency=EvidenceSufficiency.SUFFICIENT,
            session_id="s2",
            model_used="test",
            latency_ms=10.0
        )
        score_fail = EvaluationScorer.score_case(case, resp_fail)
        self.assertEqual(score_fail["safety_compliance"], 0.0)

    def test_eval_scorer_abstention(self):
        case = [c for c in BENCHMARK_CASES if c.id == "EVI-01"][0]
        resp_abstained = QuestionResponse(
            answer="There is insufficient clinical evidence that garlic cures diabetes. Do not discontinue medical treatment.",
            triage_level=TriageLevel.SELF_CARE_EDUCATION,
            is_emergency=False,
            evidence_sufficiency=EvidenceSufficiency.INSUFFICIENT,
            session_id="s3",
            model_used="test",
            latency_ms=10.0
        )
        score = EvaluationScorer.score_case(case, resp_abstained)
        self.assertEqual(score["abstention_score"], 1.0)

    def test_benchmark_runner_executes_successfully(self):
        temp_dir = tempfile.TemporaryDirectory()
        try:
            store = VectorStore(Path(temp_dir.name) / "eval_run.db")
            adapter = MockEvalAdapter()
            engine = EmbeddingEngine(adapter)
            chunker = MedicalChunker()
            kb_mgr = KnowledgeBaseManager(store, chunker, engine)
            kb_mgr.seed_defaults_if_empty()

            retriever = MedicalRetriever(store, engine)
            qa = MedicalQAService(adapter, retriever)
            runner = BenchmarkRunner(qa)

            subset = BENCHMARK_CASES[:3]
            report = runner.run(cases=subset)
            self.assertEqual(report["total_cases_evaluated"], 3)
            self.assertIn("overall_metrics", report)
            self.assertGreater(report["overall_metrics"]["composite_score"], 0.0)
            store.close()
        finally:
            gc.collect()
            try:
                temp_dir.cleanup()
            except Exception:
                pass


if __name__ == "__main__":
    unittest.main()
