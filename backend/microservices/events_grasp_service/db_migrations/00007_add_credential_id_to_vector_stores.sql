-- 00007_add_credential_id_to_vector_stores.sql
-- Add credential_id column to event_vector_stores table

-- SQLite doesn't support ADD COLUMN with FOREIGN KEY directly in older versions
-- So we add the column first without the constraint
ALTER TABLE event_vector_stores ADD COLUMN credential_id INTEGER REFERENCES credentials(credential_id);

-- Create index for the new column
CREATE INDEX IF NOT EXISTS idx_vector_stores_credential ON event_vector_stores(credential_id);
