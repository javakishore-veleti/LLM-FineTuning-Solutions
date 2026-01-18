from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.sql import func
from ..integrations.db import Base

class EventProvider(Base):
    __tablename__ = 'event_providers'

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey('events.event_id', ondelete='CASCADE'), nullable=False)
    provider_id = Column(Integer, ForeignKey('providers.provider_id', ondelete='CASCADE'), nullable=False)
    provider_config_json = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
