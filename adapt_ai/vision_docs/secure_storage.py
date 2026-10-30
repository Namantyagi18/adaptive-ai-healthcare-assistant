"""Secure Quarantined Storage for Medical Documents and Images."""

import hashlib
import uuid
from pathlib import Path
from typing import Tuple
from adapt_ai.config import settings
from adapt_ai.security.phi_sanitizer import logger


class SecureStorage:
    """Manages isolated, hashed storage of sensitive medical files."""

    @classmethod
    def save_file(cls, filename: str, file_bytes: bytes) -> Tuple[str, str, Path]:
        """Stores file with a cryptographic hash-based filename in quarantine.
        
        Returns:
            Tuple[str, str, Path]: (file_id, sha256_hash, stored_file_path)
        """
        sha256 = hashlib.sha256(file_bytes).hexdigest()
        file_id = f"med_{sha256[:12]}_{uuid.uuid4().hex[:6]}"
        ext = Path(filename).suffix.lower()
        secure_filename = f"{file_id}{ext}"
        
        storage_dir = settings.UPLOADS_DIR
        storage_dir.mkdir(parents=True, exist_ok=True)
        dest_path = storage_dir / secure_filename

        with open(dest_path, "wb") as f:
            f.write(file_bytes)

        logger.info(f"Safely quarantined file '{filename}' as '{secure_filename}' (SHA256: {sha256[:10]}...).")
        return file_id, sha256, dest_path

