# ADAPT-AI: Advanced Modular Healthcare Intelligence Platform

ADAPT-AI is a comprehensive, clinically governed healthcare question-answering, diagnostic document analysis, and medical information-access system. It provides evidence-grounded health discussions, cautious medical document/image interpretation, and safety-first clinical guidance.

---

## Important Clinical & Regulatory Notice

> **CLINICAL BOUNDARIES & ETHICAL DISCLAIMER:**
> 1. **No Automatic Diagnosis:** ADAPT-AI does not diagnose diseases or conditions from self-reported symptoms alone. Definitive diagnosis requires in-person medical evaluation, physical exam, and laboratory/imaging workup.
> 2. **No Medication Prescriptions:** ADAPT-AI does not prescribe pharmaceuticals, recommend personalized medication dosages, or override physician orders.
> 3. **Honest Capability Reporting:** We do not claim a model has been trained when it has not. Local fine-tuning requires dedicated GPU compute (16GB+ VRAM for QLoRA). The system currently provides reproducible training configurations and dry-run validation scripts.
> 4. **Emergency Red Flags:** Time-critical emergencies (Stroke FAST signs, acute chest pain/MI, anaphylaxis, severe sepsis, self-harm crisis) trigger immediate urgent-care guidance (911/999/112/988).

---

## Architectural Components

```
adapt_ai/
├── config.py                 # Central configuration via Pydantic & environment variables
├── security/
│   ├── auth.py               # Server-side API key authentication and access control
│   ├── rate_limiter.py       # Sliding-window rate limiter with burst tolerance
│   └── phi_sanitizer.py      # HIPAA-compliant Protected Health Information (PHI) log sanitizer
├── models/
│   ├── schemas.py            # Pydantic data schemas, triage levels, and evidence models
│   └── exceptions.py         # Standardized domain exceptions
├── adapters/
│   ├── base.py               # Provider-independent model interface (generate, embed, vision)
│   ├── hosted_adapter.py     # Hosted provider adapter (OpenAI / Anthropic / Gemini / vLLM)
│   ├── local_adapter.py      # Local open-weight model adapter (Ollama, vLLM, LMDeploy)
│   ├── mock_eval_adapter.py  # Deterministic offline evaluation & testing adapter
│   ├── retry_handler.py      # Exponential backoff and resilience handler
│   └── factory.py            # Adapter factory with graceful fallbacks
├── rag/
│   ├── document_parser.py    # Text & metadata extraction with SHA-256 deduplication
│   ├── chunker.py            # Sentence-boundary aware sliding window chunker
│   ├── embeddings.py         # Normalized dense subword/n-gram embedding generator
│   ├── vector_store.py       # SQLite & NumPy vector database with cosine similarity search
│   ├── retriever.py          # Top-K passage retrieval and contradiction detection
│   └── knowledge_base/       # Curated guideline corpus (WHO, CDC, NICE, USPSTF, ACC/AHA, ADA)
├── medical_core/
│   ├── safety_guardrails.py  # Emergency detection, non-prescriptive rules, jailbreak protection
│   ├── prompt_manager.py     # Evidence injection, uncertainty articulation, follow-up query engine
│   ├── session_manager.py    # Thread-safe multi-turn conversation history
│   └── qa_service.py         # Medical QA orchestrator
├── vision_docs/
│   ├── validator.py          # MIME type and binary magic-byte validator
│   ├── secure_storage.py     # SHA-256 hashed quarantined media storage
│   └── extractor.py          # Document text extraction vs cautious clinical interpretation
├── training/
│   ├── resource_inspector.py # Hardware & compute checker (GPU, VRAM, CPU, RAM)
│   ├── model_recommender.py  # Objective model recommender (license, VRAM, MedQA benchmarks)
│   ├── dataset_preprocessor.py # Dataset validation, deduplication, 80/10/10 split, leakage detector
│   ├── lora_trainer.py       # Hardware-gated PEFT/QLoRA config generator & training script
│   └── evaluator.py          # Baseline vs fine-tuned comparative evaluation metrics
├── evaluation/
│   ├── benchmark_suite.py    # Versioned 12-category clinical test suite
│   ├── metrics.py            # Relevance, safety, citation, and abstention scoring engine
│   └── run_evals.py          # Automated benchmark runner and report generator
└── api/
    ├── server.py             # FastAPI backend with pure ASGI middlewares and CORS
    └── routes/               # Modular endpoints: health, chat, rag, media, training, eval
```

---

## 12 Clinical Evaluation Categories

