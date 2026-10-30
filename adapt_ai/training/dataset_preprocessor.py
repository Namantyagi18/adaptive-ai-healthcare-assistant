"""Medical Dataset Validation, Deduplication, Train/Val/Test Splitting, and Leakage Prevention."""

import json
import hashlib
import random
from pathlib import Path
from typing import List, Dict, Any, Tuple
from adapt_ai.security.phi_sanitizer import logger


class DatasetPreprocessor:
    """Prepares and validates medical instruction-tuning datasets."""

    @staticmethod
    def validate_and_deduplicate(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
        """Validates record schema and removes duplicate prompt-answer pairs.
        
        Returns:
            Tuple[List[Dict[str, Any]], int]: (clean_records, duplicates_removed_count)
        """
        seen_hashes = set()
        clean = []
        duplicates = 0

        for r in records:
            # Normalize schema: support {question, answer} or {instruction, input, output}
            prompt = r.get("question") or r.get("instruction", "")
            response = r.get("answer") or r.get("output", "")

            if not prompt or not response:
                continue

            normalized_key = f"{prompt.strip().lower()} ||| {response.strip().lower()}"
            content_hash = hashlib.sha256(normalized_key.encode("utf-8")).hexdigest()

            if content_hash in seen_hashes:
                duplicates += 1
                continue

            seen_hashes.add(content_hash)
            clean.append({
                "prompt": prompt.strip(),
                "response": response.strip(),
                "category": r.get("category", "General Clinical")
            })

        logger.info(f"Validated dataset: {len(clean)} valid records, {duplicates} duplicates removed.")
        return clean, duplicates

    @staticmethod
    def split_dataset(
        records: List[Dict[str, Any]],
        train_ratio: float = 0.8,
        val_ratio: float = 0.1,
        seed: int = 42
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Splits records into disjoint Train, Validation, and Held-out Test partitions."""
        shuffled = list(records)
        random.seed(seed)
        random.shuffle(shuffled)

        n = len(shuffled)
        train_end = int(n * train_ratio)
        val_end = train_end + int(n * val_ratio)

        train_data = shuffled[:train_end]
        val_data = shuffled[train_end:val_end]
        test_data = shuffled[val_end:]

        return train_data, val_data, test_data

    @staticmethod
    def detect_and_prevent_leakage(
        train_data: List[Dict[str, Any]],
        test_data: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Identifies and purges any test evaluation examples present in the training set.
        
        Guarantees strict evaluation integrity by preventing data leakage.
        """
        test_prompts = {r["prompt"].strip().lower() for r in test_data}
        purged_train = []
        leaks_detected = 0

        for record in train_data:
            if record["prompt"].strip().lower() in test_prompts:
                leaks_detected += 1
                logger.warning(f"Data leakage detected and prevented for prompt: '{record['prompt'][:50]}...'")
            else:
                purged_train.append(record)

        logger.info(f"Leakage check complete: {leaks_detected} potential leaks purged from training set.")
        return purged_train, leaks_detected

    @staticmethod
    def save_splits(
        train_data: List[Dict[str, Any]],
        val_data: List[Dict[str, Any]],
        test_data: List[Dict[str, Any]],
        output_dir: Path
    ) -> Dict[str, str]:
        """Exports partitions to JSONL format."""
        output_dir.mkdir(parents=True, exist_ok=True)
        paths = {
            "train": str(output_dir / "train.jsonl"),
            "val": str(output_dir / "val.jsonl"),
            "test": str(output_dir / "test.jsonl")
        }

        for split_name, dataset in [("train", train_data), ("val", val_data), ("test", test_data)]:
            filepath = paths[split_name]
            with open(filepath, "w", encoding="utf-8") as f:
                for item in dataset:
                    f.write(json.dumps(item) + "\n")

        return paths

