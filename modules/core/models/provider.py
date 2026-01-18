from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from ..integrations.db import Base

class Provider(Base):
    __tablename__ = 'providers'

    provider_id = Column(Integer, primary_key=True, index=True)
    provider_type = Column(String(100), nullable=False)
    display_name = Column(String(255), nullable=False)
    credentials_json = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
