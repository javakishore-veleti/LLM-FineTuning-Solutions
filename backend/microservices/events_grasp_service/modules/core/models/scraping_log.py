"""Scraping Log model for tracking event scraping executions."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func


def create_scraping_log_model(Base):
    """Factory function to create ScrapingLog model bound to the given Base."""
    # Return existing mapped class if table already present
    try:
        for cls in list(Base._decl_class_registry.values()):
            if isinstance(cls, type) and getattr(cls, '__tablename__', None) == 'event_scraping_logs':
                return cls
    except Exception:
        pass

    # If table exists in metadata but no mapped class, create a mapped class that uses the existing Table
    try:
        if 'event_scraping_logs' in Base.metadata.tables:
            tbl = Base.metadata.tables['event_scraping_logs']
            ScrapingLog = type('ScrapingLog', (Base,), {'__table__': tbl})
            return ScrapingLog
    except Exception:
        pass

    class ScrapingLog(Base):
        __tablename__ = 'event_scraping_logs'

        scraping_log_id = Column(Integer, primary_key=True, index=True)
        event_id = Column(Integer, ForeignKey('events.event_id', ondelete='CASCADE'), nullable=False)
        source_location = Column(Text, nullable=False)
        source_location_type = Column(String(50), nullable=False)
        start_time = Column(DateTime, nullable=False)
        end_time = Column(DateTime)
        status = Column(String(50), default='in_progress')  # in_progress, completed, failed
        output_location = Column(Text)
        output_location_type = Column(String(50))
        files_scraped = Column(Integer, default=0)
        error_message = Column(Text)
        created_at = Column(DateTime, server_default=func.now())

    return ScrapingLog
