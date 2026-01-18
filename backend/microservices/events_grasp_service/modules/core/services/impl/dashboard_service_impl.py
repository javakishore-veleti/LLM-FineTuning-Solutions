"""Dashboard service implementation."""
from datetime import datetime, timedelta
from typing import List
from ..interfaces.dashboard_service_interface import IDashboardService
from ..dtos.dashboard import (
    DashboardCtx,
    DashboardDataResp,
    DashboardStatsModel,
    RecentEventModel,
    RecentConversationModel
)


class DashboardService(IDashboardService):
    """Implementation of dashboard service."""

    def __init__(self, db_manager, event_model, provider_model=None):
        """
        Initialize dashboard service with database manager and models.

        Args:
            db_manager: Database manager instance
            event_model: SQLAlchemy Event model
            provider_model: Optional SQLAlchemy Provider model
        """
        self._db = db_manager
        self._event_model = event_model
        self._provider_model = provider_model

    def get_dashboard_data(self, ctx: DashboardCtx) -> DashboardCtx:
        """Get complete dashboard data including stats and recent activity."""
        try:
            customer_id = ctx.req.customer_id
            limit = ctx.req.limit or 5

            # Get stats
            stats = self._get_stats_for_customer(customer_id)

            # Get recent events
            recent_events = self._get_recent_events(customer_id, limit)

            # Get recent conversations (placeholder - implement when conversation model exists)
            recent_conversations = self._get_recent_conversations(customer_id, limit)

            resp = DashboardDataResp(
                success=True,
                stats=stats,
                recent_events=recent_events,
                recent_conversations=recent_conversations
            )
            return ctx.set_resp(resp)

        except Exception as e:
            resp = DashboardDataResp(
                success=False,
                message=f"Failed to fetch dashboard data: {str(e)}"
            )
            return ctx.set_resp(resp)

    def get_stats(self, ctx: DashboardCtx) -> DashboardCtx:
        """Get dashboard statistics only."""
        try:
            customer_id = ctx.req.customer_id
            stats = self._get_stats_for_customer(customer_id)

            resp = DashboardDataResp(
                success=True,
                stats=stats
            )
            return ctx.set_resp(resp)

        except Exception as e:
            resp = DashboardDataResp(
                success=False,
                message=f"Failed to fetch stats: {str(e)}"
            )
            return ctx.set_resp(resp)

    def _get_stats_for_customer(self, customer_id: int) -> DashboardStatsModel:
        """Get statistics for a specific customer."""
        with self._db.session() as session:
            # Count events for this customer
            # Note: For now counting all events; can filter by customer_id if needed
            events_count = session.query(self._event_model).count()

            # Count providers (vector stores + LLM providers)
            vector_stores_count = 0
            providers_count = 0
            if self._provider_model:
                # Count by provider type
                vector_stores_count = session.query(self._provider_model).filter(
                    self._provider_model.provider_type == 'vector_db'
                ).count()
                providers_count = session.query(self._provider_model).filter(
                    self._provider_model.provider_type == 'llm'
                ).count()

            # Conversations count - placeholder
            conversations_count = 0

            return DashboardStatsModel(
                events=events_count,
                conversations=conversations_count,
                vector_stores=vector_stores_count,
                providers=providers_count
            )

    def _get_recent_events(self, customer_id: int, limit: int) -> List[RecentEventModel]:
        """Get recent events for dashboard."""
        with self._db.session() as session:
            events = session.query(self._event_model).order_by(
                self._event_model.created_at.desc()
            ).limit(limit).all()

            recent_events = []
            for event in events:
                recent_events.append(RecentEventModel(
                    event_id=event.event_id,
                    name=event.event_name,
                    source=event.source_url or '',
                    indexed=getattr(event, 'is_indexed', False) if hasattr(event, 'is_indexed') else False
                ))

            return recent_events

    def _get_recent_conversations(self, customer_id: int, limit: int) -> List[RecentConversationModel]:
        """Get recent conversations for dashboard. Placeholder for now."""
        # TODO: Implement when conversation model exists
        return []

    def _format_time_ago(self, dt: datetime) -> str:
        """Format datetime as human-readable time ago string."""
        if not dt:
            return ""

        now = datetime.utcnow()
        diff = now - dt

        if diff < timedelta(minutes=1):
            return "just now"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff < timedelta(days=7):
            days = diff.days
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            return dt.strftime("%b %d, %Y")


class DashboardServiceSingleton:
    """Singleton wrapper for DashboardService."""

    _instance = None

    def __new__(cls, db_manager=None, event_model=None, provider_model=None):
        if cls._instance is None:
            if db_manager is None or event_model is None:
                raise ValueError("db_manager and event_model required for first instantiation")
            cls._instance = DashboardService(db_manager, event_model, provider_model)
        return cls._instance

    @classmethod
    def reset(cls):
        """Reset singleton instance (useful for testing)."""
        cls._instance = None
