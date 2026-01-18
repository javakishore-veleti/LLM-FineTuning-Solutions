"""Scraping Logs service implementation."""
from datetime import datetime
from typing import Optional
from sqlalchemy import text
from ..interfaces.scraping_logs_service_interface import IScrapingLogsService
from ..dtos.scraping_logs import (
    ScrapingLogsCtx, ScrapingLogsResp,
    EventSummaryModel, ScrapingLogModel, ScrapedFileModel
)


class ScrapingLogsService(IScrapingLogsService):
    """Implementation of scraping logs service."""

    def __init__(self, db_manager):
        self.db = db_manager

    def get_events_with_scraping_summary(self, ctx: ScrapingLogsCtx) -> ScrapingLogsCtx:
        """Get all events with their scraping summary."""
        try:
            with self.db.session_scope() as session:
                # Query events with aggregated scraping stats
                query = text("""
                    SELECT 
                        e.event_id,
                        e.event_name,
                        e.source_url,
                        COUNT(DISTINCT sl.scraping_log_id) as total_scrapes,
                        COALESCE(SUM(sl.files_scraped), 0) as total_files,
                        MAX(sl.start_time) as last_scrape_date
                    FROM events e
                    LEFT JOIN event_scraping_logs sl ON e.event_id = sl.event_id
                    WHERE e.is_active = 1
                    GROUP BY e.event_id, e.event_name, e.source_url
                    ORDER BY e.event_name ASC
                """)

                result = session.execute(query)
                rows = result.fetchall()

                events = []
                for row in rows:
                    last_scrape = None
                    if row[5]:
                        if isinstance(row[5], str):
                            last_scrape = row[5]
                        else:
                            last_scrape = row[5].strftime("%Y-%m-%d %H:%M:%S")

                    events.append(EventSummaryModel(
                        event_id=row[0],
                        event_name=row[1],
                        source_url=row[2],
                        total_scrapes=row[3] or 0,
                        total_files=row[4] or 0,
                        last_scrape_date=last_scrape
                    ))

                ctx.set_resp(ScrapingLogsResp(
                    success=True,
                    events=events
                ))

        except Exception as e:
            ctx.set_resp(ScrapingLogsResp(
                success=False,
                message=f"Failed to fetch events: {str(e)}"
            ))

        return ctx

    def get_scraping_logs_for_event(self, ctx: ScrapingLogsCtx) -> ScrapingLogsCtx:
        """Get all scraping execution logs for a specific event."""
        try:
            event_id = ctx.req.event_id
            if not event_id:
                ctx.set_resp(ScrapingLogsResp(
                    success=False,
                    message="event_id is required"
                ))
                return ctx

            with self.db.session_scope() as session:
                query = text("""
                    SELECT 
                        scraping_log_id,
                        event_id,
                        source_location,
                        source_location_type,
                        start_time,
                        end_time,
                        status,
                        output_location,
                        output_location_type,
                        files_scraped,
                        error_message,
                        created_at
                    FROM event_scraping_logs
                    WHERE event_id = :event_id
                    ORDER BY start_time DESC
                    LIMIT :limit
                """)

                result = session.execute(query, {
                    "event_id": event_id,
                    "limit": ctx.req.limit or 50
                })
                rows = result.fetchall()

                logs = []
                for row in rows:
                    start_time = self._format_datetime(row[4])
                    end_time = self._format_datetime(row[5])
                    duration = self._calculate_duration(row[4], row[5])

                    logs.append(ScrapingLogModel(
                        scraping_log_id=row[0],
                        event_id=row[1],
                        source_location=row[2],
                        source_location_type=row[3],
                        start_time=start_time,
                        end_time=end_time,
                        status=row[6] or 'in_progress',
                        output_location=row[7],
                        output_location_type=row[8],
                        files_scraped=row[9] or 0,
                        error_message=row[10],
                        created_at=self._format_datetime(row[11]),
                        duration=duration
                    ))

                ctx.set_resp(ScrapingLogsResp(
                    success=True,
                    scraping_logs=logs
                ))

        except Exception as e:
            ctx.set_resp(ScrapingLogsResp(
                success=False,
                message=f"Failed to fetch scraping logs: {str(e)}"
            ))

        return ctx

    def get_scraped_files_for_event(self, ctx: ScrapingLogsCtx) -> ScrapingLogsCtx:
        """Get all scraped files for a specific event."""
        try:
            event_id = ctx.req.event_id
            if not event_id:
                ctx.set_resp(ScrapingLogsResp(
                    success=False,
                    message="event_id is required"
                ))
                return ctx

            with self.db.session_scope() as session:
                # Get files through vector stores linked to the event
                query = text("""
                    SELECT 
                        vsf.file_id,
                        vsf.file_name,
                        vsf.file_display_name,
                        vsf.source_file_location,
                        vsf.source_location_type,
                        vsf.file_size_bytes,
                        vsf.status,
                        vsf.uploaded_flag,
                        vsf.row_created_dt
                    FROM vector_store_files vsf
                    INNER JOIN event_vector_stores evs ON vsf.vector_store_id = evs.vector_store_id
                    WHERE evs.event_id = :event_id
                    ORDER BY vsf.row_created_dt DESC
                    LIMIT :limit
                """)

                result = session.execute(query, {
                    "event_id": event_id,
                    "limit": ctx.req.limit or 100
                })
                rows = result.fetchall()

                files = []
                for row in rows:
                    files.append(ScrapedFileModel(
                        file_id=row[0],
                        file_name=row[1],
                        file_display_name=row[2],
                        source_file_location=row[3],
                        source_location_type=row[4],
                        file_size_bytes=row[5],
                        file_size_display=self._format_file_size(row[5]),
                        status=row[6] or 'pending',
                        uploaded_flag=bool(row[7]),
                        created_at=self._format_datetime(row[8])
                    ))

                ctx.set_resp(ScrapingLogsResp(
                    success=True,
                    scraped_files=files
                ))

        except Exception as e:
            ctx.set_resp(ScrapingLogsResp(
                success=False,
                message=f"Failed to fetch scraped files: {str(e)}"
            ))

        return ctx

    def _format_datetime(self, dt) -> Optional[str]:
        """Format datetime to string."""
        if not dt:
            return None
        if isinstance(dt, str):
            return dt
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def _calculate_duration(self, start_time, end_time) -> Optional[str]:
        """Calculate duration between start and end time."""
        if not start_time or not end_time:
            return None

        try:
            if isinstance(start_time, str):
                start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            if isinstance(end_time, str):
                end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))

            diff = end_time - start_time
            total_seconds = int(diff.total_seconds())

            if total_seconds < 60:
                return f"{total_seconds}s"
            elif total_seconds < 3600:
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                return f"{minutes}m {seconds}s"
            else:
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                return f"{hours}h {minutes}m"
        except Exception:
            return None

    def _format_file_size(self, size_bytes) -> Optional[str]:
        """Format file size to human-readable string."""
        if not size_bytes:
            return None

        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


class ScrapingLogsServiceSingleton:
    """Singleton wrapper for ScrapingLogsService."""

    _instance = None

    def __new__(cls, db_manager=None):
        if cls._instance is None:
            if db_manager is None:
                raise ValueError("db_manager required for first instantiation")
            cls._instance = ScrapingLogsService(db_manager)
        return cls._instance

    @classmethod
    def reset(cls):
        """Reset singleton instance (useful for testing)."""
        cls._instance = None
