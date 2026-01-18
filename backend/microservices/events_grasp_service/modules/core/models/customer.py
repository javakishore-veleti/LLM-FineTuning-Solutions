from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func

def create_customer_model(Base):
    # return existing mapped class if table already present
    try:
        for cls in list(Base._decl_class_registry.values()):
            if isinstance(cls, type) and getattr(cls, '__tablename__', None) == 'customers':
                return cls
    except Exception:
        pass

    # if table exists in metadata but no mapped class, create a mapped class that uses the existing Table
    try:
        if 'customers' in Base.metadata.tables:
            tbl = Base.metadata.tables['customers']
            Customer = type('Customer', (Base,), {'__table__': tbl})
            return Customer
    except Exception:
        pass

    class Customer(Base):
        __tablename__ = 'customers'
        __table_args__ = {'extend_existing': True}

        customer_id = Column(Integer, primary_key=True, index=True)
        first_name = Column(String(255))
        last_name = Column(String(255))
        email = Column(String(320), nullable=False, unique=True)
        password_hash = Column(Text, nullable=False)
        is_active = Column(Boolean, default=True)
        created_at = Column(DateTime, server_default=func.now())
        updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    return Customer
