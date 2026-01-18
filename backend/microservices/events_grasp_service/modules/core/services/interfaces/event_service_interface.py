from abc import ABC, abstractmethod
from typing import Optional
from ...services.dtos.event_crud import EventCrudCtx

class IEventService(ABC):
    @abstractmethod
    def create(self, ctx: EventCrudCtx) -> EventCrudCtx:
        pass

    @abstractmethod
    def get(self, ctx: EventCrudCtx) -> EventCrudCtx:
        pass

    @abstractmethod
    def list(self, ctx: EventCrudCtx) -> EventCrudCtx:
        pass

    @abstractmethod
    def update(self, ctx: EventCrudCtx) -> EventCrudCtx:
        pass

    @abstractmethod
    def delete(self, ctx: EventCrudCtx) -> EventCrudCtx:
        pass
