"""Vector Store model for tracking event vector stores."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func


def create_vector_store_model(Base):
    """Factory function to create VectorStore model bound to the given Base."""
    # Return existing mapped class if table already present
    try:
        for cls in list(Base._decl_class_registry.values()):
            if isinstance(cls, type) and getattr(cls, '__tablename__', None) == 'event_vector_stores':
                return cls
    except Exception:
        pass

    # If table exists in metadata but no mapped class, create a mapped class that uses the existing Table
    try:
        if 'event_vector_stores' in Base.metadata.tables:
            tbl = Base.metadata.tables['event_vector_stores']
            VectorStore = type('VectorStore', (Base,), {'__table__': tbl})
            return VectorStore
    except Exception:
        pass

    class VectorStore(Base):
        __tablename__ = 'event_vector_stores'

        vector_store_id = Column(Integer, primary_key=True, index=True)
        event_id = Column(Integer, ForeignKey('events.event_id', ondelete='CASCADE'), nullable=False)
        vector_store_provider = Column(String(100), nullable=False)
        vector_config_json = Column(Text)
        vector_store_db_name = Column(String(255), nullable=False)
        vector_store_db_link = Column(Text)
        status = Column(String(50), default='pending')  # pending, active, error
        created_at = Column(DateTime, server_default=func.now())
        updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
        is_active = Column(Boolean, default=True)

    return VectorStore
