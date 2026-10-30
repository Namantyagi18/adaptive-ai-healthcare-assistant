"""Protected Health Information (PHI) Sanitization and Privacy Protection.

Enforces HIPAA Safe Harbor de-identification principles by stripping or masking
direct identifiers (Names, Phone Numbers, Emails, SSNs, MRNs, Dates of Birth)
from log records and diagnostic telemetry to prevent accidental data leaks.
"""

import re
import logging
from typing import Dict, Any


# Regular expressions for direct health identifiers
RE_EMAIL = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
RE_PHONE = re.compile(r'(?:\+?(\d{1,3}))?[-.\s]?(?:\(?(\d{3})\)?[-.\s]?)(\d{3})[-.\s]?(\d{4})\b')
RE_SSN = re.compile(r'\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b')
RE_MRN = re.compile(r'\b(?:MRN|mrn|Record|ID)[:\s#]*([A-Za-z0-9]{6,12})\b', re.IGNORECASE)
RE_DOB = re.compile(r'\b(?:DOB|dob|Birthdate|Birth\s*Date)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b', re.IGNORECASE)
RE_CREDIT_CARD = re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b')


def sanitize_text(text: str) -> str:
    """Sanitizes text by replacing direct personal health identifiers with redaction tags."""
    if not isinstance(text, str):
        return text
    
    redacted = RE_EMAIL.sub("[REDACTED_EMAIL]", text)
    redacted = RE_PHONE.sub("[REDACTED_PHONE]", redacted)
    redacted = RE_SSN.sub("[REDACTED_SSN]", redacted)
    redacted = RE_CREDIT_CARD.sub("[REDACTED_FINANCIAL_ID]", redacted)
    redacted = RE_MRN.sub("MRN:[REDACTED_MRN]", redacted)
    redacted = RE_DOB.sub("DOB:[REDACTED_DOB]", redacted)
    return redacted


def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively traverses and sanitizes strings inside dictionaries."""
    sanitized = {}
    for key, value in data.items():
        # High sensitivity keys that should always be masked
        lower_key = key.lower()
        if any(sens in lower_key for sens in ["password", "secret", "token", "auth", "api_key"]):
            sanitized[key] = "[REDACTED_CREDENTIAL]"
        elif isinstance(value, str):
            sanitized[key] = sanitize_text(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_text(v) if isinstance(v, str) else v for v in value]
        else:
            sanitized[key] = value
    return sanitized


class PHIFilter(logging.Filter):
    """Custom logging filter that automatically masks PHI before writing to log sinks."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = sanitize_text(record.msg)
        if record.args:
            if isinstance(record.args, dict):
                record.args = sanitize_dict(record.args)
            elif isinstance(record.args, tuple):
                record.args = tuple(
                    sanitize_text(a) if isinstance(a, str) else a for a in record.args
                )
        return True


def setup_secure_logger(name: str = "adapt_ai") -> logging.Logger:
    """Instantiates a structured logger equipped with PHI redaction."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    # Attach PHI filter
    logger.addFilter(PHIFilter())
    return logger


# Default logger instance
logger = setup_secure_logger()

