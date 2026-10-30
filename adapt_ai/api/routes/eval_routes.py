"""Evaluation Benchmark Endpoints."""

import json
from typing import List, Dict, Any
from pathlib import Path
from fastapi import APIRouter, Depends, Security, HTTPException
from adapt_ai.config import settings
from adapt_ai.evaluation.run_evals import BenchmarkRunner
from adapt_ai.medical_core.qa_service import MedicalQAService
from adapt_ai.adapters.factory import get_model_adapter
from adapt_ai.rag.vector_store import VectorStore
from adapt_ai.rag.embeddings import EmbeddingEngine
from adapt_ai.rag.retriever import MedicalRetriever
from adapt_ai.security.auth import verify_api_key


router = APIRouter(prefix="/evaluation", tags=["Clinical Evaluation"])


def get_qa_service() -> MedicalQAService:
    adapter = get_model_adapter()
    store = VectorStore()
    engine = EmbeddingEngine(adapter)
    retriever = MedicalRetriever(store, engine)
    return MedicalQAService(adapter, retriever)


@router.post("/run", summary="Execute Full 12-Category Clinical Evaluation Suite")
def run_evaluation(
    api_key: str = Security(verify_api_key),
    service: MedicalQAService = Depends(get_qa_service)
):
    """Executes versioned benchmark cases covering all clinical specialties, emergencies, and safety constraints."""
    runner = BenchmarkRunner(service)
    report = runner.run()
    return report


@router.get("/reports", summary="List Generated Evaluation Reports")
def list_reports(api_key: str = Security(verify_api_key)):
    """Returns list of all historical evaluation reports generated on the server."""
    report_files = sorted(settings.EVAL_REPORTS_DIR.glob("eval_report_*.json"), reverse=True)
    summaries = []
    for p in report_files:
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                summaries.append({
                    "filename": p.name,
                    "timestamp": data.get("evaluation_timestamp"),
                    "cases_evaluated": data.get("total_cases_evaluated"),
                    "composite_score": data.get("overall_metrics", {}).get("composite_score"),
                    "safety_compliance": data.get("overall_metrics", {}).get("safety_compliance")
                })
        except Exception:
            summaries.append({"filename": p.name, "error": "Unable to parse report file"})

    return {"reports": summaries}

