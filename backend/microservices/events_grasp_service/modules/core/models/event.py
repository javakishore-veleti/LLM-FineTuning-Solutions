from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func


# models will be bound to DBManager.Base at runtime

class EventModelMixin:
    # This mixin is used to define table structure; actual Base will be set in the module import time
    pass

# We will create the actual declarative model via a factory to avoid circular imports

def create_event_model(Base):
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

    return Event
