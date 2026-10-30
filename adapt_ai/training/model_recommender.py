"""Pretrained Model Recommender based on License, Hardware, Medical Benchmarks, and Cost."""

from typing import Dict, Any
from adapt_ai.models.schemas import ModelRecommendation, HardwareResourceReport


class ModelRecommender:
    """Evaluates open-weight and hosted models for clinical applications."""

    @staticmethod
    def recommend(hardware: HardwareResourceReport) -> ModelRecommendation:
        """Determines optimal model strategy based on available hardware and clinical benchmarks."""
        if hardware.compute_tier == "HIGH_VRAM_SERVER":
            return ModelRecommendation(
                recommended_model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                parameters_size="8 Billion Parameters",
                recommended_quantization="bfloat16 or 8-bit bitsandbytes",
                licence="Llama 3.1 Community License (Permits commercial use up to 700M MAU)",
                hardware_match="High-VRAM GPU server detected (>=24GB VRAM). Optimal for QLoRA and full LoRA fine-tuning.",
                medical_benchmark_scores={
                    "MedQA_USMLE": 68.4,
                    "PubMedQA": 79.2,
                    "MMLU_Professional_Medicine": 73.1
                },
                estimated_inference_cost="$0.00 / token (Self-hosted on existing GPU cluster, ~$0.70/hr cloud GPU instance)",
                training_method="QLoRA 4-bit with rank 16 and target modules [q_proj, v_proj, k_proj, o_proj]",
                notes="Recommended for self-hosted environments requiring complete patient data isolation and on-premise governance."
            )
        elif hardware.compute_tier == "LOW_VRAM_GPU":
            return ModelRecommendation(
                recommended_model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                parameters_size="8 Billion Parameters",
                recommended_quantization="4-bit NF4 (bitsandbytes)",
                licence="Llama 3.1 Community License",
                hardware_match="Moderate VRAM GPU detected (8-16GB VRAM). Suitable for 4-bit quantized inference and small batch QLoRA.",
                medical_benchmark_scores={
                    "MedQA_USMLE": 68.4,
                    "PubMedQA": 79.2,
                    "MMLU_Professional_Medicine": 73.1
                },
                estimated_inference_cost="$0.00 / token (Local execution)",
                training_method="QLoRA 4-bit with gradient checkpointing and batch size 1",
                notes="Requires gradient accumulation to maintain effective batch size without triggering CUDA Out-of-Memory."
            )
        else:
            # CPU_ONLY detected
            return ModelRecommendation(
                recommended_model="Hosted Endpoint (e.g., GPT-4o-mini / Claude 3.5 Haiku / Gemini Flash) OR Cloud GPU QLoRA",
                parameters_size="Hosted Cloud Foundation Models / 8B open-weight on cloud",
                recommended_quantization="Provider-managed / 4-bit on cloud instance",
                licence="Commercial Cloud API Terms of Service (HIPAA BAA available from cloud vendors)",
                hardware_match="CPU-only system detected (0 dedicated GPUs). Local LLM training is NOT computationally feasible.",
                medical_benchmark_scores={
                    "MedQA_USMLE": 82.5,
                    "PubMedQA": 84.1,
                    "MMLU_Professional_Medicine": 87.2
                },
                estimated_inference_cost="~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens (hosted)",
                training_method="Hosted API Fine-Tuning or Rental of On-Demand Cloud GPU (e.g. Lambda Labs, RunPod A10G at ~$0.35/hr)",
                notes="Local machine is fully capable of running the RAG vector engine and document pipeline. Training large language models should be dispatched to cloud GPU instances."
            )

