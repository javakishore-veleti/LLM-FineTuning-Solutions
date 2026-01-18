"""Dashboard API routes."""
from fastapi import APIRouter, HTTPException
from typing import Optional
from ...core.services.dtos.dashboard import (
    DashboardCtx,
    DashboardDataReq,
    DashboardDataResp
)
from ...core.services.impl.dashboard_service_impl import DashboardServiceSingleton
from ...core.integrations.db import get_db_manager
from ...core.models.event import create_event_model
from ...core.models.provider import create_provider_model

router = APIRouter(prefix='/api/dashboard', tags=['dashboard'])

# Initialize DB manager and models
DB = get_db_manager()
Base = DB.Base
EventModel = create_event_model(Base)
ProviderModel = create_provider_model(Base)

# Initialize dashboard service singleton
dashboard_service = DashboardServiceSingleton(DB, EventModel, ProviderModel)


@router.get('/', response_model=DashboardDataResp)
def get_dashboard_data(customer_id: Optional[int] = 1, limit: Optional[int] = 5):
    """
    Get complete dashboard data including stats and recent activity.

    Args:
        customer_id: Customer ID (default: 1 for now)
        limit: Number of recent items to fetch (default: 5)

    Returns:
        Dashboard data with stats, recent events, and recent conversations
    """
    req = DashboardDataReq(customer_id=customer_id, limit=limit)
    ctx = DashboardCtx(req=req)
    ctx = dashboard_service.get_dashboard_data(ctx)

    if not ctx.resp.success:
        raise HTTPException(status_code=500, detail=ctx.resp.message)

    return ctx.resp


@router.get('/stats', response_model=DashboardDataResp)
def get_dashboard_stats(customer_id: Optional[int] = 1):
    """
    Get dashboard statistics only.

    Args:
        customer_id: Customer ID (default: 1 for now)

    Returns:
        Dashboard stats (events count, conversations count, vector stores, providers)
    """
    req = DashboardDataReq(customer_id=customer_id)
    ctx = DashboardCtx(req=req)
    ctx = dashboard_service.get_stats(ctx)

    if not ctx.resp.success:
        raise HTTPException(status_code=500, detail=ctx.resp.message)

    return ctx.resp
