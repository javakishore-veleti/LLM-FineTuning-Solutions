import sqlite3
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent.parent / 'db_migrations'
DB_PATH = Path(os.getcwd()) / 'runtime_data' / 'events.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def apply_migrations(db_url: str = None):
    # very simple sqlite-only migrator: run SQL files in alphanumeric order if not applied
    if db_url and not db_url.startswith('sqlite'):
        logger.warning('apply_migrations currently supports only sqlite in this simple implementation')
    db_file = DB_PATH
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
        for f in files:
            fname = f.name
            cur.execute('SELECT 1 FROM _migrations WHERE filename = ?', (fname,))
            if cur.fetchone():
                logger.info(f'Skipping already applied migration: {fname}')
                continue
            logger.info(f'Applying migration: {fname}')
            sql = f.read_text()
            cur.executescript(sql)
            cur.execute('INSERT INTO _migrations (filename) VALUES (?)', (fname,))
            conn.commit()
        logger.info('Migrations applied')
    finally:
        conn.close()
