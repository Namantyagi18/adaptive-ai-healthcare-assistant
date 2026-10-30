"""Pydantic schemas and clinical data models for ADAPT-AI."""

from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from pydantic import BaseModel, Field


class TriageLevel(str, Enum):
    """Clinical triage classification for guiding users to appropriate care."""
    EMERGENCY_IMMEDIATE = "EMERGENCY_IMMEDIATE"   # Red flags: Stroke, Myocardial Infarction, Severe Sepsis, Anaphylaxis
    URGENT_CARE = "URGENT_CARE"                   # Needs clinical assessment within 12-24 hours
    ROUTINE_CLINICAL = "ROUTINE_CLINICAL"         # Primary care appointment recommended
    SELF_CARE_EDUCATION = "SELF_CARE_EDUCATION"   # Educational context, general health literacy
    UNCERTAIN_AMBIGUOUS = "UNCERTAIN_AMBIGUOUS"   # Ambiguous symptoms requiring clarifying history


class EvidenceSufficiency(str, Enum):
    """Categorization of evidence sufficiency."""
    SUFFICIENT = "SUFFICIENT"
    INSUFFICIENT = "INSUFFICIENT"
    CONTRADICTORY = "CONTRADICTORY"


class EvidenceReference(BaseModel):
    """Represents a validated medical knowledge base citation."""
    doc_id: str = Field(..., description="Unique guideline or document identifier")
    title: str = Field(..., description="Document or guideline title")
    source: str = Field(..., description="Issuing body (e.g. WHO, CDC, NICE, NHS)")
    chunk_id: str = Field(..., description="Chunk ID for provenance tracking")
    relevance_score: float = Field(..., description="Cosine similarity score (0.0 to 1.0)")
    excerpt: str = Field(..., description="Relevant passage text excerpt")


class ChatRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    role: ChatRole = Field(..., description="Role of the speaker")
    content: str = Field(..., description="Message text content")


class QuestionRequest(BaseModel):
    """Request payload for medical QA."""
    question: str = Field(..., min_length=2, max_length=2000, description="User healthcare query")
    session_id: Optional[str] = Field(None, description="Optional conversation session ID for multi-turn history")
    include_citations: bool = Field(True, description="Whether to include guideline citations")
    language_hint: Optional[str] = Field("en", description="ISO 639-1 language code hint")
    country_code: Optional[str] = Field(None, description="Optional ISO 3166-1 alpha-2 country code (e.g. 'IN', 'US', 'GB')")


class QuestionResponse(BaseModel):
    """Comprehensive, clinically cautious healthcare QA response."""
    answer: str = Field(..., description="Synthesized medical explanation or guidance")
    triage_level: TriageLevel = Field(..., description="Triage urgency classification")
    is_emergency: bool = Field(False, description="Flag indicating urgent red flag warning signs")
    emergency_guidance: Optional[str] = Field(None, description="Immediate life-saving instructions (e.g. 911 / A&E)")
    citations: List[EvidenceReference] = Field(default_factory=list, description="Validated source references")
    evidence_sufficiency: EvidenceSufficiency = Field(..., description="Sufficiency of knowledge base evidence")
    uncertainty_statement: Optional[str] = Field(None, description="Clinical uncertainty or boundary statement")
    follow_up_questions: List[str] = Field(default_factory=list, description="Clarifying questions for missing history")
    session_id: str = Field(..., description="Conversation session ID")
    model_used: str = Field(..., description="Model identifier used for inference")
    latency_ms: float = Field(..., description="Processing time in milliseconds")
    safety_disclaimer: str = Field(
        default=(
            "ADAPT-AI is an informational clinical decision support and health education tool. "
            "It does not provide formal medical diagnoses or prescribe medications. "
            "Always consult a qualified healthcare professional for medical diagnosis and treatment decisions."
        ),
        description="Standard regulatory medical disclaimer"
    )


class IngestionItem(BaseModel):
    title: str = Field(..., description="Guideline or document title")
    source: str = Field(..., description="Authoritative issuing body")
    category: str = Field(..., description="Clinical specialty or topic")
    content: str = Field(..., description="Full text content")
    version: Optional[str] = Field("1.0", description="Document version")
    url: Optional[str] = Field(None, description="Canonical source URL")


class IngestionRequest(BaseModel):
    documents: List[IngestionItem] = Field(..., description="List of authoritative medical documents to index")


class IngestionResponse(BaseModel):
    status: str
    documents_indexed: int
    chunks_created: int
    duplicates_skipped: int
    total_vectors_in_store: int


class ImageUploadResponse(BaseModel):
    file_id: str
    original_filename: str
    content_type: str
    size_bytes: int
    sha256_hash: str
    quarantined_path: str
    image_metadata: Dict[str, Any]
    text_extracted: Optional[str] = None
    extraction_status: str
    clinical_interpretation: str
    safety_note: str


class HardwareResourceReport(BaseModel):
    cpu_count: int
    system_os: str
    ram_total_gb: float
    ram_available_gb: float
    gpu_available: bool
    gpu_name: Optional[str]
    vram_total_gb: Optional[float]
    compute_tier: str  # "CPU_ONLY", "LOW_VRAM_GPU", "HIGH_VRAM_SERVER"
    training_feasibility: Dict[str, Any]


class ModelRecommendation(BaseModel):
    recommended_model: str
    parameters_size: str
    recommended_quantization: str
    licence: str
    hardware_match: str
    medical_benchmark_scores: Dict[str, float]
    estimated_inference_cost: str
    training_method: str  # e.g., "QLoRA 4-bit" or "Hosted API fine-tuning"
    notes: str


class TrainingJobConfig(BaseModel):
    dataset_path: str
    base_model_name: str = "meta-llama/Meta-Llama-3-8B-Instruct"
    output_model_dir: str = "./models/adapt-ai-finetuned"
    peft_method: Literal["lora", "qlora"] = "qlora"
    lora_r: int = 16
    lora_alpha: int = 32
    batch_size: int = 2
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-4
    epochs: int = 3
    max_seq_length: int = 1024
    dry_run: bool = True

