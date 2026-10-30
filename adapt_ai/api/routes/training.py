"""Training Pipeline and Preprocessing Endpoints."""

from typing import List, Dict, Any
from pathlib import Path
from fastapi import APIRouter, Depends, Security, HTTPException, Body
from adapt_ai.models.schemas import TrainingJobConfig
from adapt_ai.training.dataset_preprocessor import DatasetPreprocessor
from adapt_ai.training.lora_trainer import LoRATrainer
from adapt_ai.training.evaluator import ModelEvaluator
from adapt_ai.config import settings
from adapt_ai.security.auth import verify_api_key


router = APIRouter(prefix="/training", tags=["Training Pipeline"])


@router.post("/preprocess", summary="Validate, Deduplicate, Split Dataset, and Detect Leakage")
def preprocess_dataset(
    records: List[Dict[str, Any]] = Body(..., description="Raw instruction or QA dataset records"),
    output_subdir: str = Body("finetuning_dataset", description="Subfolder in data directory"),
    api_key: str = Security(verify_api_key)
):
    """Performs validation, deduplication, 80/10/10 train-val-test split, and strict leakage prevention."""
    if not records:
        raise HTTPException(status_code=400, detail="Empty dataset provided.")

    clean_records, duplicates_removed = DatasetPreprocessor.validate_and_deduplicate(records)
    train_data, val_data, test_data = DatasetPreprocessor.split_dataset(clean_records)
    purged_train, leaks_detected = DatasetPreprocessor.detect_and_prevent_leakage(train_data, test_data)

    out_dir = settings.DATA_DIR / output_subdir
    paths = DatasetPreprocessor.save_splits(purged_train, val_data, test_data, out_dir)

    return {
        "status": "success",
        "total_records_received": len(records),
        "valid_records": len(clean_records),
        "duplicates_removed": duplicates_removed,
        "evaluation_leaks_prevented": leaks_detected,
        "splits": {
            "train_count": len(purged_train),
            "val_count": len(val_data),
            "test_count": len(test_data),
        },
        "saved_paths": paths
    }


@router.post("/launch", summary="Pre-flight Hardware and Launch/Configure QLoRA Training")
def launch_training_job(
    config: TrainingJobConfig,
    api_key: str = Security(verify_api_key)
):
    """Pre-flights compute hardware, verifies VRAM/RAM requirements, and produces reproducible training configs."""
    try:
        return LoRATrainer.launch_job(config)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/evaluate-comparison", summary="Compare Pretrained Baseline vs Fine-Tuned Model")
def compare_models(
    baseline_predictions: List[str] = Body(..., description="List of baseline model predictions"),
    finetuned_predictions: List[str] = Body(..., description="List of fine-tuned model predictions"),
    ground_truths: List[str] = Body(..., description="List of gold standard reference answers"),
    api_key: str = Security(verify_api_key)
):
    """Computes comparative metrics: factual grounding, safety adherence, and abstention."""
    if not (len(baseline_predictions) == len(finetuned_predictions) == len(ground_truths)):
        raise HTTPException(status_code=400, detail="Input arrays must have identical length.")

    base_results = []
    fine_results = []

    for bp, fp, gt in zip(baseline_predictions, finetuned_predictions, ground_truths):
        base_results.append(ModelEvaluator.evaluate_pair(bp, gt))
        fine_results.append(ModelEvaluator.evaluate_pair(fp, gt))

    return ModelEvaluator.compare_models(base_results, fine_results)

