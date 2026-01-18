from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Optional
import os
from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(10):
        if (cur / 'package.json').exists() or (cur / '.git').exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    # fallback to repository's parent directories (two up from this file)
    return start.resolve().parents[4] if len(start.resolve().parents) >= 5 else start.resolve()

class DBManager:
    def __init__(self, database_url: Optional[str] = None):
        repo_root = _find_repo_root(Path(__file__).resolve())
        default_db_path = repo_root / 'runtime_data' / 'events.db'
        default_db_path.parent.mkdir(parents=True, exist_ok=True)
        self.database_url = database_url or os.environ.get('DATABASE_URL') or f"sqlite:///{default_db_path}"
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


# Module-level singleton for the default DBManager
_default_db_manager: Optional[DBManager] = None


def get_db_manager() -> DBManager:
    """Return a singleton DBManager for the application default database."""
    global _default_db_manager
    if _default_db_manager is None:
        _default_db_manager = DBManager()
    return _default_db_manager