The system includes a versioned clinical benchmark suite covering:
1. **Common symptoms** (fever triage, acute bronchitis vs antibiotics)
2. **Infectious diseases** (influenza antiviral timing, tuberculosis symptoms)
3. **Cancer-related questions** (USPSTF colorectal screening, red-flag cancer signs)
4. **Blood disorders** (iron-deficiency anemia workup, ferritin interpretation)
5. **Cardiovascular & respiratory** (hypertension stages, GINA asthma safety principles)
6. **Diabetes & chronic conditions** (ADA diagnostic thresholds, HbA1c targets)
7. **Children's & women's health** (simple febrile seizures, preeclampsia severe features)
8. **Medical terminology & report explanations** (CBC leukocytosis, anemia, ALT/AST)
9. **Multilingual questions** (Spanish, French, and Hindi emergency and health terms)
10. **Emergency scenarios** (FAST stroke protocol, anaphylaxis, crushing chest pain)
11. **Ambiguous questions** (unexplained dizziness, non-specific fatigue history gathering)
12. **Questions lacking sufficient evidence** (unproven diabetes cures, unverified tea recipes)

---

## Quickstart & Installation

### Requirements
- Python 3.10+
- Installed packages: `fastapi`, `uvicorn`, `pydantic`, `numpy`, `pillow`, `requests`, `pyyaml`

### 1. Configure Environment
```bash
cp .env.example .env
```
Configure your `HOSTED_API_KEY` in `.env` (e.g. Google Gemini API key from Google AI Studio).

### 2. Run Test Suite
```bash
python -m unittest discover -s tests
```
*Current test suite: 115 unit tests passing across all modules (zero paid API calls).*

### 3. Run Clinical Evaluation Suite
```bash
# Offline benchmark verification using mock eval adapter:
python -m adapt_ai.evaluation.run_evals --adapter mock_eval

# Live benchmark against configured hosted provider (requires HOSTED_API_KEY):
python -m adapt_ai.evaluation.run_evals
```

### 4. Start the Backend API Server
```bash
python run_server.py
```
Interactive Swagger UI will be live at `http://localhost:8000/docs`.

---

## Backend Authentication & Swagger UI Guide

ADAPT-AI enforces role-separated API authentication:

| Key Variable | Purpose | Location | Header / Scheme |
|---|---|---|---|
| `ADAPT_AI_API_KEY` | Client access key to call ADAPT-AI endpoints | `.env` on backend, client request header | `X-API-Key: <key>` |
| `HOSTED_API_KEY` | Upstream LLM key to call Google Gemini | Server-side `.env` only (never shared) | `Authorization: Bearer <key>` |

### How to Authenticate in Swagger UI (`http://localhost:8000/docs`):
1. Open `http://localhost:8000/docs` in your browser.
2. Click the green **Authorize** button (padlock icon) at the top-right of the page.
3. In the **ApiKeyAuth** modal, enter your `ADAPT_AI_API_KEY` value:
   - For local development, use the pre-configured dev key: `adapt-ai-default-dev-secret-key-2026` (or the custom key you set in `.env`).
4. Click **Authorize**, then click **Close**.
5. The lock icons will now show as closed/locked. All subsequent **Try it out** requests (e.g. `POST /api/v1/chat/question`) will automatically include the required `X-API-Key` header.
6. Swagger UI preserves your authorized session in browser storage across page refreshes.

### How to Authenticate via cURL / HTTP Requests:
```bash
curl -X POST "http://localhost:8000/api/v1/chat/question" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: adapt-ai-default-dev-secret-key-2026" \
     -d '{"question": "What are the lifestyle interventions for hypertension?", "include_citations": true}'
```

*Note: Public telemetry endpoints (`GET /api/v1/health`, `GET /api/v1/health/resources`) do not require authentication.*

---

## Hardware Assessment & Training Feasibility

- **Local Machine Compute:** 8 CPU cores, 16GB RAM, 0 dedicated NVIDIA GPUs.
- **Feasibility:**
  - Local RAG retrieval & vector search: **Fully Functional** (NumPy vector engine).
  - Local Document & Vision processing: **Fully Functional** (Pillow & text parsers).
  - Local LLM Inference: **Functional** via local Ollama/vLLM daemon or hosted API.
  - Local QLoRA/LoRA 8B Training: **Not Feasible on CPU alone**. Pre-flight check prevents system out-of-memory crashes and generates reproducible configs (`train_qlora.py` and `qlora_config.yaml`) for cloud GPU nodes (RTX 4090 / A10G / A100).
