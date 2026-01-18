from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func


# models will be bound to DBManager.Base at runtime

class EventModelMixin:
    # This mixin is used to define table structure; actual Base will be set in the module import time
    pass

# We will create the actual declarative model via a factory to avoid circular imports

def create_event_model(Base):
    # return existing mapped class if table already present
    try:
        for cls in list(Base._decl_class_registry.values()):
            if isinstance(cls, type) and getattr(cls, '__tablename__', None) == 'events':
                return cls
    except Exception:
        pass

    # if table exists in metadata but no mapped class, create a mapped class that uses the existing Table
    try:
        if 'events' in Base.metadata.tables:
            tbl = Base.metadata.tables['events']
            Event = type('Event', (Base,), {'__table__': tbl})
            return Event
    except Exception:
        pass

    class Event(Base):
        __tablename__ = 'events'

        event_id = Column(Integer, primary_key=True, index=True)
        event_name = Column(String(255), nullable=False)
        event_description = Column(Text)
        source_url = Column(Text, nullable=False)
        source_location_type = Column(String(50), default='http_url')
        customer_id = Column(Integer, ForeignKey('customers.customer_id', ondelete='SET NULL'), nullable=True)
        created_at = Column(DateTime, server_default=func.now())
        updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
        is_active = Column(Boolean, default=True)

    return Event
