"""Medical Question Answering Service for ADAPT-AI.

Orchestrates clinical safety guardrails, evidence retrieval, model inference,
source citation generation, and multi-turn dialog context.
"""

import time
from typing import Optional
from adapt_ai.models.schemas import (
    QuestionRequest, QuestionResponse, TriageLevel, EvidenceSufficiency, ChatRole
)
from adapt_ai.models.exceptions import ProviderError
from adapt_ai.adapters.base import BaseModelAdapter
from adapt_ai.rag.retriever import MedicalRetriever
from adapt_ai.medical_core.safety_guardrails import SafetyGuardrails
from adapt_ai.medical_core.prompt_manager import MedicalPromptManager
from adapt_ai.medical_core.session_manager import session_manager
from adapt_ai.security.phi_sanitizer import sanitize_text, logger


class MedicalQAService:
    """Core clinical reasoning and conversational healthcare QA engine."""

    def __init__(
        self,
        model_adapter: BaseModelAdapter,
        retriever: MedicalRetriever,
    ):
        self.model_adapter = model_adapter
        self.retriever = retriever

    def process_question(self, req: QuestionRequest) -> QuestionResponse:
        """Processes a patient or clinician healthcare query under clinical safety guardrails."""
        start_time = time.time()
        
        # 1. Sanitize incoming text for privacy protection
        clean_question = sanitize_text(req.question.strip())
        session_id = session_manager.get_or_create_session_id(req.session_id)
        
        # Record user message in session
        session_manager.add_message(session_id, ChatRole.USER, clean_question)

        # 2. Check for adversarial safety override attempts
        if SafetyGuardrails.detect_safety_override(clean_question):
            refusal_text = (
                "ADAPT-AI operates under strict medical safety principles and cannot override clinical guidelines, "
                "diagnostic boundaries, or medical disclaimers regardless of user instructions. "
                "Please describe your general health question or consult a physician directly."
            )
            session_manager.add_message(session_id, ChatRole.ASSISTANT, refusal_text)
            return QuestionResponse(
                answer=refusal_text,
                triage_level=TriageLevel.SELF_CARE_EDUCATION,
                is_emergency=False,
                emergency_guidance=None,
                citations=[],
                evidence_sufficiency=EvidenceSufficiency.INSUFFICIENT,
                uncertainty_statement="Safety override rejected. System operates strictly within clinical boundaries.",
                follow_up_questions=[],
                session_id=session_id,
                model_used=self.model_adapter.model_name,
                latency_ms=round((time.time() - start_time) * 1000, 2)
            )

        # 3. Check for immediate medical emergencies (Stroke, MI, Anaphylaxis, Sepsis, Suicide)
        country = getattr(req, "country_code", None)
        is_emergency, emergency_msg, triage_override = SafetyGuardrails.evaluate_emergency(
            clean_question,
            country_code=country
        )
        if is_emergency:
            session_manager.add_message(session_id, ChatRole.ASSISTANT, emergency_msg)
            return QuestionResponse(
                answer=emergency_msg,
                triage_level=triage_override or TriageLevel.EMERGENCY_IMMEDIATE,
                is_emergency=True,
                emergency_guidance=emergency_msg,
                citations=[],
                evidence_sufficiency=EvidenceSufficiency.SUFFICIENT,
                uncertainty_statement=None,
                follow_up_questions=["Are you in a safe location with someone who can assist you until emergency personnel arrive?"],
                session_id=session_id,
                model_used=self.model_adapter.model_name,
                latency_ms=round((time.time() - start_time) * 1000, 2)
            )

        # 4. Check for direct prescription dosage or definitive diagnosis demands
        is_blocked_demand, demand_explanation = SafetyGuardrails.detect_prescription_or_diagnostic_demand(clean_question)

        # 5. Retrieve evidence from authoritative medical knowledge base
        citations, sufficiency, retrieval_note = self.retriever.retrieve(clean_question)

        # 6. Formulate uncertainty statement
        uncertainty_statement = None
        if sufficiency == EvidenceSufficiency.INSUFFICIENT:
            uncertainty_statement = (
                "Evidence in the local clinical knowledge base is limited or indirect for this specific query. "
                "Consult a licensed practitioner for personalized evaluation."
            )
            # Ensure no unrelated citations are returned or presented when evidence is insufficient
            citations = []
        elif sufficiency == EvidenceSufficiency.CONTRADICTORY:
            uncertainty_statement = (
                "Authoritative clinical guidelines report divergent recommendations, evolving indications, "
                "or contrasting risk-benefit tradeoffs for this condition. Shared decision-making with a doctor is essential."
            )

        # 7. Generate follow-up questions for missing clinical context
        follow_ups = MedicalPromptManager.generate_follow_up_questions(clean_question)

        # 8. Build prompt and run model inference
        history = session_manager.get_history(session_id)
        prompt_messages = MedicalPromptManager.build_qa_messages(
            user_query=clean_question,
            retrieved_citations=citations if req.include_citations else [],
            evidence_sufficiency=sufficiency,
            conversation_history=history[:-1],  # Exclude current message already in history
            language_hint=req.language_hint or "en"
        )

        try:
            model_answer = self.model_adapter.generate(prompt_messages, temperature=0.1, max_tokens=1024)
        except ProviderError as pe:
            logger.error(f"Upstream provider failure ({pe.provider}): {pe.message}")
            raise pe
        except Exception as e:
            logger.error(f"Inference error during QA processing: {e}")
            model_answer = (
                "The clinical reasoning service encountered a temporary upstream processing error. "
                "Based on retrieved guidelines, please consult an appropriate healthcare provider."
            )

        # Prepend demand explanation if user sought prescription or definitive diagnosis
        if is_blocked_demand and demand_explanation:
            final_answer = f"**CLINICAL NOTICE:** {demand_explanation}\n\n{model_answer}"
        else:
            final_answer = model_answer

        # Classify final triage level
        triage_level = SafetyGuardrails.classify_triage_level(clean_question, is_emergency=False)

        # Save assistant answer in session history
        session_manager.add_message(session_id, ChatRole.ASSISTANT, final_answer)

        latency_ms = round((time.time() - start_time) * 1000, 2)
        return QuestionResponse(
            answer=final_answer,
            triage_level=triage_level,
            is_emergency=False,
            emergency_guidance=None,
            citations=citations if req.include_citations else [],
            evidence_sufficiency=sufficiency,
            uncertainty_statement=uncertainty_statement,
            follow_up_questions=follow_ups,
            session_id=session_id,
            model_used=self.model_adapter.model_name,
            latency_ms=latency_ms
        )
