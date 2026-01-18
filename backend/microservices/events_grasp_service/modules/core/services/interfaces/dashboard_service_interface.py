"""Dashboard service interface."""
from abc import ABC, abstractmethod
from ..dtos.dashboard import DashboardCtx


class IDashboardService(ABC):
    """Interface for dashboard service operations."""

    @abstractmethod
    def get_dashboard_data(self, ctx: DashboardCtx) -> DashboardCtx:
        """
        Get dashboard data including stats and recent activity.

        Args:
            ctx: Dashboard context with request data containing customer_id

        Returns:
            DashboardCtx with response containing stats, recent events, and conversations
        """
        pass

    @abstractmethod
    def get_stats(self, ctx: DashboardCtx) -> DashboardCtx:
        """
        Get dashboard statistics only.

        Args:
            ctx: Dashboard context with request data containing customer_id

        Returns:
            DashboardCtx with response containing stats only
        """
        pass
