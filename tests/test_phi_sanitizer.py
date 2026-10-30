"""Unit tests for PHI Sanitization and HIPAA Compliance."""

import unittest
import logging
from adapt_ai.security.phi_sanitizer import sanitize_text, sanitize_dict, PHIFilter, setup_secure_logger


class TestPHISanitizer(unittest.TestCase):

    def test_email_redaction(self):
        text = "Contact patient John Doe at john.doe@hospital.org regarding lab results."
        clean = sanitize_text(text)
        self.assertNotIn("john.doe@hospital.org", clean)
        self.assertIn("[REDACTED_EMAIL]", clean)

    def test_phone_number_redaction(self):
        text = "Patient phone is 555-123-4567 or +1 (800) 555-0199."
        clean = sanitize_text(text)
        self.assertNotIn("555-123-4567", clean)
        self.assertIn("[REDACTED_PHONE]", clean)

    def test_ssn_redaction(self):
        text = "Patient SSN is 123-45-6789 on the file."
        clean = sanitize_text(text)
        self.assertNotIn("123-45-6789", clean)
        self.assertIn("[REDACTED_SSN]", clean)

    def test_mrn_and_dob_redaction(self):
        text = "MRN: A12345678, DOB: 05/12/1985 reported chest pain."
        clean = sanitize_text(text)
        self.assertNotIn("A12345678", clean)
        self.assertNotIn("05/12/1985", clean)
        self.assertIn("MRN:[REDACTED_MRN]", clean)
        self.assertIn("DOB:[REDACTED_DOB]", clean)

    def test_dict_sanitization(self):
        payload = {
            "name": "Jane Doe",
            "email": "jane@clinic.org",
            "api_key": "secret-12345",
            "nested": {
                "phone": "555-888-9999"
            }
        }
        sanitized = sanitize_dict(payload)
        self.assertEqual(sanitized["api_key"], "[REDACTED_CREDENTIAL]")
        self.assertIn("[REDACTED_EMAIL]", sanitized["email"])
        self.assertIn("[REDACTED_PHONE]", sanitized["nested"]["phone"])

    def test_logging_filter(self):
        logger = setup_secure_logger("test_phi_logger")
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="User email test@domain.com submitted query.",
            args=(),
            exc_info=None
        )
        filt = PHIFilter()
        self.assertTrue(filt.filter(record))
        self.assertNotIn("test@domain.com", record.msg)
        self.assertIn("[REDACTED_EMAIL]", record.msg)


if __name__ == "__main__":
    unittest.main()

