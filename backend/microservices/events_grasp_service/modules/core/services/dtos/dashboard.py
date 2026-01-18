"""Dashboard DTO classes for request/response data transfer."""
from pydantic import BaseModel
from typing import Optional, List
from dataclasses import dataclass


class DashboardStatsModel(BaseModel):
    """Dashboard statistics model."""
    events: int = 0
    conversations: int = 0
    vector_stores: int = 0
    providers: int = 0


class RecentEventModel(BaseModel):
    """Recent event item for dashboard."""
    event_id: int
    name: str
    source: str
    indexed: bool = False


class RecentConversationModel(BaseModel):
    """Recent conversation item for dashboard."""
    conversation_id: int
    title: str
    messages: int = 0
    time_ago: str = ""


class DashboardDataReq(BaseModel):
    """Dashboard data request model."""
    customer_id: int
    limit: Optional[int] = 5


class DashboardDataResp(BaseModel):
    """Dashboard data response model."""
    success: bool = True
    message: Optional[str] = None
    stats: Optional[DashboardStatsModel] = None
    recent_events: Optional[List[RecentEventModel]] = None
    recent_conversations: Optional[List[RecentConversationModel]] = None


@dataclass
class DashboardCtx:
    """Dashboard context for service layer."""
    req: DashboardDataReq
    resp: DashboardDataResp = None

    def set_resp(self, resp: DashboardDataResp):
        self.resp = resp
        return self
