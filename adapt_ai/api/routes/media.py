"""Media and Diagnostic Document Upload Processing Endpoints."""

import base64
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Security, HTTPException
from adapt_ai.models.schemas import ImageUploadResponse
from adapt_ai.vision_docs.extractor import DocumentVisionPipeline
from adapt_ai.adapters.factory import get_model_adapter
from adapt_ai.security.auth import verify_api_key


router = APIRouter(prefix="/media", tags=["Image and Document Processing"])


class DocumentUploadPayload(BaseModel):
    filename: str = Field(..., description="Original filename including extension (e.g. scan.png, lab.txt)")
    content_base64: str = Field(..., description="Base64 encoded binary contents of the file")
    prompt: Optional[str] = Field(None, description="Optional diagnostic interpretation question")


@router.post("/upload", response_model=ImageUploadResponse, summary="Upload Diagnostic Document or Image")
def upload_document(
    payload: DocumentUploadPayload,
    api_key: str = Security(verify_api_key)
):
    """Validates, quarantines, extracts content, and cautiously analyzes medical documents/images."""
    try:
        file_bytes = base64.b64decode(payload.content_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 payload: {str(e)}")

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file payload is empty.")

    adapter = get_model_adapter()
    pipeline = DocumentVisionPipeline(adapter)

    try:
        result = pipeline.process_file(
            filename=payload.filename,
            file_bytes=file_bytes,
            user_prompt=payload.prompt
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
