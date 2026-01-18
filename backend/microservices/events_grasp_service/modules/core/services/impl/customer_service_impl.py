from threading import Lock
from events_grasp_service.modules.core.services.interfaces.customer_service_interface import ICustomerService
from events_grasp_service.modules.core.dtos.customer_dtos import CustomerCtx, CustomerReq, CustomerResp, CustomerApiModel
from events_grasp_service.modules.core.dao.impl.customer_dao import CustomerDAO
from events_grasp_service.modules.core.utils.passwords import hash_password, verify_password

class CustomerServiceSingleton(ICustomerService):
    _instance = None
    _lock = Lock()

    def __new__(cls, db_manager, CustomerModel):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._init(db_manager, CustomerModel)
        return cls._instance

    def _init(self, db_manager, CustomerModel):
        self.dao = CustomerDAO(db_manager, CustomerModel)

    def create(self, ctx: CustomerCtx) -> CustomerCtx:
        req: CustomerReq = ctx.req
        # hash password
        if not req.password:
            ctx.set_resp(CustomerResp(success=False, message='password required'))
            return ctx
        password_hash = hash_password(req.password)
        cust = self.dao.create_customer({
            'first_name': req.first_name,
            'last_name': req.last_name,
            'email': req.email,
            'password_hash': password_hash
        })
        api = CustomerApiModel(customer_id=cust.customer_id, first_name=cust.first_name, last_name=cust.last_name, email=cust.email, is_active=cust.is_active, created_at=cust.created_at.isoformat() if cust.created_at else None)
        ctx.set_resp(CustomerResp(success=True, customer=api))
        return ctx

    def get(self, ctx: CustomerCtx) -> CustomerCtx:
        req: CustomerReq = ctx.req
        cust = self.dao.get_customer_by_id(req.customer_id)
        if not cust:
            ctx.set_resp(CustomerResp(success=False, message='not found'))
            return ctx
        api = CustomerApiModel(customer_id=cust.customer_id, first_name=cust.first_name, last_name=cust.last_name, email=cust.email, is_active=cust.is_active, created_at=cust.created_at.isoformat() if cust.created_at else None)
        ctx.set_resp(CustomerResp(success=True, customer=api))
        return ctx

    def list(self, ctx: CustomerCtx) -> CustomerCtx:
        custs = self.dao.list_customers()
        apis = [CustomerApiModel(customer_id=c.customer_id, first_name=c.first_name, last_name=c.last_name, email=c.email, is_active=c.is_active, created_at=c.created_at.isoformat() if c.created_at else None) for c in custs]
        ctx.set_resp(CustomerResp(success=True, customers=apis))
        return ctx

    def update(self, ctx: CustomerCtx) -> CustomerCtx:
        req: CustomerReq = ctx.req
        data = req.dict(exclude_none=True)
        if 'password' in data:
            data['password_hash'] = hash_password(data.pop('password'))
        cust = self.dao.update_customer(req.customer_id, data)
        if not cust:
            ctx.set_resp(CustomerResp(success=False, message='not found'))
            return ctx
        api = CustomerApiModel(customer_id=cust.customer_id, first_name=cust.first_name, last_name=cust.last_name, email=cust.email, is_active=cust.is_active, created_at=cust.created_at.isoformat() if cust.created_at else None)
        ctx.set_resp(CustomerResp(success=True, customer=api))
        return ctx

    def delete(self, ctx: CustomerCtx) -> CustomerCtx:
        req: CustomerReq = ctx.req
        ok = self.dao.delete_customer(req.customer_id)
        ctx.set_resp(CustomerResp(success=ok, message='deleted' if ok else 'not found'))
        return ctx
