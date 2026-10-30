"""Unit tests for Model Adapter Layer and Resilience Handlers."""

import unittest
from unittest.mock import MagicMock
from adapt_ai.adapters.mock_eval_adapter import MockEvalAdapter
from adapt_ai.adapters.retry_handler import execute_with_retry
from adapt_ai.adapters.factory import get_model_adapter
from adapt_ai.models.schemas import ChatMessage, ChatRole
from adapt_ai.models.exceptions import ProviderError


class TestModelAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = MockEvalAdapter(model_name="test-eval-model", embedding_dim=64)

    def test_mock_adapter_generate_with_context(self):
        messages = [
            ChatMessage(
                role=ChatRole.SYSTEM,
                content="RETRIEVED MEDICAL CONTEXT:\nFever is defined as temperature >= 38.0 C.\nUSER QUESTION:"
            ),
            ChatMessage(role=ChatRole.USER, content="What temperature is a fever?")
        ]
        resp = self.adapter.generate(messages)
        self.assertIn("Regarding your query", resp)
        self.assertIn("Fever is defined as temperature >= 38.0 C.", resp)

    def test_mock_adapter_generate_without_context(self):
        messages = [
            ChatMessage(role=ChatRole.USER, content="What is an alien symptom?")
        ]
        resp = self.adapter.generate(messages)
        self.assertIn("insufficient specific evidence", resp)

    def test_mock_adapter_embeddings(self):
        texts = ["Cardiovascular hypertension diagnosis", "Pediatric febrile seizure"]
        embeddings = self.adapter.embed(texts)
        self.assertEqual(len(embeddings), 2)
        self.assertEqual(len(embeddings[0]), 64)
        self.assertEqual(len(embeddings[1]), 64)

    def test_mock_adapter_vision(self):
        img_bytes = b"fake_png_binary_bytes"
        ans = self.adapter.analyze_vision(img_bytes, "image/png", "Check skin lesion")
        self.assertIn("Visual Inspection Engine", ans)
        self.assertIn("requires direct in-person clinical examination", ans)

    def test_retry_handler_success(self):
        counter = {"calls": 0}
        def flaky_func():
            counter["calls"] += 1
            if counter["calls"] < 2:
                raise ConnectionError("Temporary timeout")
            return "success_payload"

        result = execute_with_retry(flaky_func, max_retries=3, backoff_factor=1.1, provider_name="test-prov")
        self.assertEqual(result, "success_payload")
        self.assertEqual(counter["calls"], 2)

    def test_retry_handler_exhaustion_raises_provider_error(self):
        def permanent_failing_func():
            raise ConnectionError("Server completely unreachable")

        with self.assertRaises(ProviderError):
            execute_with_retry(permanent_failing_func, max_retries=2, backoff_factor=1.1, provider_name="failing-prov")

    def test_factory_fallback(self):
        adapter = get_model_adapter(override_provider="mock_eval")
        self.assertIsInstance(adapter, MockEvalAdapter)
        self.assertTrue(adapter.is_healthy())


if __name__ == "__main__":
    unittest.main()

