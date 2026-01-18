"""Vector Stores API routes."""
import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any
from pydantic import BaseModel
from ...core.services.dtos.vector_stores import (
    VectorStoresCtx,
    VectorStoresReq,
    VectorStoresResp,
    VectorStoreCreateReq,
    VectorStoreUpdateReq
)
from ...core.services.impl.vector_stores_service_impl import VectorStoresServiceSingleton
from ...core.integrations.db import get_db_manager
from ...core.vector_stores import VectorStoreConfigFacade, is_provider_available
from ...core.auth import get_current_customer, AuthenticatedCustomer, require_customer_id

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/api/vector-stores', tags=['vector-stores'])

# Initialize DB manager and service
DB = get_db_manager()
vector_stores_service = VectorStoresServiceSingleton(DB)


@router.get('/', response_model=VectorStoresResp)
def list_vector_stores(
    event_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    limit: Optional[int] = 100
):
    """
    Get all vector stores, optionally filtered by event or customer.

    Args:
        event_id: Optional event ID to filter by
        customer_id: Optional customer ID to filter by (get all vector stores for customer's events)
        limit: Maximum number of stores to return (default: 100)

    Returns:
        List of vector stores with event names and file counts
    """
    logger.info(f"[list_vector_stores] Called with event_id={event_id}, customer_id={customer_id}, limit={limit}")

    # Validate customer_id if provided
    if customer_id is not None:
        require_customer_id(customer_id)

    try:
        req = VectorStoresReq(event_id=event_id, customer_id=customer_id, limit=limit)
        ctx = VectorStoresCtx(req=req)
        logger.debug(f"[list_vector_stores] Request created: {req}")

        ctx = vector_stores_service.list_vector_stores(ctx)
        logger.debug(f"[list_vector_stores] Service returned: success={ctx.resp.success}, message={ctx.resp.message}")

        if not ctx.resp.success:
            logger.error(f"[list_vector_stores] Service failed: {ctx.resp.message}")
            raise HTTPException(status_code=500, detail=ctx.resp.message)

        logger.info(f"[list_vector_stores] Returning {len(ctx.resp.vector_stores or [])} vector stores")
        return ctx.resp
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"[list_vector_stores] Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{vector_store_id}', response_model=VectorStoresResp)
def get_vector_store(vector_store_id: int):
    """
    Get a specific vector store by ID.

    Args:
        vector_store_id: The vector store ID

    Returns:
        Vector store details
    """
    req = VectorStoresReq()
    ctx = VectorStoresCtx(req=req)
    ctx = vector_stores_service.get_vector_store(ctx, vector_store_id)

    if not ctx.resp.success:
        raise HTTPException(status_code=404, detail=ctx.resp.message)

    return ctx.resp


@router.post('/', response_model=VectorStoresResp, status_code=201)
def create_vector_store(payload: VectorStoreCreateReq):
    """
    Create a new vector store.

    Args:
        payload: Vector store creation data

    Returns:
        Created vector store details
    """
    req = VectorStoresReq()
    ctx = VectorStoresCtx(req=req)
    ctx = vector_stores_service.create_vector_store(ctx, payload.model_dump())

    if not ctx.resp.success:
        raise HTTPException(status_code=400, detail=ctx.resp.message)

    return ctx.resp


@router.put('/{vector_store_id}', response_model=VectorStoresResp)
def update_vector_store(vector_store_id: int, payload: VectorStoreUpdateReq):
    """
    Update an existing vector store.

    Args:
        vector_store_id: The vector store ID
        payload: Updated vector store data

    Returns:
        Updated vector store details
    """
    req = VectorStoresReq()
    ctx = VectorStoresCtx(req=req)
    ctx = vector_stores_service.update_vector_store(ctx, vector_store_id, payload.model_dump(exclude_unset=True))

    if not ctx.resp.success:
        raise HTTPException(status_code=400, detail=ctx.resp.message)

    return ctx.resp


@router.delete('/{vector_store_id}', response_model=VectorStoresResp)
def delete_vector_store(vector_store_id: int):
    """
    Delete a vector store.

    Args:
        vector_store_id: The vector store ID

    Returns:
        Success/failure message
    """
    req = VectorStoresReq()
    ctx = VectorStoresCtx(req=req)
    ctx = vector_stores_service.delete_vector_store(ctx, vector_store_id)

    if not ctx.resp.success:
        raise HTTPException(status_code=404, detail=ctx.resp.message)

    return ctx.resp


# ============== Provider Configuration Routes ==============

class ProviderConfigRequest(BaseModel):
    """Request model for creating a vector store with provider config."""
    event_id: int
    display_name: str
    provider_type: str
    config: Dict[str, Any]


class TestConnectionRequest(BaseModel):
    """Request model for testing connection."""
    provider_type: str
    config: Dict[str, Any]


@router.get('/providers/list')
def get_all_providers():
    """
    Get all available vector store providers with their metadata.

    Returns:
        List of providers with name, category, status, and description
    """
    logger.info("[get_all_providers] Fetching all providers")
    providers = VectorStoreConfigFacade.get_all_providers()
    return {
        "success": True,
        "providers": providers
    }


