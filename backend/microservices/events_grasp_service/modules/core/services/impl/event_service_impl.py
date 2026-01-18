from threading import Lock
from typing import List
from ...services.interfaces.event_service_interface import IEventService
from ...services.dtos.event_crud import EventCrudCtx, EventCrudReq, EventCrudResp, EventCrudApiModel
from ...dao.event_dao import EventDAO

class EventServiceSingleton(IEventService):
    _instance = None
    _lock = Lock()

    def __new__(cls, db_manager, EventModel):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._init(db_manager, EventModel)
        return cls._instance

    def _init(self, db_manager, EventModel):
        self.dao = EventDAO(db_manager, EventModel)

    def create(self, ctx: EventCrudCtx) -> EventCrudCtx:
        req: EventCrudReq = ctx.req
        ev = self.dao.create_event(req.dict())
        api = EventCrudApiModel(
            event_id=ev.event_id,
            event_name=ev.event_name,
            event_description=ev.event_description,
            source_url=ev.source_url,
            source_location_type=ev.source_location_type,
            created_at=ev.created_at.isoformat() if ev.created_at else None,
            updated_at=ev.updated_at.isoformat() if ev.updated_at else None,
            is_active=ev.is_active
        )
        resp = EventCrudResp(success=True, message='created', event=api)
        ctx.set_resp(resp)
        return ctx

    def get(self, ctx: EventCrudCtx) -> EventCrudCtx:
        req: EventCrudReq = ctx.req
        ev = self.dao.get_event(req.event_id)
        if not ev:
            ctx.set_resp(EventCrudResp(success=False, message='not found'))
            return ctx
        api = EventCrudApiModel(
            event_id=ev.event_id,
            event_name=ev.event_name,
            event_description=ev.event_description,
            source_url=ev.source_url,
            source_location_type=ev.source_location_type,
            created_at=ev.created_at.isoformat() if ev.created_at else None,
            updated_at=ev.updated_at.isoformat() if ev.updated_at else None,
            is_active=ev.is_active
        )
        ctx.set_resp(EventCrudResp(success=True, event=api))
        return ctx

    def list(self, ctx: EventCrudCtx) -> EventCrudCtx:
        evs = self.dao.list_events()
        apis = [EventCrudApiModel(
            event_id=e.event_id,
            event_name=e.event_name,
            event_description=e.event_description,
            source_url=e.source_url,
            source_location_type=e.source_location_type,
            created_at=e.created_at.isoformat() if e.created_at else None,
            updated_at=e.updated_at.isoformat() if e.updated_at else None,
            is_active=e.is_active
        ) for e in evs]
        ctx.set_resp(EventCrudResp(success=True, events=apis))
        return ctx

    def update(self, ctx: EventCrudCtx) -> EventCrudCtx:
        req: EventCrudReq = ctx.req
        ev = self.dao.update_event(req.event_id, req.dict())
        if not ev:
            ctx.set_resp(EventCrudResp(success=False, message='not found'))
            return ctx
        api = EventCrudApiModel(
            event_id=ev.event_id,
            event_name=ev.event_name,
            event_description=ev.event_description,
            source_url=ev.source_url,
            source_location_type=ev.source_location_type,
            created_at=ev.created_at.isoformat() if ev.created_at else None,
            updated_at=ev.updated_at.isoformat() if ev.updated_at else None,
            is_active=ev.is_active
        )
        ctx.set_resp(EventCrudResp(success=True, event=api))
        return ctx

    def delete(self, ctx: EventCrudCtx) -> EventCrudCtx:
        req: EventCrudReq = ctx.req
        ok = self.dao.delete_event(req.event_id)
        ctx.set_resp(EventCrudResp(success=ok, message='deleted' if ok else 'not found'))
        return ctx
