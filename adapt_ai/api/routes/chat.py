"""Medical Chat and Question Answering Endpoints."""

from typing import List
from fastapi import APIRouter, Depends, Security, HTTPException
from adapt_ai.models.schemas import QuestionRequest, QuestionResponse, ChatMessage
from adapt_ai.medical_core.qa_service import MedicalQAService
from adapt_ai.medical_core.session_manager import session_manager
from adapt_ai.adapters.factory import get_model_adapter
from adapt_ai.rag.vector_store import VectorStore
from adapt_ai.rag.embeddings import EmbeddingEngine
from adapt_ai.rag.retriever import MedicalRetriever
from adapt_ai.security.auth import verify_api_key


router = APIRouter(prefix="/chat", tags=["Medical Question Answering"])


def get_qa_service() -> MedicalQAService:
    adapter = get_model_adapter()
    store = VectorStore()
    engine = EmbeddingEngine(adapter)
    retriever = MedicalRetriever(store, engine)
    return MedicalQAService(adapter, retriever)


@router.post("/question", response_model=QuestionResponse, summary="Submit Healthcare Question")
def ask_question(
    req: QuestionRequest,
    api_key: str = Security(verify_api_key),
    service: MedicalQAService = Depends(get_qa_service)
):
    """Processes healthcare queries under clinical guardrails, returning citations and triage."""
    return service.process_question(req)


@router.get("/history/{session_id}", response_model=List[ChatMessage], summary="Retrieve Conversation History")
def get_session_history(
    session_id: str,
    api_key: str = Security(verify_api_key)
):
    """Returns conversation history for a given session."""
    return session_manager.get_history(session_id)


@router.delete("/session/{session_id}", summary="Clear Conversation Session")
def delete_session(
    session_id: str,
    api_key: str = Security(verify_api_key)
):
    """Ends and clears history for a given conversation session."""
    session_manager.clear()
    return {"status": "cleared", "session_id": session_id}

