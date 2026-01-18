from pydantic import BaseModel
from dataclasses import dataclass
from typing import Optional, List

class CustomerReq(BaseModel):
    customer_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class CustomerApiModel(BaseModel):
    customer_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    is_active: bool
    created_at: Optional[str] = None

class CustomerResp(BaseModel):
    success: bool
    message: Optional[str] = None
    customer: Optional[CustomerApiModel] = None
    customers: Optional[List[CustomerApiModel]] = None

@dataclass
class CustomerCtx:
    req: CustomerReq
    resp: CustomerResp = None

    def set_resp(self, resp: CustomerResp):
        self.resp = resp
        return self
