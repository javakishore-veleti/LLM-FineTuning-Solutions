"""PBKDF2-only password hashing utilities.
This module uses PBKDF2-HMAC-SHA256 for hashing and verification and DOES NOT rely on passlib or bcrypt.
Stored format: base64(salt(16) + dk(32)) using 100_000 iterations.
"""
import hashlib
import os
import base64
from typing import Tuple

_ITERATIONS = 100_000
_SALT_BYTES = 16
_DK_BYTES = 32


def _encode(salt: bytes, dk: bytes) -> str:
    return base64.b64encode(salt + dk).decode('utf-8')


def _decode(encoded: str) -> Tuple[bytes, bytes]:
    b = base64.b64decode(encoded.encode('utf-8'))
    salt, dk = b[:_SALT_BYTES], b[_SALT_BYTES:]
    return salt, dk


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 and return a base64-encoded salt+dk string."""
    salt = os.urandom(_SALT_BYTES)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, _ITERATIONS, dklen=_DK_BYTES)
    return _encode(salt, dk)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a stored base64(salt+dk) string."""
    try:
        salt, dk = _decode(hashed)
        check = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, _ITERATIONS, dklen=len(dk))
        import hmac
        return hmac.compare_digest(check, dk)
    except Exception:
        return False
