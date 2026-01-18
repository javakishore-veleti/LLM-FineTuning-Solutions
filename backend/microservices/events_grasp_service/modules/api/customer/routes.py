from fastapi import APIRouter, HTTPException
from typing import List
from ...core.dtos.customer_dtos import CustomerReq, CustomerCtx, CustomerResp, CustomerApiModel
from ...core.services.impl.customer_service_impl import CustomerServiceSingleton
from ...core.integrations.db import get_db_manager
from ...core.models.customer import create_customer_model

router = APIRouter(prefix='/api/customers')

DB = get_db_manager()
Base = DB.Base
CustomerModel = create_customer_model(Base)
service = CustomerServiceSingleton(DB, CustomerModel)

@router.get('/', response_model=List[CustomerApiModel])
def list_customers():
    ctx = CustomerCtx(req=CustomerReq())
    ctx = service.list(ctx)
    return ctx.resp.customers or []

@router.get('/{customer_id}', response_model=CustomerApiModel)
def get_customer(customer_id: int):
    ctx = CustomerCtx(req=CustomerReq(customer_id=customer_id))
    ctx = service.get(ctx)
    if not ctx.resp.success:
        raise HTTPException(status_code=404, detail=ctx.resp.message)
    return ctx.resp.customer

@router.post('/', response_model=CustomerResp, status_code=201)
def create_customer(payload: CustomerReq):
    ctx = CustomerCtx(req=payload)
    ctx = service.create(ctx)
    return ctx.resp

@router.put('/{customer_id}', response_model=CustomerResp)
def update_customer(customer_id: int, payload: CustomerReq):
    payload.customer_id = customer_id
    ctx = CustomerCtx(req=payload)
    ctx = service.update(ctx)
    if not ctx.resp.success:
        raise HTTPException(status_code=404, detail=ctx.resp.message)
    return ctx.resp

@router.delete('/{customer_id}', response_model=CustomerResp)
def delete_customer(customer_id: int):
    ctx = CustomerCtx(req=CustomerReq(customer_id=customer_id))
    ctx = service.delete(ctx)
    if not ctx.resp.success:
        raise HTTPException(status_code=404, detail=ctx.resp.message)
    return ctx.resp
