"""Scraping Logs service interface."""
from abc import ABC, abstractmethod
from ..dtos.scraping_logs import ScrapingLogsCtx


class IScrapingLogsService(ABC):
    """Interface for scraping logs service operations."""

    @abstractmethod
    def get_events_with_scraping_summary(self, ctx: ScrapingLogsCtx) -> ScrapingLogsCtx:
        """
        Get all events with their scraping summary (total scrapes, files, last scrape date).

        Args:
            ctx: Context with request data containing optional customer_id

        Returns:
            ScrapingLogsCtx with response containing list of events with summaries
        """
        pass

    @abstractmethod
    def get_scraping_logs_for_event(self, ctx: ScrapingLogsCtx) -> ScrapingLogsCtx:
        """
        Get all scraping execution logs for a specific event.

        Args:
            ctx: Context with request data containing event_id

        Returns:
            ScrapingLogsCtx with response containing scraping logs for the event
        """
        pass

    @abstractmethod
    def get_scraped_files_for_event(self, ctx: ScrapingLogsCtx) -> ScrapingLogsCtx:
        """
        Get all scraped files for a specific event.

        Args:
            ctx: Context with request data containing event_id

        Returns:
            ScrapingLogsCtx with response containing scraped files for the event
        """
        pass
