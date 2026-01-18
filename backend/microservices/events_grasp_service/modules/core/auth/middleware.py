"""Authentication middleware and dependencies for FastAPI."""
import logging
from typing import Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .customer_cache import get_customer_cache
from ..integrations.db import get_db_manager

logger = logging.getLogger(__name__)

# HTTP Bearer token security
security = HTTPBearer(auto_error=False)


class AuthenticatedCustomer:
    """Represents an authenticated customer."""
    def __init__(self, customer_id: int, email: str, first_name: str = None, last_name: str = None):
        self.customer_id = customer_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


def _get_customer_from_db(customer_id: int) -> Optional[dict]:
    """
    Fetch customer from database.

    Args:
        customer_id: The customer ID to look up

    Returns:
        Customer dict if found, None otherwise
    """
    try:
        db_manager = get_db_manager()
        with db_manager.session_scope() as session:
            from sqlalchemy import text
            query = text("""
                SELECT customer_id, email, first_name, last_name, is_active 
                FROM customers 
                WHERE customer_id = :customer_id
            """)
            result = session.execute(query, {"customer_id": customer_id})
            row = result.fetchone()

            if row and row[4]:  # Check is_active
                return {
                    "customer_id": row[0],
                    "email": row[1],
                    "first_name": row[2],
                    "last_name": row[3]
                }
            return None
    except Exception as e:
        logger.exception(f"[Auth] Error fetching customer {customer_id}: {e}")
        return None


def _get_session_from_db(token: str) -> Optional[dict]:
    """
    Fetch session from database by token.

    Args:
        token: The session token

    Returns:
        Session dict with customer_id if valid, None otherwise
    """
    try:
        db_manager = get_db_manager()
        with db_manager.session_scope() as session:
            from sqlalchemy import text
            from datetime import datetime

            query = text("""
                SELECT session_id, customer_id, expires_at 
                FROM customer_sessions 
                WHERE token = :token
            """)
            result = session.execute(query, {"token": token})
            row = result.fetchone()

            if row:
                expires_at = row[2]
                # Check if session is expired
                if expires_at:
                    if isinstance(expires_at, str):
                        expires_at = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                    if expires_at < datetime.utcnow():
                        logger.debug(f"[Auth] Session expired for token")
                        return None

                return {
                    "session_id": row[0],
                    "customer_id": row[1]
                }
            return None
    except Exception as e:
        logger.exception(f"[Auth] Error fetching session: {e}")
        return None


def validate_customer(customer_id: int) -> Optional[AuthenticatedCustomer]:
    """
    Validate that a customer exists and is active.
    Uses cache with 1-hour TTL to reduce DB access.

    Args:
        customer_id: The customer ID to validate

    Returns:
        AuthenticatedCustomer if valid, None otherwise
    """
    if customer_id is None:
        return None

    cache = get_customer_cache()

    # Check cache first
    cached_valid = cache.is_customer_valid(customer_id)

    if cached_valid is True:
        # Customer is cached as valid - still need to get details for the object
        # but we know they exist
        customer_data = _get_customer_from_db(customer_id)
        if customer_data:
            return AuthenticatedCustomer(**customer_data)
        else:
            # Customer was deleted - invalidate cache
            cache.invalidate_customer(customer_id)
            return None

    if cached_valid is False:
        # Customer is cached as invalid
        return None

    # Cache miss - check database
    customer_data = _get_customer_from_db(customer_id)

    if customer_data:
        # Cache as valid
        cache.set_customer_valid(customer_id, True)
        return AuthenticatedCustomer(**customer_data)
    else:
        # Cache as invalid
        cache.set_customer_valid(customer_id, False)
        return None


async def get_current_customer(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> AuthenticatedCustomer:
    """
    FastAPI dependency to get the current authenticated customer.

    Extracts token from Authorization header, validates session,
    and returns the authenticated customer.

    Raises:
        HTTPException 401 if not authenticated or invalid
    """
    token = None

    # Try to get token from Authorization header
    if credentials:
        token = credentials.credentials

    # Also check query parameter (for backward compatibility)
    if not token:
        token = request.query_params.get('token')

    if not token:
        logger.debug("[Auth] No token provided")
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Get session from database
    session_data = _get_session_from_db(token)

    if not session_data:
        logger.debug("[Auth] Invalid or expired token")
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Validate customer using cache
    customer = validate_customer(session_data["customer_id"])

    if not customer:
        logger.debug(f"[Auth] Customer {session_data['customer_id']} not found or inactive")
        raise HTTPException(
            status_code=401,
            detail="Customer account not found or inactive",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return customer


async def get_optional_customer(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[AuthenticatedCustomer]:
    """
    FastAPI dependency to optionally get the current authenticated customer.
    Returns None if not authenticated (doesn't raise exception).
    """
    try:
        return await get_current_customer(request, credentials)
    except HTTPException:
        return None


def require_customer_id(customer_id: Optional[int]) -> int:
    """
    Validate that a customer_id is provided and the customer exists.
    Use this in route handlers that receive customer_id as a parameter.

    Args:
        customer_id: The customer ID to validate

    Returns:
        The validated customer_id

    Raises:
        HTTPException 401 if customer_id is None or customer doesn't exist
    """
    if customer_id is None:
        raise HTTPException(
            status_code=401,
            detail="Customer ID required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    customer = validate_customer(customer_id)

    if not customer:
        raise HTTPException(
            status_code=401,
            detail="Customer not found or inactive",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return customer_id
