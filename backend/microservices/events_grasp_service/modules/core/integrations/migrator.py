import sqlite3
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def _find_repo_root(start: Path) -> Path:
    """Find the repository root by looking for package.json or .git"""
    cur = start.resolve()
    for _ in range(10):
        if (cur / 'package.json').exists() or (cur / '.git').exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    # fallback to repository's parent directories (four up from this file)
    return start.resolve().parents[4] if len(start.resolve().parents) >= 5 else start.resolve()

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent.parent.parent / 'db_migrations'
REPO_ROOT = _find_repo_root(Path(__file__).resolve())
DB_PATH = REPO_ROOT / 'runtime_data' / 'events.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def apply_migrations(db_url: str = None):
    # very simple sqlite-only migrator: run SQL files in alphanumeric order if not applied
    logger.info(f'[Migrator] REPO_ROOT: {REPO_ROOT}')
    logger.info(f'[Migrator] MIGRATIONS_DIR: {MIGRATIONS_DIR}')
    logger.info(f'[Migrator] DB_PATH: {DB_PATH}')
    logger.info(f'[Migrator] Current working directory: {os.getcwd()}')

    if db_url and not db_url.startswith('sqlite'):
        logger.warning('apply_migrations currently supports only sqlite in this simple implementation')
    db_file = DB_PATH

    logger.info(f'[Migrator] Connecting to database: {db_file}')
    conn = sqlite3.connect(str(db_file))
    try:
        cur = conn.cursor()
        # ensure migrations table exists
        cur.execute('''CREATE TABLE IF NOT EXISTS _migrations (
            migration_id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename VARCHAR(512) NOT NULL UNIQUE,
            applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()

        files = sorted([p for p in MIGRATIONS_DIR.glob('*.sql')])
        logger.info(f'[Migrator] Found {len(files)} migration files: {[f.name for f in files]}')

        for f in files:
            fname = f.name
            cur.execute('SELECT 1 FROM _migrations WHERE filename = ?', (fname,))
            if cur.fetchone():
                logger.info(f'[Migrator] Skipping already applied migration: {fname}')
                continue
            logger.info(f'[Migrator] Applying migration: {fname}')
            sql = f.read_text()
            cur.executescript(sql)
            cur.execute('INSERT INTO _migrations (filename) VALUES (?)', (fname,))
            conn.commit()
            logger.info(f'[Migrator] Successfully applied: {fname}')
        logger.info('[Migrator] All migrations applied')
    except Exception as e:
        logger.exception(f'[Migrator] Error applying migrations: {e}')
        raise
    finally:
        conn.close()
