from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.sql import func

def create_event_provider_model(Base):
    try:
        for cls in list(Base._decl_class_registry.values()):
            if isinstance(cls, type) and getattr(cls, '__tablename__', None) == 'event_providers':
                return cls
    except Exception:
        pass

    try:
        if 'event_providers' in Base.metadata.tables:
            tbl = Base.metadata.tables['event_providers']
            EventProvider = type('EventProvider', (Base,), {'__table__': tbl})
            return EventProvider
    except Exception:
        pass

    class EventProvider(Base):
        __tablename__ = 'event_providers'
        __table_args__ = {'extend_existing': True}

        id = Column(Integer, primary_key=True, index=True)
        event_id = Column(Integer, ForeignKey('events.event_id', ondelete='CASCADE'), nullable=False)
        provider_id = Column(Integer, ForeignKey('providers.provider_id', ondelete='CASCADE'), nullable=False)
        provider_config_json = Column(Text, nullable=True)
        created_at = Column(DateTime, server_default=func.now())
        updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
        is_active = Column(Boolean, default=True)
    return EventProvider
