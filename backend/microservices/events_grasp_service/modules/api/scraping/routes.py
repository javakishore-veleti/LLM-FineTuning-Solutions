"""Scraping Logs API routes."""
from fastapi import APIRouter, HTTPException
from typing import Optional
from ...core.services.dtos.scraping_logs import (
    ScrapingLogsCtx,
    ScrapingLogsReq,
    ScrapingLogsResp
)
from ...core.services.impl.scraping_logs_service_impl import ScrapingLogsServiceSingleton
from ...core.integrations.db import get_db_manager

router = APIRouter(prefix='/api/scraping-logs', tags=['scraping-logs'])

# Initialize DB manager and service
DB = get_db_manager()
scraping_logs_service = ScrapingLogsServiceSingleton(DB)


@router.get('/events', response_model=ScrapingLogsResp)
def get_events_with_scraping_summary(customer_id: Optional[int] = 1):
    """
    Get all events with their scraping summary.

    Returns:
        List of events with total scrapes, files count, and last scrape date
    """
    req = ScrapingLogsReq(customer_id=customer_id)
    ctx = ScrapingLogsCtx(req=req)
    ctx = scraping_logs_service.get_events_with_scraping_summary(ctx)

    if not ctx.resp.success:
        raise HTTPException(status_code=500, detail=ctx.resp.message)

    return ctx.resp


@router.get('/events/{event_id}/logs', response_model=ScrapingLogsResp)
def get_scraping_logs_for_event(event_id: int, limit: Optional[int] = 50):
    """
    Get all scraping execution logs for a specific event.

    Args:
        event_id: The event ID
        limit: Maximum number of logs to return (default: 50)

    Returns:
        List of scraping logs with execution details
    """
    req = ScrapingLogsReq(event_id=event_id, limit=limit)
    ctx = ScrapingLogsCtx(req=req)
    ctx = scraping_logs_service.get_scraping_logs_for_event(ctx)

    if not ctx.resp.success:
        raise HTTPException(status_code=500, detail=ctx.resp.message)

    return ctx.resp


@router.get('/events/{event_id}/files', response_model=ScrapingLogsResp)
def get_scraped_files_for_event(event_id: int, limit: Optional[int] = 100):
    """
    Get all scraped files for a specific event.

    Args:
        event_id: The event ID
        limit: Maximum number of files to return (default: 100)

    Returns:
        List of scraped files with details
    """
    req = ScrapingLogsReq(event_id=event_id, limit=limit)
    ctx = ScrapingLogsCtx(req=req)
    ctx = scraping_logs_service.get_scraped_files_for_event(ctx)

    if not ctx.resp.success:
        raise HTTPException(status_code=500, detail=ctx.resp.message)

    return ctx.resp
