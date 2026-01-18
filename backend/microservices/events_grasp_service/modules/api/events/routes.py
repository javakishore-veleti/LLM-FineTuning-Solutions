from fastapi import APIRouter, HTTPException
from typing import List
from events_grasp_service.modules.core.services.dtos.event_crud import EventCrudReq, EventCrudResp, EventCrudApiModel, EventCrudCtx
from events_grasp_service.modules.core.services.impl.event_service_impl import EventServiceSingleton
from events_grasp_service.modules.core.integrations.db import get_db_manager
from events_grasp_service.modules.core.models.event import create_event_model

router = APIRouter(prefix='/api/events')

# instantiate service singleton using shared DBManager and model
DB = get_db_manager()
Base = DB.Base
EventModel = create_event_model(Base)
service = EventServiceSingleton(DB, EventModel)

@router.get('/', response_model=List[EventCrudApiModel])
def list_events():
    ctx = EventCrudCtx(req=EventCrudReq())
    ctx = service.list(ctx)
    return ctx.resp.events or []

@router.get('/{event_id}', response_model=EventCrudApiModel)
def get_event(event_id: int):
    ctx = EventCrudCtx(req=EventCrudReq(event_id=event_id))
    ctx = service.get(ctx)
    if not ctx.resp.success:
        raise HTTPException(status_code=404, detail=ctx.resp.message)
    return ctx.resp.event

@router.post('/', response_model=EventCrudResp, status_code=201)
def create_event(payload: EventCrudReq):
    ctx = EventCrudCtx(req=payload)
    ctx = service.create(ctx)
    return ctx.resp

@router.put('/{event_id}', response_model=EventCrudResp)
def update_event(event_id: int, payload: EventCrudReq):
    payload.event_id = event_id
    ctx = EventCrudCtx(req=payload)
    ctx = service.update(ctx)
    if not ctx.resp.success:
        raise HTTPException(status_code=404, detail=ctx.resp.message)
    return ctx.resp

@router.delete('/{event_id}', response_model=EventCrudResp)
def delete_event(event_id: int):
    ctx = EventCrudCtx(req=EventCrudReq(event_id=event_id))
    ctx = service.delete(ctx)
    if not ctx.resp.success:
        raise HTTPException(status_code=404, detail=ctx.resp.message)
    return ctx.resp