@router.get('/providers/categories')
def get_provider_categories():
    """
    Get providers grouped by category.

    Returns:
        Dictionary with categories as keys and provider lists as values
    """
    logger.info("[get_provider_categories] Fetching providers by category")
    categories = VectorStoreConfigFacade.get_provider_categories()
    return {
        "success": True,
        "categories": categories
    }


@router.get('/providers/{provider_type}/schema')
def get_provider_schema(provider_type: str):
    """
    Get the configuration schema for a specific provider.

    Args:
        provider_type: The provider type (e.g., 'aws_opensearch', 'mongodb_atlas')

    Returns:
        Configuration schema with fields, types, and validation rules
    """
    logger.info(f"[get_provider_schema] Fetching schema for provider: {provider_type}")
    try:
        schema = VectorStoreConfigFacade.get_config_schema(provider_type)
        return {
            "success": True,
            "schema": schema
        }
    except Exception as e:
        logger.exception(f"[get_provider_schema] Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/providers/validate')
def validate_provider_config(request: ProviderConfigRequest):
    """
    Validate a provider configuration without saving.

    Args:
        request: Provider configuration to validate

    Returns:
        Validation result with success status and any error messages
    """
    logger.info(f"[validate_provider_config] Validating config for provider: {request.provider_type}")

    is_valid, error = VectorStoreConfigFacade.validate_config(
        request.provider_type,
        request.config
    )

    return {
        "success": is_valid,
        "valid": is_valid,
        "error": error
    }


@router.post('/providers/test-connection')
def test_provider_connection(request: TestConnectionRequest):
    """
    Test connection to a vector store provider.

    Args:
        request: Provider type and configuration

    Returns:
        Connection test result
    """
    logger.info(f"[test_provider_connection] Testing connection for provider: {request.provider_type}")

    success, message = VectorStoreConfigFacade.test_connection(
        request.provider_type,
        request.config
    )

    return {
        "success": success,
        "message": message
    }


@router.post('/providers/create', response_model=VectorStoresResp, status_code=201)
def create_vector_store_with_config(request: ProviderConfigRequest):
    """
    Create a new vector store with provider-specific configuration.

    Args:
        request: Event ID, display name, provider type, and configuration

    Returns:
        Created vector store details
    """
    logger.info(f"[create_vector_store_with_config] Creating vector store: {request.display_name} with provider: {request.provider_type}")

    # Check if provider is available
    if not is_provider_available(request.provider_type):
        raise HTTPException(
            status_code=400,
            detail=f"Provider '{request.provider_type}' is not yet available"
        )

    # Validate and create config
    success, result, error = VectorStoreConfigFacade.create_vector_store_config(
        request.provider_type,
        request.display_name,
        request.config
    )

    if not success:
        raise HTTPException(status_code=400, detail=error)

    # Create the vector store in database
    create_req = VectorStoresReq()
    ctx = VectorStoresCtx(req=create_req)

    store_data = {
        "event_id": request.event_id,
        "vector_store_provider": request.provider_type,
        "vector_store_db_name": request.display_name,
        "vector_config_json": result.get("config_json")
    }

    ctx = vector_stores_service.create_vector_store(ctx, store_data)

    if not ctx.resp.success:
        raise HTTPException(status_code=400, detail=ctx.resp.message)

    logger.info(f"[create_vector_store_with_config] Successfully created vector store")
    return ctx.resp


class StandaloneVectorStoreRequest(BaseModel):
    """Request model for creating a standalone vector store (no event association)."""
    display_name: str
    provider_type: str
    config: Dict[str, Any]


@router.post('/providers/create-standalone', response_model=VectorStoresResp, status_code=201)
def create_standalone_vector_store(request: StandaloneVectorStoreRequest):
    """
    Create a new standalone vector store without event association.
    The vector store can be associated with events later from the Event Details page.

    Args:
        request: Display name, provider type, and configuration

    Returns:
        Created vector store details
    """
    logger.info(f"[create_standalone_vector_store] Creating standalone vector store: {request.display_name} with provider: {request.provider_type}")

    # Check if provider is available
    if not is_provider_available(request.provider_type):
        raise HTTPException(
            status_code=400,
            detail=f"Provider '{request.provider_type}' is not yet available"
        )

    # Validate and create config
    success, result, error = VectorStoreConfigFacade.create_vector_store_config(
        request.provider_type,
        request.display_name,
        request.config
    )

    if not success:
        raise HTTPException(status_code=400, detail=error)

    # Create the vector store in database (without event_id)
    create_req = VectorStoresReq()
    ctx = VectorStoresCtx(req=create_req)

    store_data = {
        "event_id": None,  # No event association
        "vector_store_provider": request.provider_type,
        "vector_store_db_name": request.display_name,
        "vector_config_json": result.get("config_json")
    }

    ctx = vector_stores_service.create_vector_store(ctx, store_data)

    if not ctx.resp.success:
        raise HTTPException(status_code=400, detail=ctx.resp.message)

    logger.info(f"[create_standalone_vector_store] Successfully created standalone vector store")
    return ctx.resp


