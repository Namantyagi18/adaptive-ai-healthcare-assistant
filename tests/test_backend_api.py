"""Unit and Integration tests for Backend Route Handlers, Auth, and Rate Limiting."""

import base64
import unittest
import tempfile
import gc
from pathlib import Path
from fastapi import HTTPException
from adapt_ai.config import settings
from adapt_ai.security.auth import verify_api_key
from adapt_ai.security.rate_limiter import rate_limiter
from adapt_ai.api.server import app
from adapt_ai.models.schemas import QuestionRequest, IngestionItem, IngestionRequest, TrainingJobConfig
from adapt_ai.api.routes.health import get_health, inspect_hardware, get_model_recommendation
from adapt_ai.api.routes.chat import ask_question, get_session_history, delete_session, get_qa_service
from adapt_ai.api.routes.rag import get_knowledge_base_stats, search_passages, ingest_guidelines, get_kb_manager, reindex_knowledge_base
from adapt_ai.api.routes.media import upload_document, DocumentUploadPayload
from adapt_ai.api.routes.training import preprocess_dataset, launch_training_job, compare_models
from adapt_ai.api.routes.eval_routes import run_evaluation, list_reports


class TestBackendAPI(unittest.TestCase):

    def setUp(self):
        self.orig_provider = settings.MODEL_PROVIDER
        self.orig_env = settings.APP_ENV
        self.orig_key = settings.API_KEY_SECRET
        self.orig_vector_dir = settings.VECTOR_INDEX_DIR
        self.temp_dir = tempfile.TemporaryDirectory()
        settings.VECTOR_INDEX_DIR = Path(self.temp_dir.name)
        settings.MODEL_PROVIDER = "mock_eval"
        settings.APP_ENV = "development"
        self.valid_key = settings.API_KEY_SECRET
        rate_limiter.clear()

    def tearDown(self):
        settings.MODEL_PROVIDER = self.orig_provider
        settings.APP_ENV = self.orig_env
        settings.API_KEY_SECRET = self.orig_key
        settings.VECTOR_INDEX_DIR = self.orig_vector_dir
        gc.collect()
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_auth_success(self):
        result = verify_api_key(api_key=self.valid_key)
        self.assertEqual(result, self.valid_key)

    def test_auth_success_with_whitespace(self):
        padded_key = f"  {self.valid_key}  \n"
        result = verify_api_key(api_key=padded_key)
        self.assertEqual(result, self.valid_key)

    def test_auth_missing_key_none(self):
        with self.assertRaises(HTTPException) as ctx:
            verify_api_key(api_key=None)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Missing required authentication header: 'X-API-Key'", ctx.exception.detail)
        self.assertEqual(ctx.exception.headers.get("WWW-Authenticate"), "ApiKey")

    def test_auth_missing_key_empty_string(self):
        with self.assertRaises(HTTPException) as ctx:
            verify_api_key(api_key="")
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Missing required authentication header: 'X-API-Key'", ctx.exception.detail)

    def test_auth_missing_key_whitespace_only(self):
        with self.assertRaises(HTTPException) as ctx:
            verify_api_key(api_key="   ")
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Missing required authentication header: 'X-API-Key'", ctx.exception.detail)

    def test_auth_incorrect_key_returns_401(self):
        with self.assertRaises(HTTPException) as ctx:
            verify_api_key(api_key="completely_wrong_key")
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Invalid or unauthorized API key", ctx.exception.detail)
        self.assertEqual(ctx.exception.headers.get("WWW-Authenticate"), "ApiKey")

    def test_auth_production_rejects_development_key(self):
        """Ensures that the default development API key cannot accidentally be used in production."""
        settings.APP_ENV = "production"
        settings.API_KEY_SECRET = "production-secure-enterprise-key-2026-xyz"
        dev_key = "adapt-ai-default-dev-secret-key-2026"

        # Attempt to authenticate with the dev key in production
        with self.assertRaises(HTTPException) as ctx:
            verify_api_key(api_key=dev_key)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Development API key is strictly prohibited in production", ctx.exception.detail)

    def test_auth_production_accepts_valid_production_key(self):
        """Ensures strong valid keys work seamlessly in production mode."""
        settings.APP_ENV = "production"
        prod_key = "production-secure-enterprise-key-2026-xyz"
        settings.API_KEY_SECRET = prod_key

        result = verify_api_key(api_key=prod_key)
        self.assertEqual(result, prod_key)

    def test_auth_production_rejects_misconfigured_server_with_dev_key(self):
        """Ensures production refuses to authenticate if server secret is still the dev key."""
        settings.APP_ENV = "production"
        settings.API_KEY_SECRET = "adapt-ai-default-dev-secret-key-2026"

        with self.assertRaises(HTTPException) as ctx:
            verify_api_key(api_key="adapt-ai-default-dev-secret-key-2026")
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("strictly prohibited", ctx.exception.detail)

    def test_openapi_swagger_security_spec(self):
        openapi_schema = app.openapi()
        
        # Verify ApiKeyAuth security scheme definition
        schemes = openapi_schema.get("components", {}).get("securitySchemes", {})
        self.assertIn("ApiKeyAuth", schemes)
        self.assertEqual(schemes["ApiKeyAuth"]["type"], "apiKey")
        self.assertEqual(schemes["ApiKeyAuth"]["in"], "header")
        self.assertEqual(schemes["ApiKeyAuth"]["name"], "X-API-Key")
        self.assertIn("ADAPT_AI_API_KEY", schemes["ApiKeyAuth"]["description"])

        # Verify secured endpoints require ApiKeyAuth
        chat_post = openapi_schema.get("paths", {}).get("/api/v1/chat/question", {}).get("post", {})
        self.assertIn("security", chat_post)
        self.assertEqual(chat_post["security"], [{"ApiKeyAuth": []}])

        # Verify public health probe has NO security requirement
        health_get = openapi_schema.get("paths", {}).get("/api/v1/health", {}).get("get", {})
        self.assertIsNone(health_get.get("security"))

    def test_health_routes(self):
        health = get_health()
        self.assertEqual(health["status"], "healthy")
        self.assertEqual(health["service"], settings.APP_NAME)

        hw = inspect_hardware()
        self.assertGreater(hw.cpu_count, 0)

        rec = get_model_recommendation()
        self.assertIsNotNone(rec.recommended_model)

    def test_chat_route_ask_and_history(self):
        service = get_qa_service()
        req = QuestionRequest(
            question="What are the symptoms of acute seasonal influenza?",
            session_id="route_test_session_1",
            include_citations=True
        )
        resp = ask_question(req=req, api_key=self.valid_key, service=service)
        self.assertIn("influenza", resp.answer.lower())
        self.assertEqual(resp.session_id, "route_test_session_1")

        # History
        history = get_session_history(session_id="route_test_session_1", api_key=self.valid_key)
        self.assertGreaterEqual(len(history), 2)

        # Clear session
        del_resp = delete_session(session_id="route_test_session_1", api_key=self.valid_key)
        self.assertEqual(del_resp["status"], "cleared")

    def test_rag_routes(self):
        stats = get_knowledge_base_stats(api_key=self.valid_key)
        self.assertIn("total_documents", stats)

        search_res = search_passages(q="hypertension", top_k=2, threshold=0.1, api_key=self.valid_key)
        self.assertIn("results_found", search_res)

        # Ingest new guideline
        new_doc = IngestionItem(
            title="AHA Heart Healthy Diet",
            source="AHA",
            category="Cardiovascular",
            content="A Mediterranean dietary pattern rich in unsaturated fats protects cardiovascular health."
        )
        ingest_req = IngestionRequest(documents=[new_doc])
        ingest_res = ingest_guidelines(req=ingest_req, api_key=self.valid_key, kb_mgr=get_kb_manager())
        self.assertEqual(ingest_res.status, "success")

        # Test re-index route
        reindex_res = reindex_knowledge_base(api_key=self.valid_key, kb_mgr=get_kb_manager())
        self.assertEqual(reindex_res["status"], "success")
        self.assertGreater(reindex_res["embedding_dimension"], 0)

    def test_media_upload_route(self):
        raw_text = b"Patient lab test: Blood sugar fasting 90 mg/dL, normal."
        b64_content = base64.b64encode(raw_text).decode("utf-8")
        payload = DocumentUploadPayload(
            filename="glucose_test.txt",
            content_base64=b64_content,
            prompt="Summarize fasting blood glucose"
        )
        res = upload_document(payload=payload, api_key=self.valid_key)
        self.assertEqual(res.extraction_status, "completed")
        self.assertIn("90 mg/dL", res.text_extracted)
        self.assertIn("CRITICAL MEDICAL NOTICE", res.safety_note)

    def test_training_routes(self):
        records = [
            {"question": "How to treat fever?", "answer": "Hydration and rest."},
            {"question": "How to treat fever?", "answer": "Hydration and rest."},  # duplicate
            {"question": "What is asthma?", "answer": "Chronic airway disease."}
        ]
        prep_res = preprocess_dataset(records=records, output_subdir="test_prep", api_key=self.valid_key)
        self.assertEqual(prep_res["status"], "success")
        self.assertEqual(prep_res["duplicates_removed"], 1)

        # Launch dry run
        job = TrainingJobConfig(
            dataset_path="./test.jsonl",
            output_model_dir="./data/test_job_out",
            dry_run=True
        )
        launch_res = launch_training_job(config=job, api_key=self.valid_key)
        self.assertEqual(launch_res["status"], "dry_run_validated")

        # Compare models
        comp_res = compare_models(
            baseline_predictions=["Mild fever."],
            finetuned_predictions=["Mild fever >= 38 C with rest."],
            ground_truths=["Fever is body temperature >= 38 C."],
            api_key=self.valid_key
        )
        self.assertEqual(comp_res["total_test_samples"], 1)

    def test_evaluation_routes(self):
        reports = list_reports(api_key=self.valid_key)
        self.assertIn("reports", reports)

    def test_rate_limiter_logic(self):
        client = "192.168.1.100"
        limiter = rate_limiter
        limiter.limit = 3
        limiter.burst = 0
        limiter.clear()

        # 3 calls permitted
        self.assertTrue(limiter.is_allowed(client)[0])
        self.assertTrue(limiter.is_allowed(client)[0])
        self.assertTrue(limiter.is_allowed(client)[0])
        
        # 4th call rejected
        allowed, remaining, retry_after = limiter.is_allowed(client)
        self.assertFalse(allowed)
        self.assertGreater(retry_after, 0.0)

        # Reset
        limiter.limit = settings.RATE_LIMIT_PER_MINUTE
        limiter.burst = settings.RATE_LIMIT_BURST
        limiter.clear()


if __name__ == "__main__":
    unittest.main()
