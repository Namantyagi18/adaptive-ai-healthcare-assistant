"""Unit tests for Hardware Inspection, Dataset Preparation, and Training Pipeline."""

import unittest
import tempfile
from pathlib import Path
from adapt_ai.training.resource_inspector import ResourceInspector
from adapt_ai.training.model_recommender import ModelRecommender
from adapt_ai.training.dataset_preprocessor import DatasetPreprocessor
from adapt_ai.training.lora_trainer import LoRATrainer
from adapt_ai.training.evaluator import ModelEvaluator
from adapt_ai.models.schemas import TrainingJobConfig, HardwareResourceReport
from adapt_ai.models.exceptions import ResourceInsufficientError


class TestTrainingPipeline(unittest.TestCase):

    def test_resource_inspector(self):
        hardware = ResourceInspector.inspect()
        self.assertGreater(hardware.cpu_count, 0)
        self.assertIn(hardware.compute_tier, ["CPU_ONLY", "LOW_VRAM_GPU", "HIGH_VRAM_SERVER"])
        self.assertIn("full_parameter_finetune_8b", hardware.training_feasibility)

    def test_model_recommender_cpu_only(self):
        cpu_report = HardwareResourceReport(
            cpu_count=8,
            system_os="Windows 11",
            ram_total_gb=16.0,
            ram_available_gb=8.0,
            gpu_available=False,
            gpu_name=None,
            vram_total_gb=None,
            compute_tier="CPU_ONLY",
            training_feasibility={}
        )
        rec = ModelRecommender.recommend(cpu_report)
        self.assertIn("CPU-only system detected", rec.hardware_match)
        self.assertIn("Hosted Endpoint", rec.recommended_model)

    def test_dataset_preprocessor_deduplication(self):
        records = [
            {"question": "What is hypertension?", "answer": "High blood pressure."},
            {"question": "What is hypertension?", "answer": "High blood pressure."},  # Duplicate
            {"instruction": "Define asthma.", "output": "Chronic airway disease."}
        ]
        clean, dups = DatasetPreprocessor.validate_and_deduplicate(records)
        self.assertEqual(len(clean), 2)
        self.assertEqual(dups, 1)

    def test_dataset_preprocessor_split_and_leakage_prevention(self):
        records = [
            {"prompt": f"Medical query {i}", "response": f"Clinical explanation {i}", "category": "General"}
            for i in range(20)
        ]
        train, val, test = DatasetPreprocessor.split_dataset(records, train_ratio=0.8, val_ratio=0.1)
        self.assertEqual(len(train), 16)
        self.assertEqual(len(val), 2)
        self.assertEqual(len(test), 2)

        # Inject deliberate leak into training set
        train.append(test[0])
        self.assertEqual(len(train), 17)

        # Purge leak
        purged_train, leaks = DatasetPreprocessor.detect_and_prevent_leakage(train, test)
        self.assertEqual(leaks, 1)
        self.assertEqual(len(purged_train), 16)

    def test_lora_trainer_preflight_cpu_enforcement(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            job = TrainingJobConfig(
                dataset_path="./fake_data.jsonl",
                output_model_dir=tmpdir,
                dry_run=False  # Must fail if running on CPU
            )
            hardware = ResourceInspector.inspect()
            if hardware.compute_tier == "CPU_ONLY":
                with self.assertRaises(ResourceInsufficientError):
                    LoRATrainer.launch_job(job)

    def test_lora_trainer_dry_run_generates_artifacts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            job = TrainingJobConfig(
                dataset_path="./fake_data.jsonl",
                output_model_dir=tmpdir,
                dry_run=True  # Dry run should succeed and produce config & script
            )
            result = LoRATrainer.launch_job(job)
            self.assertEqual(result["status"], "dry_run_validated")
            self.assertTrue(Path(result["config_path"]).exists())
            self.assertTrue(Path(result["script_path"]).exists())

    def test_model_evaluator_comparative_metrics(self):
        baseline_preds = ["Fever is high temperature. Take pill."]
        finetuned_preds = ["Fever is temperature >= 38.0 C. Rest, hydrate, and consult a physician if persistent."]
        ground_truths = ["Fever is defined as body temperature >= 38.0 C requiring hydration, rest, and doctor evaluation."]

        comp = ModelEvaluator.compare_models(
            [ModelEvaluator.evaluate_pair(baseline_preds[0], ground_truths[0])],
            [ModelEvaluator.evaluate_pair(finetuned_preds[0], ground_truths[0])]
        )
        self.assertEqual(comp["total_test_samples"], 1)
        self.assertGreater(comp["finetuned_metrics"]["factual_grounding"], comp["baseline_metrics"]["factual_grounding"])


if __name__ == "__main__":
    unittest.main()

