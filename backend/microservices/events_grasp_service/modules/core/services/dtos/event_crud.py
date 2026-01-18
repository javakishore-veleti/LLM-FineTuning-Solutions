from pydantic import BaseModel
from typing import Optional, List
from dataclasses import dataclass

class EventCrudReq(BaseModel):
    event_id: Optional[int] = None
    event_name: Optional[str] = None
    event_description: Optional[str] = None
    source_url: Optional[str] = None
    source_location_type: Optional[str] = 'http_url'
    is_active: Optional[bool] = True

class EventCrudApiModel(BaseModel):
    event_id: int
    event_name: str
    event_description: Optional[str] = None
    source_url: str
    source_location_type: Optional[str] = 'http_url'
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_active: Optional[bool] = True

class EventCrudResp(BaseModel):
    success: bool
    message: Optional[str] = None
    event: Optional[EventCrudApiModel] = None
    events: Optional[List[EventCrudApiModel]] = None

@dataclass
class EventCrudCtx:
    req: EventCrudReq
    resp: EventCrudResp = None

    def set_resp(self, resp: EventCrudResp):
        self.resp = resp
        return self
