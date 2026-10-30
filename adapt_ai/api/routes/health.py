"""Health, System Telemetry, and Compute Resource Endpoints."""

from fastapi import APIRouter, Depends
from adapt_ai.config import settings
from adapt_ai.models.schemas import HardwareResourceReport, ModelRecommendation
from adapt_ai.training.resource_inspector import ResourceInspector
from adapt_ai.training.model_recommender import ModelRecommender
from adapt_ai.adapters.factory import get_model_adapter
from adapt_ai.rag.vector_store import VectorStore


router = APIRouter(prefix="/health", tags=["Health & Telemetry"])


@router.get("", summary="System Health and Component Status")
def get_health():
    """Returns operational status of model adapter, vector store, and system configuration."""
    adapter = get_model_adapter()
    store = VectorStore()
    stats = store.get_stats()

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.APP_ENV,
        "components": {
            "model_adapter": {
                "name": adapter.model_name,
                "healthy": adapter.is_healthy(),
                "configured_provider": settings.MODEL_PROVIDER
            },
            "vector_store": {
                "total_documents": stats["total_documents"],
                "total_chunks": stats["total_chunks"],
                "categories": stats["categories"]
            }
        }
    }


@router.get("/resources", response_model=HardwareResourceReport, summary="Inspect Available Compute Resources")
def inspect_hardware():
    """Inspects local hardware (CPU, RAM, GPU, VRAM) to verify training & inference feasibility."""
    return ResourceInspector.inspect()


@router.get("/recommendation", response_model=ModelRecommendation, summary="Model Architecture Recommendation")
def get_model_recommendation():
    """Recommends optimal clinical models based on licenses, hardware, benchmarks, and costs."""
    hardware = ResourceInspector.inspect()
    return ModelRecommender.recommend(hardware)

