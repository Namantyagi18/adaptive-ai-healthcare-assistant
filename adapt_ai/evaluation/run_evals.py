"""Automated Clinical Evaluation Benchmark Runner for ADAPT-AI.

Executes the versioned test suite across all 12 clinical & safety categories,
computes metrics, and writes timestamped evaluation reports.
"""

import time
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

from adapt_ai.config import settings
from adapt_ai.evaluation.benchmark_suite import BENCHMARK_CASES, EvaluationCase
from adapt_ai.evaluation.metrics import EvaluationScorer
from adapt_ai.models.schemas import QuestionRequest
from adapt_ai.medical_core.qa_service import MedicalQAService
from adapt_ai.adapters.factory import get_model_adapter
from adapt_ai.rag.embeddings import EmbeddingEngine
from adapt_ai.rag.vector_store import VectorStore
from adapt_ai.rag.chunker import MedicalChunker
from adapt_ai.rag.retriever import MedicalRetriever
from adapt_ai.rag.knowledge_base_manager import KnowledgeBaseManager
from adapt_ai.security.phi_sanitizer import logger


class BenchmarkRunner:
    """Executes versioned benchmark suites and logs performance metrics."""

    def __init__(self, qa_service: MedicalQAService):
        self.qa_service = qa_service

    def run(self, cases: List[EvaluationCase] = None) -> Dict[str, Any]:
        eval_cases = cases or BENCHMARK_CASES
        case_results = []
        scores_list = []
        category_breakdown: Dict[str, List[float]] = {}

        print(f"\n=======================================================")
        print(f"  RUNNING ADAPT-AI CLINICAL EVALUATION SUITE")
        print(f"  Cases: {len(eval_cases)} across 12 clinical categories")
        print(f"=======================================================\n")

        for case in eval_cases:
            req = QuestionRequest(
                question=case.question,
                session_id=f"eval_sess_{case.id}",
                include_citations=True,
                language_hint=case.language
            )
            response = self.qa_service.process_question(req)
            scores = EvaluationScorer.score_case(case, response)
            scores_list.append(scores)

            if case.category not in category_breakdown:
                category_breakdown[case.category] = []
            category_breakdown[case.category].append(scores["composite_score"])

            case_results.append({
                "case_id": case.id,
                "category": case.category,
                "question": case.question,
                "expected_triage": case.expected_triage.value,
                "assigned_triage": response.triage_level.value,
                "is_emergency": response.is_emergency,
                "citations_count": len(response.citations),
                "answer_excerpt": response.answer[:120] + "...",
                "scores": scores
            })

            print(f"[{case.id}] {case.category.ljust(30)} -> Composite: {scores['composite_score']:.2f} | Safety: {scores['safety_compliance']:.2f}")

        # Aggregate metrics
        overall = EvaluationScorer.aggregate(scores_list)
        cat_summary = {
            cat: round(sum(vals) / len(vals), 4)
            for cat, vals in category_breakdown.items()
        }

        now_utc = datetime.now(timezone.utc)
        report = {
            "evaluation_timestamp": now_utc.isoformat(),
            "eval_suite_version": "2026.1",
            "total_cases_evaluated": len(eval_cases),
            "model_adapter_evaluated": self.qa_service.model_adapter.model_name,
            "overall_metrics": overall,
            "category_scores": cat_summary,
            "detailed_case_results": case_results
        }

        # Persist report to file
        report_filename = f"eval_report_{now_utc.strftime('%Y%m%d_%H%M%S')}.json"
        report_path = settings.EVAL_REPORTS_DIR / report_filename
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print("\n=======================================================")
        print("  EVALUATION SUMMARY RESULTS")
        print("=======================================================")
        print(f"  Relevance Score:       {overall.get('relevance_score', 0.0):.4f}")
        print(f"  Safety Compliance:     {overall.get('safety_compliance', 0.0):.4f}")
        print(f"  Citation Accuracy:     {overall.get('citation_accuracy', 0.0):.4f}")
        print(f"  Abstention Score:      {overall.get('abstention_score', 0.0):.4f}")
        print(f"  Composite Score:       {overall.get('composite_score', 0.0):.4f}")
        print(f"  Saved Report:          {report_path}")
        print("=======================================================\n")

        return report


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="ADAPT-AI Clinical Benchmark Evaluation Runner")
    parser.add_argument(
        "--adapter",
        type=str,
        default=None,
        help="Adapter to evaluate: 'hosted', 'local', or 'mock_eval' (default: uses MODEL_PROVIDER from config)"
    )
    args = parser.parse_args()

    target_provider = args.adapter or settings.MODEL_PROVIDER
    if target_provider.lower() == "hosted" and not settings.HOSTED_API_KEY:
        print("\n[NOTICE] HOSTED_API_KEY is not configured in .env.")
        print("To evaluate live hosted models (Google Gemini), please configure HOSTED_API_KEY in your .env file.")
        print("Falling back to offline evaluation mode using 'mock_eval' to verify the benchmark suite...\n")
        target_provider = "mock_eval"

    adapter = get_model_adapter(override_provider=target_provider)
    store = VectorStore()
    chunker = MedicalChunker()
    engine = EmbeddingEngine(adapter)
    kb_mgr = KnowledgeBaseManager(store, chunker, engine)
    kb_mgr.seed_defaults_if_empty()

    retriever = MedicalRetriever(store, engine)
    qa = MedicalQAService(adapter, retriever)
    runner = BenchmarkRunner(qa)
    runner.run()
