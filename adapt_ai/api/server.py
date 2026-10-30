"""FastAPI Server for ADAPT-AI Medical Healthcare System.

Implements rate limiting, PHI audit logging, CORS security, exception handling,
and modular healthcare endpoints using pure ASGI middlewares.
"""

import time
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from adapt_ai.config import settings
from adapt_ai.security.rate_limiter import rate_limiter
from adapt_ai.security.phi_sanitizer import sanitize_text, logger
from adapt_ai.models.exceptions import (
    AdaptAIException, ProviderError, RateLimitExceededError,
    SafetyViolationError, ResourceInsufficientError, InvalidDocumentError
)
from adapt_ai.rag.vector_store import VectorStore
from adapt_ai.rag.chunker import MedicalChunker
from adapt_ai.rag.embeddings import EmbeddingEngine
from adapt_ai.rag.knowledge_base_manager import KnowledgeBaseManager
from adapt_ai.adapters.factory import get_model_adapter

# Import route submodules
from adapt_ai.api.routes.health import router as health_router
from adapt_ai.api.routes.chat import router as chat_router
from adapt_ai.api.routes.rag import router as rag_router
from adapt_ai.api.routes.media import router as media_router
from adapt_ai.api.routes.training import router as training_router
from adapt_ai.api.routes.eval_routes import router as eval_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifespan events."""
    logger.info("==================================================")
    logger.info(f"Initializing {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.APP_ENV} | Model Provider: {settings.MODEL_PROVIDER}")
    logger.info("==================================================")

    # Automatically seed knowledge base with curated medical guidelines if empty
    try:
        store = VectorStore()
        chunker = MedicalChunker()
        adapter = get_model_adapter()
        engine = EmbeddingEngine(adapter)
        kb_mgr = KnowledgeBaseManager(store, chunker, engine)
        seed_result = kb_mgr.seed_defaults_if_empty()
        logger.info(f"RAG Knowledge Base Status: {seed_result.status} (Total vectors: {seed_result.total_vectors_in_store})")
    except Exception as e:
        logger.error(f"Failed to initialize RAG knowledge base on startup: {e}")

    yield

    logger.info("Shutting down ADAPT-AI server. Releasing resources...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=(
        "Advanced, modular healthcare question-answering and clinical access system. "
        "Provides provider-independent model adapters, evidence-grounded RAG, clinical safety guardrails, "
        "diagnostic document processing, and hardware-aware training evaluation."
    ),
    swagger_ui_parameters={"persistAuthorization": True},
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PureASGIRateLimitingAndPHIMiddleware:
    """Pure ASGI middleware for high-performance rate limiting and PHI audit logging without buffering."""

    def __init__(self, asgi_app):
        self.asgi_app = asgi_app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.asgi_app(scope, receive, send)

        client = scope.get("client")
        client_ip = client[0] if client else "unknown"
        path = scope.get("path", "")

        # Exclude public health probe from rate limits
        if not path.endswith("/health"):
            allowed, remaining, retry_after = rate_limiter.is_allowed(client_ip)
            if not allowed:
                body = json.dumps({
                    "error": "RateLimitExceeded",
                    "message": f"Client request rate limit exceeded. Retry after {retry_after} seconds.",
                    "retry_after_seconds": retry_after
                }).encode("utf-8")
                await send({
                    "type": "http.response.start",
                    "status": 429,
                    "headers": [
                        (b"content-type", b"application/json"),
                        (b"retry-after", str(int(retry_after) + 1).encode("ascii"))
                    ]
                })
                await send({
                    "type": "http.response.body",
                    "body": body,
                    "more_body": False
                })
                return

        start_time = time.time()
        sanitized_path = sanitize_text(path)
        logger.info(f"Incoming {scope['method']} {sanitized_path} from client {client_ip}")

        async def logging_send(message):
            if message["type"] == "http.response.start":
                duration_ms = round((time.time() - start_time) * 1000, 2)
                status_code = message.get("status", 200)
                logger.info(f"Completed {scope['method']} {sanitized_path} -> Status {status_code} ({duration_ms}ms)")
            await send(message)

        await self.asgi_app(scope, receive, logging_send)


# Attach pure ASGI middleware
app.add_middleware(PureASGIRateLimitingAndPHIMiddleware)


# Global Exception Handlers
@app.exception_handler(ProviderError)
async def provider_error_handler(request: Request, exc: ProviderError):
    if exc.status_code == 429:
        http_status = status.HTTP_429_TOO_MANY_REQUESTS
    elif exc.status_code == 504:
        http_status = status.HTTP_504_GATEWAY_TIMEOUT
    elif exc.status_code == 503:
        http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        http_status = status.HTTP_502_BAD_GATEWAY

    return JSONResponse(
        status_code=http_status,
        content={
            "error": "UpstreamProviderError",
            "provider": exc.provider,
            "upstream_status": exc.status_code,
            "message": exc.message,
            "details": exc.details
        }
    )


@app.exception_handler(SafetyViolationError)
async def safety_violation_handler(request: Request, exc: SafetyViolationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "SafetyViolation",
            "message": exc.message,
            "category": exc.category
        }
    )


@app.exception_handler(ResourceInsufficientError)
async def resource_error_handler(request: Request, exc: ResourceInsufficientError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ResourceInsufficient",
            "message": exc.message,
            "details": exc.details
        }
    )


@app.exception_handler(InvalidDocumentError)
async def invalid_doc_handler(request: Request, exc: InvalidDocumentError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "InvalidDocument",
            "message": exc.message
        }
    )


# Attach Route Blueprints under /api/v1
API_V1_PREFIX = "/api/v1"
app.include_router(health_router, prefix=API_V1_PREFIX)
app.include_router(chat_router, prefix=API_V1_PREFIX)
app.include_router(rag_router, prefix=API_V1_PREFIX)
app.include_router(media_router, prefix=API_V1_PREFIX)
app.include_router(training_router, prefix=API_V1_PREFIX)
app.include_router(eval_router, prefix=API_V1_PREFIX)
