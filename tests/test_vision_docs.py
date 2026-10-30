"""Unit tests for Image and Document Processing Pipeline."""

import io
import unittest
from PIL import Image
from adapt_ai.vision_docs.validator import DocumentValidator
from adapt_ai.vision_docs.secure_storage import SecureStorage
from adapt_ai.vision_docs.extractor import DocumentVisionPipeline
from adapt_ai.adapters.mock_eval_adapter import MockEvalAdapter
from adapt_ai.models.exceptions import InvalidDocumentError


class TestVisionDocs(unittest.TestCase):

    def setUp(self):
        self.adapter = MockEvalAdapter()
        self.pipeline = DocumentVisionPipeline(self.adapter)

    def test_validator_valid_text(self):
        content = b"Patient lab report: Hemoglobin 14.2 g/dL, WBC 7,200 /mcL."
        ext, mime = DocumentValidator.validate_upload("report.txt", content)
        self.assertEqual(ext, ".txt")
        self.assertEqual(mime, "text/plain")

    def test_validator_valid_png_magic_bytes(self):
        # Generate genuine small PNG in memory
        img = Image.new("RGB", (64, 64), color="red")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        png_bytes = buf.getvalue()

        ext, mime = DocumentValidator.validate_upload("xray.png", png_bytes)
        self.assertEqual(ext, ".png")
        self.assertEqual(mime, "image/png")

    def test_validator_rejects_disallowed_extension(self):
        content = b"malicious binary payload"
        with self.assertRaises(InvalidDocumentError):
            DocumentValidator.validate_upload("script.exe", content)

    def test_validator_rejects_spoofed_magic_bytes(self):
        # File named .png but containing plain text
        spoofed = b"This is plain text pretending to be a png."
        with self.assertRaises(InvalidDocumentError):
            DocumentValidator.validate_upload("spoofed.png", spoofed)

    def test_validator_rejects_oversized_file(self):
        huge_bytes = b"0" * (11 * 1024 * 1024)  # 11 MB > 10 MB limit
        with self.assertRaises(InvalidDocumentError):
            DocumentValidator.validate_upload("huge.txt", huge_bytes)

    def test_secure_storage_quarantine(self):
        sample = b"Confidential clinical lab memo"
        file_id, sha256_hash, dest_path = SecureStorage.save_file("memo.txt", sample)
        self.assertTrue(dest_path.exists())
        self.assertEqual(len(sha256_hash), 64)
        self.assertTrue(file_id.startswith("med_"))

    def test_pipeline_text_document(self):
        sample = b"Blood glucose: 95 mg/dL (fasting). Total cholesterol: 180 mg/dL."
        resp = self.pipeline.process_file("lab_summary.txt", sample)
        self.assertEqual(resp.extraction_status, "completed")
        self.assertIn("Blood glucose: 95 mg/dL", resp.text_extracted)
        self.assertIn("CRITICAL MEDICAL NOTICE", resp.safety_note)

    def test_pipeline_image_processing_and_safety_disclaimer(self):
        img = Image.new("RGB", (32, 32), color="blue")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        png_bytes = buf.getvalue()

        resp = self.pipeline.process_file("derm_scan.png", png_bytes, user_prompt="Inspect rash")
        self.assertEqual(resp.image_metadata["width"], 32)
        self.assertEqual(resp.image_metadata["height"], 32)
        self.assertIn("Visual Inspection Engine", resp.clinical_interpretation)
        self.assertIn("CRITICAL MEDICAL NOTICE", resp.safety_note)
        self.assertIn("Under no circumstances should serious illnesses", resp.safety_note)


if __name__ == "__main__":
    unittest.main()
