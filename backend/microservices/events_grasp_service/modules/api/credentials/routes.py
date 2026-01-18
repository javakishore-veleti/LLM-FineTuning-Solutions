"""Credentials API routes."""
import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any
from pydantic import BaseModel

from ...core.credentials import (
    get_credential_providers,
    get_provider_auth_types,
    get_credential_schema,
    is_credential_provider_available,
    get_credentials_service
)
from ...core.integrations.db import get_db_manager
from ...core.auth import get_current_customer, AuthenticatedCustomer

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/api/credentials', tags=['credentials'])

# Initialize DB manager
DB = get_db_manager()


class CredentialCreateRequest(BaseModel):
    """Request model for creating a credential."""
    credential_name: str
    provider_type: str
    auth_type: str
    config: Dict[str, Any]
    description: Optional[str] = ""


class CredentialUpdateRequest(BaseModel):
    """Request model for updating a credential."""
    credential_name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


# ============== Provider Routes ==============

@router.get('/providers')
def list_credential_providers():
    """
    Get all available credential providers.

    Returns:
        List of providers with their auth types and metadata
    """
    logger.info("[list_credential_providers] Fetching all credential providers")
    providers = get_credential_providers()
    return {
        "success": True,
        "providers": providers
    }


@router.get('/providers/{provider_type}/auth-types')
def get_auth_types(provider_type: str):
    """
    Get available authentication types for a provider.

    Args:
        provider_type: The provider type (aws, azure, gcp, etc.)

    Returns:
        List of auth types for the provider
    """
    logger.info(f"[get_auth_types] Fetching auth types for provider: {provider_type}")
    auth_types = get_provider_auth_types(provider_type)
    return {
        "success": True,
        "auth_types": auth_types
    }


@router.get('/providers/{provider_type}/schema/{auth_type}')
def get_schema(provider_type: str, auth_type: str):
    """
    Get the configuration schema for a provider and auth type.

    Args:
        provider_type: The provider type
        auth_type: The authentication type

    Returns:
        Configuration schema with fields
    """
    logger.info(f"[get_schema] Fetching schema for {provider_type}:{auth_type}")
    schema = get_credential_schema(provider_type, auth_type)
    return {
        "success": True,
        "schema": schema
    }


# ============== Credential CRUD Routes ==============

@router.get('/')
async def list_credentials(
    provider_type: Optional[str] = None,
    customer: AuthenticatedCustomer = Depends(get_current_customer)
):
    """
    List all credentials for the current customer.

    Args:
        provider_type: Optional filter by provider type

    Returns:
        List of credentials
    """
    logger.info(f"[list_credentials] Listing credentials for customer {customer.customer_id}")
    service = get_credentials_service(DB)
    result = service.list_credentials(customer.customer_id, provider_type)

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("message"))

    return result


@router.get('/{credential_id}')
async def get_credential(
    credential_id: int,
    customer: AuthenticatedCustomer = Depends(get_current_customer)
):
    """
    Get a specific credential by ID.

    Args:
        credential_id: The credential ID

    Returns:
        Credential details (with masked sensitive fields)
    """
    logger.info(f"[get_credential] Getting credential {credential_id} for customer {customer.customer_id}")
    service = get_credentials_service(DB)
    result = service.get_credential(credential_id, customer.customer_id)

    if not result["success"]:
        raise HTTPException(status_code=404, detail=result.get("message"))

    return result


@router.post('/', status_code=201)
async def create_credential(
    request: CredentialCreateRequest,
    customer: AuthenticatedCustomer = Depends(get_current_customer)
):
    """
    Create a new credential.

    Args:
        request: Credential creation data

    Returns:
        Created credential ID
    """
    logger.info(f"[create_credential] Creating credential '{request.credential_name}' for customer {customer.customer_id}")

    # Check if provider is available
    if not is_credential_provider_available(request.provider_type):
        raise HTTPException(
            status_code=400,
            detail=f"Provider '{request.provider_type}' is not yet available"
        )

    service = get_credentials_service(DB)
    result = service.create_credential(customer.customer_id, {
        "credential_name": request.credential_name,
        "provider_type": request.provider_type,
        "auth_type": request.auth_type,
        "config": request.config,
        "description": request.description
    })

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("message"))

    return result


@router.put('/{credential_id}')
async def update_credential(
    credential_id: int,
    request: CredentialUpdateRequest,
    customer: AuthenticatedCustomer = Depends(get_current_customer)
):
    """
    Update an existing credential.

    Args:
        credential_id: The credential ID
        request: Updated credential data

    Returns:
        Success message
    """
    logger.info(f"[update_credential] Updating credential {credential_id} for customer {customer.customer_id}")

    service = get_credentials_service(DB)
    result = service.update_credential(
        credential_id,
        customer.customer_id,
        request.model_dump(exclude_unset=True)
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("message"))

    return result


@router.delete('/{credential_id}')
async def delete_credential(
    credential_id: int,
    customer: AuthenticatedCustomer = Depends(get_current_customer)
):
    """
    Delete a credential.

    Args:
        credential_id: The credential ID

    Returns:
        Success message
    """
    logger.info(f"[delete_credential] Deleting credential {credential_id} for customer {customer.customer_id}")

    service = get_credentials_service(DB)
    result = service.delete_credential(credential_id, customer.customer_id)

    if not result["success"]:
        raise HTTPException(status_code=404, detail=result.get("message"))

    return result


@router.get('/for-provider/{vector_store_provider}')
async def get_credentials_for_vector_store(
    vector_store_provider: str,
    customer: AuthenticatedCustomer = Depends(get_current_customer)
):
    """
    Get credentials compatible with a specific vector store provider.

    Args:
        vector_store_provider: The vector store provider type

    Returns:
        List of compatible credentials
    """
    logger.info(f"[get_credentials_for_vector_store] Getting credentials for {vector_store_provider}")

    service = get_credentials_service(DB)
    credentials = service.get_credentials_for_provider(
        customer.customer_id,
        vector_store_provider
    )

    return {
        "success": True,
        "credentials": credentials
    }
