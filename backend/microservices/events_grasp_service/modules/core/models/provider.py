from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func


def create_provider_model(Base):
    try:
        for cls in list(Base._decl_class_registry.values()):
            if isinstance(cls, type) and getattr(cls, '__tablename__', None) == 'providers':
                return cls
    except Exception:
        pass

    # bind to existing table if present
    try:
        if 'providers' in Base.metadata.tables:
            tbl = Base.metadata.tables['providers']
            Provider = type('Provider', (Base,), {'__table__': tbl})
            return Provider
    except Exception:
        pass

    class Provider(Base):
        __tablename__ = 'providers'
        __table_args__ = {'extend_existing': True}

        provider_id = Column(Integer, primary_key=True, index=True)
        provider_type = Column(String(100), nullable=False)
        display_name = Column(String(255), nullable=False)
        credentials_json = Column(Text, nullable=True)
        customer_id = Column(Integer, ForeignKey('customers.customer_id', ondelete='SET NULL'), nullable=True)
        created_at = Column(DateTime, server_default=func.now())
        updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
        is_active = Column(Boolean, default=True)
    return Provider
