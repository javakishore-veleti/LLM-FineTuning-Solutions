from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from ..integrations.db import Base

class Event(Base):
    __tablename__ = 'events'

    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(255), nullable=False)
    event_description = Column(Text)
    source_url = Column(Text, nullable=False)
    source_location_type = Column(String(50), default='http_url')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
