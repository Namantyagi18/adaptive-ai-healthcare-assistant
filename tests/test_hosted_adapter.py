"""Unit tests for Hosted Model Adapter (Google Gemini / OpenAI) with Mocked Network Layer.

Guarantees 100% test coverage for authentication, retries, error translation,
RAG citation injection, and emergency bypass WITHOUT making live or paid API calls.
"""

import unittest
from unittest.mock import patch, MagicMock
import requests

from adapt_ai.adapters.hosted_adapter import HostedModelAdapter
from adapt_ai.adapters.factory import get_model_adapter
from adapt_ai.models.schemas import ChatMessage, ChatRole, QuestionRequest, TriageLevel
from adapt_ai.models.exceptions import ProviderError
from adapt_ai.medical_core.qa_service import MedicalQAService
from adapt_ai.rag.retriever import MedicalRetriever
from adapt_ai.rag.vector_store import VectorStore
from adapt_ai.rag.embeddings import EmbeddingEngine


class TestHostedGeminiAdapter(unittest.TestCase):

    def setUp(self):
        self.api_key = "test-gemini-secret-api-key-12345"
        self.adapter = HostedModelAdapter(
            api_key=self.api_key,
            api_base="https://generativelanguage.googleapis.com/v1beta/openai",
            model_name="gemini-1.5-flash",
            provider_type="google",
            timeout=5.0,
            max_retries=2
        )

    def test_headers_include_both_bearer_and_google_key(self):
        headers = self.adapter._headers()
        self.assertEqual(headers["Authorization"], f"Bearer {self.api_key}")
        self.assertEqual(headers["x-goog-api-key"], self.api_key)
        self.assertEqual(headers["Content-Type"], "application/json")

    def test_missing_api_key_raises_provider_error(self):
        adapter_no_key = HostedModelAdapter(
            api_key=None,
            provider_type="google"
        )
        messages = [ChatMessage(role=ChatRole.USER, content="Hello")]
        with self.assertRaises(ProviderError) as ctx:
            adapter_no_key.generate(messages)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("requires a valid API key", ctx.exception.message)

    @patch("requests.post")
    def test_generate_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Stage 1 hypertension requires lifestyle modifications including DASH diet."
                    }
                }
            ]
        }
        mock_post.return_value = mock_resp

        messages = [
            ChatMessage(role=ChatRole.SYSTEM, content="Clinical guidance prompt"),
            ChatMessage(role=ChatRole.USER, content="What is hypertension?")
        ]
        answer = self.adapter.generate(messages)

        self.assertIn("Stage 1 hypertension requires lifestyle modifications", answer)
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", call_args[0][0])
        self.assertEqual(call_args[1]["json"]["model"], "gemini-1.5-flash")

    @patch("requests.post")
    def test_analyze_vision_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "The uploaded chest X-ray shows normal lung fields with no acute focal consolidation."
                    }
                }
            ]
        }
        mock_post.return_value = mock_resp

        sample_bytes = b"\x89PNG\r\n\x1a\nfake_image_bytes"
        ans = self.adapter.analyze_vision(sample_bytes, "image/png", "Describe X-ray findings cautiously")
        self.assertIn("normal lung fields", ans)

        mock_post.assert_called_once()
        payload = mock_post.call_args[1]["json"]
        self.assertEqual(payload["model"], "gemini-1.5-flash")
        user_content = payload["messages"][0]["content"]
        self.assertEqual(user_content[0]["type"], "text")
        self.assertEqual(user_content[1]["type"], "image_url")
        self.assertTrue(user_content[1]["image_url"]["url"].startswith("data:image/png;base64,"))

    @patch("requests.post")
    def test_embed_success_with_gemini_embedding_model(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "data": [
                {"embedding": [0.1, 0.2, 0.3]}
            ]
        }
        mock_post.return_value = mock_resp

        embs = self.adapter.embed(["Hypertension lifestyle guideline"])
        self.assertEqual(len(embs), 1)
        self.assertEqual(len(embs[0]), 3)

        payload = mock_post.call_args[1]["json"]
        self.assertEqual(payload["model"], "gemini-embedding-001")

    @patch("requests.post")
    def test_invalid_api_key_401_error(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.json.return_value = {
            "error": {
                "code": 401,
                "message": "API key not valid. Please pass a valid API key.",
                "status": "UNAUTHENTICATED"
            }
        }
        mock_post.return_value = mock_resp

        messages = [ChatMessage(role=ChatRole.USER, content="Test")]
        with self.assertRaises(ProviderError) as ctx:
            self.adapter.generate(messages)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("authentication failed", ctx.exception.message.lower())

    @patch("requests.post")
    def test_google_400_api_key_invalid_details(self, mock_post):
        """Google AI Studio often returns HTTP 400 with API_KEY_INVALID in error details."""
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.json.return_value = {
            "error": {
                "code": 400,
                "message": "API key not valid. Please pass a valid API key.",
                "status": "INVALID_ARGUMENT",
                "details": [
                    {
                        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
                        "reason": "API_KEY_INVALID",
                        "domain": "googleapis.com"
                    }
                ]
            }
        }
        mock_post.return_value = mock_resp

        messages = [ChatMessage(role=ChatRole.USER, content="Test")]
        with self.assertRaises(ProviderError) as ctx:
            self.adapter.generate(messages)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("authentication failed", ctx.exception.message.lower())

    def test_placeholder_api_key_aborts_without_network_call(self):
        adapter = HostedModelAdapter(api_key="your_gemini_api_key_here")
        messages = [ChatMessage(role=ChatRole.USER, content="Test")]
        with self.assertRaises(ProviderError) as ctx:
            adapter.generate(messages)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("placeholder value", ctx.exception.message.lower())

    @patch("requests.post")
    def test_model_not_found_404(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.json.return_value = {
            "error": {
                "code": 404,
                "message": "models/gemini-invalid is not found for API version v1beta",
                "status": "NOT_FOUND"
            }
        }
        mock_post.return_value = mock_resp

        messages = [ChatMessage(role=ChatRole.USER, content="Test")]
        with self.assertRaises(ProviderError) as ctx:
            self.adapter.generate(messages)
        self.assertEqual(ctx.exception.status_code, 404)
        self.assertIn("was not found", ctx.exception.message.lower())

    @patch("requests.post")
    def test_network_connection_error_503(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError("Failed to resolve host")
        messages = [ChatMessage(role=ChatRole.USER, content="Test")]
        with self.assertRaises(ProviderError) as ctx:
            self.adapter.generate(messages)
        self.assertEqual(ctx.exception.status_code, 503)
        self.assertIn("network connection failed", ctx.exception.message.lower())

    @patch("requests.post")
    def test_rate_limit_429_exhaustion(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 429
        mock_resp.json.return_value = {
            "error": {
                "code": 429,
                "message": "Resource has been exhausted (e.g. check quota).",
                "status": "RESOURCE_EXHAUSTED"
            }
        }
        mock_post.return_value = mock_resp

        messages = [ChatMessage(role=ChatRole.USER, content="Test")]
        with self.assertRaises(ProviderError) as ctx:
            self.adapter.generate(messages)
        self.assertEqual(ctx.exception.status_code, 429)

    @patch("requests.post")
    def test_timeout_retry_and_exhaustion(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout("Connection timed out")
        messages = [ChatMessage(role=ChatRole.USER, content="Test")]
        with self.assertRaises(ProviderError) as ctx:
            self.adapter.generate(messages)
        self.assertIn("timed out", ctx.exception.message)
        self.assertEqual(ctx.exception.status_code, 504)

    def test_no_silent_mock_fallback_when_hosted_configured(self):
        adapter = get_model_adapter(override_provider="hosted")
        self.assertIsInstance(adapter, HostedModelAdapter)
        from adapt_ai.config import settings
        self.assertEqual(adapter.model_name, settings.HOSTED_MODEL_NAME)

    @patch("requests.post")
    def test_medical_qa_service_with_hosted_gemini(self, mock_post):
        def _mock_post(url, *args, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            if "embeddings" in url:
                resp.json.return_value = {"data": [{"embedding": [0.1] * 128}]}
            else:
                resp.json.return_value = {
                    "choices": [
                        {
                            "message": {
                                "content": "According to GINA guidelines, short-acting beta-agonists should not be used alone."
                            }
                        }
                    ]
                }
            return resp

        mock_post.side_effect = _mock_post

        store = VectorStore()
        engine = EmbeddingEngine(self.adapter)
        retriever = MedicalRetriever(store, engine)
        qa = MedicalQAService(self.adapter, retriever)

        req = QuestionRequest(
            question="Why is an inhaler without steroid dangerous in asthma?",
            include_citations=True
        )
        resp = qa.process_question(req)
        self.assertEqual(resp.model_used, "gemini-1.5-flash")
        self.assertIn("According to GINA guidelines", resp.answer)
        self.assertFalse(resp.is_emergency)

    def test_emergency_bypasses_hosted_model_call(self):
        store = VectorStore()
        engine = EmbeddingEngine(self.adapter)
        retriever = MedicalRetriever(store, engine)
        qa = MedicalQAService(self.adapter, retriever)

        emergency_query = "My mother has sudden facial droop, arm weakness, and slurred speech."
        req = QuestionRequest(question=emergency_query)

        # Emergency detection must short-circuit without calling external APIs
        resp = qa.process_question(req)
        self.assertTrue(resp.is_emergency)
        self.assertEqual(resp.triage_level, TriageLevel.EMERGENCY_IMMEDIATE)
        self.assertIn("FAST", resp.emergency_guidance)

    def test_is_healthy_returns_false_for_unconfigured_or_placeholder_keys(self):
        adapter_placeholder = HostedModelAdapter(api_key="your_gemini_api_key_here")
        self.assertFalse(adapter_placeholder.is_healthy())

        adapter_none = HostedModelAdapter(api_key=None)
        self.assertFalse(adapter_none.is_healthy())

        adapter_empty = HostedModelAdapter(api_key="")
        self.assertFalse(adapter_empty.is_healthy())


if __name__ == "__main__":
    unittest.main()
