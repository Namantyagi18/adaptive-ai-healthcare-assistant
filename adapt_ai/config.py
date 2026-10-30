"""Configuration settings for ADAPT-AI Medical Healthcare System.

Reads parameters strictly from environment variables and provides validated defaults.
Secrets (such as API keys) are kept server-side and never exposed to clients.
"""

from typing import Optional, List
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseModel):
    """Central configuration validated through Pydantic."""
    
    # Environment & System
    APP_ENV: str = Field(default="development", description="Environment: development, staging, production")
    APP_NAME: str = Field(default="ADAPT-AI Healthcare Intelligence Platform", description="Application Name")
    VERSION: str = Field(default="1.0.0", description="System API Version")
    DEBUG: bool = Field(default=False, description="Debug mode flag")
    
    # Server & Security
    HOST: str = Field(default="0.0.0.0", description="Bind host")
    PORT: int = Field(default=8000, description="Bind port")
    API_KEY_SECRET: str = Field(
        default_factory=lambda: os.getenv("ADAPT_AI_API_KEY", "adapt-ai-default-dev-secret-key-2026"),
        description="Master API authentication key for backend API access"
    )
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173").split(",") if origin.strip()],
        description="Allowed CORS origins"
    )
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="Max client requests permitted per minute")
    RATE_LIMIT_BURST: int = Field(default=10, description="Burst allowance above steady rate")
    SANITIZE_LOG_PHI: bool = Field(default=True, description="Enforce automatic PHI redaction from all server logs")
    DEFAULT_COUNTRY: str = Field(
        default_factory=lambda: os.getenv("DEFAULT_COUNTRY", "IN").upper(),
        description="Default ISO 3166-1 alpha-2 country code for emergency triage and contact routing (e.g. 'IN', 'US', 'GB')"
    )
    
    # Model Adapter Configuration (Defaults to Google Gemini Hosted API)
    MODEL_PROVIDER: str = Field(
        default_factory=lambda: os.getenv("ADAPT_AI_MODEL_PROVIDER", "hosted").lower(),
        description="Provider: 'hosted', 'local', or 'mock_eval'"
    )
    HOSTED_PROVIDER_TYPE: str = Field(
        default_factory=lambda: os.getenv("HOSTED_PROVIDER_TYPE", "google").lower(),
        description="Type of hosted provider: 'google', 'openai', or 'openai-compatible'"
    )
    HOSTED_API_KEY: Optional[str] = Field(
        default_factory=lambda: (
            os.getenv("HOSTED_API_KEY")
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or None
        ),
        description="Server-side secret key for hosted LLM APIs (Google AI Studio or OpenAI)"
    )
    HOSTED_API_BASE: str = Field(
        default_factory=lambda: os.getenv(
            "HOSTED_API_BASE",
            "https://generativelanguage.googleapis.com/v1beta/openai"
        ),
        description="Base URL for hosted LLM endpoint"
    )
    HOSTED_MODEL_NAME: str = Field(
        default_factory=lambda: os.getenv("HOSTED_MODEL_NAME", "gemini-1.5-flash"),
        description="Hosted model identifier (e.g. gemini-1.5-flash, gemini-2.0-flash, gpt-4o-mini)"
    )
    HOSTED_EMBEDDING_MODEL: str = Field(
        default_factory=lambda: os.getenv("HOSTED_EMBEDDING_MODEL", "gemini-embedding-001"),
        description="Hosted model identifier for embeddings (e.g. gemini-embedding-001, text-embedding-3-small)"
    )

    @property
    def is_hosted_key_configured(self) -> bool:
        """Returns True if HOSTED_API_KEY is non-empty and not a placeholder."""
        if not self.HOSTED_API_KEY:
            return False
        clean = self.HOSTED_API_KEY.strip().lower()
        return clean not in ("", "your_gemini_api_key_here", "your_api_key_here", "placeholder", "<api_key>", "none")

    @property
    def is_production(self) -> bool:
        """Returns True if the application is executing in production mode."""
        return self.APP_ENV.strip().lower() in ("production", "prod")
    
    # Local Model Adapter Configuration (Fallback option)
    LOCAL_MODEL_ENDPOINT: str = Field(
        default_factory=lambda: os.getenv("LOCAL_MODEL_ENDPOINT", "http://localhost:11434/v1"),
        description="OpenAI-compatible local server URL (e.g. Ollama, vLLM, LMDeploy)"
    )
    LOCAL_MODEL_NAME: str = Field(
        default_factory=lambda: os.getenv("LOCAL_MODEL_NAME", "llama3.2:3b"),
        description="Local model identifier"
    )
    
    # Resilience & Timeouts
    REQUEST_TIMEOUT_SECONDS: float = Field(default=30.0, description="Upstream inference timeout in seconds")
    MAX_RETRIES: int = Field(default=3, description="Maximum retry attempts on transient failures")
    RETRY_BACKOFF_FACTOR: float = Field(default=1.5, description="Exponential backoff multiplier")
    
    # Storage & RAG Directories
    DATA_DIR: Path = Field(default=BASE_DIR / "data", description="Data storage root")
    UPLOADS_DIR: Path = Field(default=BASE_DIR / "data" / "secure_uploads", description="Directory for quarantined uploads")
    VECTOR_INDEX_DIR: Path = Field(default=BASE_DIR / "data" / "rag_index", description="Vector database storage directory")
    EVAL_REPORTS_DIR: Path = Field(default=BASE_DIR / "data" / "eval_reports", description="Evaluation benchmarks storage")
    
    # Upload Limits
    MAX_UPLOAD_SIZE_BYTES: int = Field(default=10 * 1024 * 1024, description="Max upload size (10 MB)")
    ALLOWED_UPLOAD_EXTENSIONS: List[str] = Field(
        default_factory=lambda: [".png", ".jpg", ".jpeg", ".webp", ".pdf", ".txt", ".json", ".csv"],
        description="Allowed file extensions for ingestion and analysis"
    )
    
    # RAG Engine Parameters
    RAG_TOP_K: int = Field(default=4, description="Number of passage chunks retrieved per query")
    RAG_SIMILARITY_THRESHOLD: float = Field(
        default_factory=lambda: float(os.getenv("RAG_SIMILARITY_THRESHOLD", "0.65")),
        description="Minimum similarity score required to claim relevance (dense cosine threshold >= 0.65)"
    )
    CONTRADICTION_DETECTION_THRESHOLD: float = Field(default=0.70, description="Divergence threshold indicating contradictory evidence")

    class Config:
        arbitrary_types_allowed = True


# Global singleton settings instance
settings = Settings()

# Ensure directories exist
for directory in [settings.DATA_DIR, settings.UPLOADS_DIR, settings.VECTOR_INDEX_DIR, settings.EVAL_REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
