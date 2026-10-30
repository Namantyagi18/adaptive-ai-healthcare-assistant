"""Validation and integrity verification for medical image and document uploads."""

import os
from typing import Tuple
from pathlib import Path
from adapt_ai.config import settings
from adapt_ai.models.exceptions import InvalidDocumentError


# Magic byte signatures for authorized file formats
MAGIC_BYTES = {
    b"\x89PNG\r\n\x1a\n": "image/png",
    b"\xff\xd8\xff": "image/jpeg",
    b"RIFF": "image/webp",  # WebP container
    b"%PDF": "application/pdf",
}


class DocumentValidator:
    """Performs strict MIME and byte checks to prevent malicious file uploads."""

    @classmethod
    def validate_upload(cls, filename: str, file_bytes: bytes) -> Tuple[str, str]:
        """Validates file extension, payload size, and binary magic bytes.
        
        Returns:
            Tuple[str, str]: (sanitized_extension, detected_mime_type)
        """
        # 1. Size verification
        size = len(file_bytes)
        if size == 0:
            raise InvalidDocumentError("Uploaded file is empty (0 bytes).")
        if size > settings.MAX_UPLOAD_SIZE_BYTES:
            max_mb = settings.MAX_UPLOAD_SIZE_BYTES / (1024 * 1024)
            raise InvalidDocumentError(f"File size exceeds maximum allowed limit of {max_mb:.1f} MB.")

        # 2. Extension verification
        ext = Path(filename).suffix.lower()
        if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
            allowed = ", ".join(settings.ALLOWED_UPLOAD_EXTENSIONS)
            raise InvalidDocumentError(f"Extension '{ext}' is not permitted. Allowed: {allowed}")

        # 3. Magic byte check for binary formats
        detected_mime = "application/octet-stream"
        if ext in [".png", ".jpg", ".jpeg", ".webp", ".pdf"]:
            matched = False
            for magic, mime in MAGIC_BYTES.items():
                if file_bytes.startswith(magic):
                    detected_mime = mime
                    matched = True
                    break
            if not matched:
                raise InvalidDocumentError(f"Binary header does not match expected format for extension '{ext}'.")
        elif ext in [".txt", ".json", ".csv"]:
            try:
                file_bytes.decode("utf-8")
                detected_mime = "text/plain"
            except UnicodeDecodeError:
                raise InvalidDocumentError(f"Text file is not valid UTF-8 encoded text.")

        return ext, detected_mime

