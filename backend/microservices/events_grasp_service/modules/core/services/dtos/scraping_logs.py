"""Scraping Logs DTO classes for request/response data transfer."""
from pydantic import BaseModel
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


class ScrapingLogModel(BaseModel):
    """Scraping log item model."""
    scraping_log_id: int
    event_id: int
    source_location: str
    source_location_type: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status: str = 'in_progress'
    output_location: Optional[str] = None
    output_location_type: Optional[str] = None
    files_scraped: int = 0
    error_message: Optional[str] = None
    created_at: Optional[str] = None
    duration: Optional[str] = None  # Human-readable duration


class ScrapedFileModel(BaseModel):
    """Scraped file item model."""
    file_id: int
    file_name: str
    file_display_name: Optional[str] = None
    source_file_location: str
    source_location_type: str
    file_size_bytes: Optional[int] = None
    file_size_display: Optional[str] = None  # Human-readable size
    status: str = 'pending'
    uploaded_flag: bool = False
    created_at: Optional[str] = None


class EventSummaryModel(BaseModel):
    """Event summary for dropdown."""
    event_id: int
    event_name: str
    source_url: str
    total_scrapes: int = 0
    total_files: int = 0
    last_scrape_date: Optional[str] = None


class ScrapingLogsReq(BaseModel):
    """Request model for scraping logs."""
    event_id: Optional[int] = None
    customer_id: Optional[int] = 1
    limit: Optional[int] = 50


class ScrapingLogsResp(BaseModel):
    """Response model for scraping logs."""
    success: bool = True
    message: Optional[str] = None
    events: Optional[List[EventSummaryModel]] = None
    scraping_logs: Optional[List[ScrapingLogModel]] = None
    scraped_files: Optional[List[ScrapedFileModel]] = None


@dataclass
class ScrapingLogsCtx:
    """Scraping logs context for service layer."""
    req: ScrapingLogsReq
    resp: ScrapingLogsResp = None

    def set_resp(self, resp: ScrapingLogsResp):
        self.resp = resp
        return self
