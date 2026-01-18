"""Scraped File model for tracking files generated during scraping."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, BigInteger, Boolean
from sqlalchemy.sql import func


def create_scraped_file_model(Base):
    """Factory function to create ScrapedFile model bound to the given Base."""
    # Return existing mapped class if table already present
    try:
        for cls in list(Base._decl_class_registry.values()):
            if isinstance(cls, type) and getattr(cls, '__tablename__', None) == 'vector_store_files':
                return cls
    except Exception:
        pass

    # If table exists in metadata but no mapped class, create a mapped class that uses the existing Table
    try:
        if 'vector_store_files' in Base.metadata.tables:
            tbl = Base.metadata.tables['vector_store_files']
            ScrapedFile = type('ScrapedFile', (Base,), {'__table__': tbl})
            return ScrapedFile
    except Exception:
        pass

    class ScrapedFile(Base):
        __tablename__ = 'vector_store_files'

        file_id = Column(Integer, primary_key=True, index=True)
        vector_store_id = Column(Integer, ForeignKey('event_vector_stores.vector_store_id', ondelete='CASCADE'), nullable=False)
        file_name = Column(String(500), nullable=False)
        file_display_name = Column(String(255))
        row_created_dt = Column(DateTime, server_default=func.now())
        uploaded_to_datetime = Column(DateTime)
        status = Column(String(50), default='pending')
        uploaded_flag = Column(Boolean, default=False)
        source_file_location = Column(Text, nullable=False)
        source_location_type = Column(String(50), nullable=False)
        file_size_bytes = Column(BigInteger)
        file_metadata_json = Column(Text)

    return ScrapedFile
