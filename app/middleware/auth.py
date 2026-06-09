"""
app/middleware/auth.py
---------------------
API-key authentication.  Add this as a dependency to any route you want
to protect.

Usage in a route file:
    from app.middleware.auth import verify_api_key

    @router.post("/ingest")
    async def ingest(payload: ..., _key: str = Depends(verify_api_key)):
        ...
"""
import hmac
import hashlib
from typing import Optional

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from app.config import settings

_header_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def _safe_compare(a: str, b: str) -> bool:
    """Constant-time string comparison — prevents timing attacks."""
    return hmac.compare_digest(
        hashlib.sha256(a.encode()).digest(),
        hashlib.sha256(b.encode()).digest(),
    )


async def verify_api_key(api_key: Optional[str] = Security(_header_scheme)) -> str:
    """
    FastAPI dependency that validates the X-API-Key request header.

    Raises 401 if the header is missing or the key is wrong.
    Returns the validated key on success.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )

    for valid_key in settings.api_keys:
        if _safe_compare(api_key, valid_key):
            return api_key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key",
    )