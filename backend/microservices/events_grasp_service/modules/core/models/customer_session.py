from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func


def create_customer_session_model(Base):
    try:
        for cls in list(Base._decl_class_registry.values()):
            if isinstance(cls, type) and getattr(cls, '__tablename__', None) == 'customer_sessions':
                return cls
    except Exception:
        pass

    # bind to existing table if present
    try:
        if 'customer_sessions' in Base.metadata.tables:
            tbl = Base.metadata.tables['customer_sessions']
            CustomerSession = type('CustomerSession', (Base,), {'__table__': tbl})
            return CustomerSession
    except Exception:
        pass

    class CustomerSession(Base):
        __tablename__ = 'customer_sessions'
        __table_args__ = {'extend_existing': True}

        session_id = Column(Integer, primary_key=True, index=True)
        customer_id = Column(Integer, ForeignKey('customers.customer_id', ondelete='CASCADE'), nullable=False)
        token = Column(String(512), nullable=False, unique=True, index=True)
        expires_at = Column(DateTime, nullable=True)
        created_at = Column(DateTime, server_default=func.now())
    return CustomerSession
