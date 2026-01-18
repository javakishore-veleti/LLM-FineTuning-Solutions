from typing import Protocol
from ..interfaces.event_service_interface import IEventService
from ..impl.event_service_impl import EventServiceSingleton
from ...integrations.db import DBManager
from ...models.event import create_event_model

# Factory function to return an IEventService instance (singleton under the hood)

def get_event_service(db: DBManager = None):
    dbm = db or DBManager()
    Base = dbm.Base
    EventModel = create_event_model(Base)
    svc: IEventService = EventServiceSingleton(dbm, EventModel)
    return svc
