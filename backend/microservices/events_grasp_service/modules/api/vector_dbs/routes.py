"""Vector Stores API routes."""
import logging
from fastapi import APIRouter, HTTPException
from typing import Optional
from ...core.services.dtos.vector_stores import (
    VectorStoresCtx,
    VectorStoresReq,
    VectorStoresResp,
    VectorStoreCreateReq,
    VectorStoreUpdateReq
)
from ...core.services.impl.vector_stores_service_impl import VectorStoresServiceSingleton
from ...core.integrations.db import get_db_manager

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/api/vector-stores', tags=['vector-stores'])

# Initialize DB manager and service
DB = get_db_manager()
vector_stores_service = VectorStoresServiceSingleton(DB)


@router.get('/', response_model=VectorStoresResp)
def list_vector_stores(event_id: Optional[int] = None, customer_id: Optional[int] = None, limit: Optional[int] = 100):
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
