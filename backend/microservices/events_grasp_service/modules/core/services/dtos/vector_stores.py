"""Vector Stores DTO classes for request/response data transfer."""
from pydantic import BaseModel
from typing import Optional, List
from dataclasses import dataclass


class VectorStoreModel(BaseModel):
    """Vector store item model."""
    vector_store_id: int
    event_id: int
    event_name: Optional[str] = None
    vector_store_provider: str
    vector_store_db_name: str
    vector_store_db_link: Optional[str] = None
    status: str = 'pending'
    files_count: int = 0
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class VectorStoreCreateReq(BaseModel):
    """Request model for creating a vector store."""
    event_id: int
    vector_store_provider: str
    vector_store_db_name: str
    vector_store_db_link: Optional[str] = None
    vector_config_json: Optional[str] = None


class VectorStoreUpdateReq(BaseModel):
    """Request model for updating a vector store."""
    vector_store_provider: Optional[str] = None
    vector_store_db_name: Optional[str] = None
    vector_store_db_link: Optional[str] = None
    vector_config_json: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


class VectorStoresReq(BaseModel):
    """Request model for listing vector stores."""
    event_id: Optional[int] = None
    customer_id: Optional[int] = 1
    limit: Optional[int] = 100


class VectorStoresResp(BaseModel):
    """Response model for vector stores operations."""
    success: bool = True
    message: Optional[str] = None
    vector_stores: Optional[List[VectorStoreModel]] = None
    vector_store: Optional[VectorStoreModel] = None
    total_count: int = 0


class VectorStoreStatsModel(BaseModel):
    """Statistics for vector stores."""
    total_stores: int = 0
    active_stores: int = 0
    total_files: int = 0
    providers: List[str] = []


@dataclass
class VectorStoresCtx:
    """Vector stores context for service layer."""
    req: VectorStoresReq
    resp: VectorStoresResp = None

    def set_resp(self, resp: VectorStoresResp):
        self.resp = resp
        return self
