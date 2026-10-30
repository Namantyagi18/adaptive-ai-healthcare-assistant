"""Patient Authentication and Session Management Endpoints."""

from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Security
from adapt_ai.security.auth import issue_patient_session_token, verify_api_key


router = APIRouter(prefix="/auth", tags=["Patient Authentication"])


class SessionCreateRequest(BaseModel):
    session_id: Optional[str] = Field(None, description="Optional persistent client session ID")


class SessionResponse(BaseModel):
    session_id: str
    token: str
    token_type: str = "Bearer"
    expires_in: int
    expires_at: int


@router.post("/session", response_model=SessionResponse, summary="Obtain Secure Patient Session Token")
def create_patient_session(req: Optional[SessionCreateRequest] = None):
    """Issues a signed, time-limited patient session token.
    
    Allows ordinary patient web clients to access the healthcare assistant without
    possessing or exposing master server API secrets.
    """
    sid = req.session_id if req else None
    return issue_patient_session_token(session_id=sid)


@router.get("/session/verify", summary="Verify Active Session or API Key")
def verify_session(api_key: str = Security(verify_api_key)):
    """Verifies that the provided API key or patient session token is active and valid."""
    is_patient = api_key.startswith("pat_")
    return {
        "status": "authenticated",
        "auth_type": "patient_session" if is_patient else "master_api_key",
    }

