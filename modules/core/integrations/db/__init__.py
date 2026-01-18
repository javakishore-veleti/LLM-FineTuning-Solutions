from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DB_URL = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(os.getcwd(), 'runtime_data', 'events.db')}"

# Ensure runtime_data dir exists
os.makedirs(os.path.dirname(DB_URL.replace('sqlite:///', '')), exist_ok=True)

engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """Create all tables. Call this at app startup."""
    Base.metadata.create_all(bind=engine)
