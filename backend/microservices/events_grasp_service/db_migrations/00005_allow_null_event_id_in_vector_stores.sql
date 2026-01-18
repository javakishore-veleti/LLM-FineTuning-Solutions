-- 00005_allow_null_event_id_in_vector_stores.sql
-- Allow vector stores to be created without an event association
-- They can be associated with events later from the Event Details page

-- SQLite doesn't support ALTER COLUMN, so we need to:
-- 1. Create a new table with nullable event_id
-- 2. Copy data from old table
-- 3. Drop old table
-- 4. Rename new table

-- Create new table with nullable event_id
CREATE TABLE IF NOT EXISTS event_vector_stores_new (
    vector_store_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,  -- Now nullable
    vector_store_provider VARCHAR(100) NOT NULL,
    vector_config_json TEXT,
    vector_store_db_name VARCHAR(255) NOT NULL,
    vector_store_db_link TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE SET NULL
);

-- Copy existing data
INSERT INTO event_vector_stores_new
    (vector_store_id, event_id, vector_store_provider, vector_config_json,
     vector_store_db_name, vector_store_db_link, status, created_at, updated_at, is_active)
SELECT
    vector_store_id, event_id, vector_store_provider, vector_config_json,
    vector_store_db_name, vector_store_db_link, status, created_at, updated_at, is_active
FROM event_vector_stores;

-- Drop old table
DROP TABLE IF EXISTS event_vector_stores;

-- Rename new table
ALTER TABLE event_vector_stores_new RENAME TO event_vector_stores;

-- Recreate indexes
CREATE INDEX IF NOT EXISTS idx_vector_stores_event ON event_vector_stores(event_id);
CREATE INDEX IF NOT EXISTS idx_vector_stores_provider ON event_vector_stores(vector_store_provider);
CREATE INDEX IF NOT EXISTS idx_vector_stores_status ON event_vector_stores(status);
