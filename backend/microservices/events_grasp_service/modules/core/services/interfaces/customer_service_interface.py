from abc import ABC, abstractmethod
from ...dtos.customer_dtos import CustomerCtx

class ICustomerService(ABC):
    @abstractmethod
    def create(self, ctx: CustomerCtx) -> CustomerCtx:
        pass

    @abstractmethod
    def get(self, ctx: CustomerCtx) -> CustomerCtx:
        pass

    @abstractmethod
    def list(self, ctx: CustomerCtx) -> CustomerCtx:
        pass

    @abstractmethod
    def update(self, ctx: CustomerCtx) -> CustomerCtx:
        pass

    @abstractmethod
    def delete(self, ctx: CustomerCtx) -> CustomerCtx:
        pass
