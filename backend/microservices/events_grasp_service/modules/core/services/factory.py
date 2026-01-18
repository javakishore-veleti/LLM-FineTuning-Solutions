from .interfaces.event_service_interface import IEventService
from .interfaces.dashboard_service_interface import IDashboardService
from .impl.event_service_impl import EventServiceSingleton
from .impl.dashboard_service_impl import DashboardServiceSingleton
from ..integrations.db import DBManager, get_db_manager
from ..models.event import create_event_model
from ..models.provider import create_provider_model

# Factory function to return an IEventService instance (singleton under the hood)

def get_event_service(db: DBManager = None):
    dbm = db or get_db_manager()
    Base = dbm.Base
    EventModel = create_event_model(Base)
    svc: IEventService = EventServiceSingleton(dbm, EventModel)
    return svc


def get_dashboard_service(db: DBManager = None) -> IDashboardService:
    """Factory function to return an IDashboardService instance (singleton under the hood)."""
    dbm = db or get_db_manager()
    Base = dbm.Base
    EventModel = create_event_model(Base)
    ProviderModel = create_provider_model(Base)
    svc: IDashboardService = DashboardServiceSingleton(dbm, EventModel, ProviderModel)
    return svc

