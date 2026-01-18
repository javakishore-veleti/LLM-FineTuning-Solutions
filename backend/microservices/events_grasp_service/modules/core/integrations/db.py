from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Optional
import os
from pathlib import Path

class DBManager:
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(os.getcwd(), 'runtime_data', 'events.db')}"
        # ensure runtime_data dir exists for sqlite
        if self.database_url.startswith('sqlite'):
            sqlite_path = self.database_url.replace('sqlite:///', '')
            folder = os.path.dirname(sqlite_path)
            if folder:
                Path(folder).mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(self.database_url, connect_args={"check_same_thread": False} if self.database_url.startswith('sqlite') else {})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def init_db(self):
        self.Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()
