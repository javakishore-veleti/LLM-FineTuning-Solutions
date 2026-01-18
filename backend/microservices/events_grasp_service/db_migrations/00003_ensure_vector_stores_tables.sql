-- 00003_ensure_vector_stores_tables.sql
-- Ensure all vector stores related tables exist (idempotent - uses IF NOT EXISTS)

-- EVENT VECTOR STORES
CREATE TABLE IF NOT EXISTS event_vector_stores (
    vector_store_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    vector_store_provider VARCHAR(100) NOT NULL,
    vector_config_json TEXT,
    vector_store_db_name VARCHAR(255) NOT NULL,
    vector_store_db_link TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- EVENT SCRAPING LOGS
CREATE TABLE IF NOT EXISTS event_scraping_logs (
    scraping_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    source_location TEXT NOT NULL,
    source_location_type VARCHAR(50) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    status VARCHAR(50) DEFAULT 'in_progress',
    output_location TEXT,
    output_location_type VARCHAR(50),
    files_scraped INTEGER DEFAULT 0,
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- VECTOR STORE FILES
CREATE TABLE IF NOT EXISTS vector_store_files (
    file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vector_store_id INTEGER NOT NULL,
    file_name VARCHAR(500) NOT NULL,
    file_display_name VARCHAR(255),
    row_created_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    uploaded_to_datetime DATETIME,
    status VARCHAR(50) DEFAULT 'pending',
    uploaded_flag BOOLEAN DEFAULT 0,
    source_file_location TEXT NOT NULL,
    source_location_type VARCHAR(50) NOT NULL,
    file_size_bytes BIGINT,
    file_metadata_json TEXT,
    FOREIGN KEY (vector_store_id) REFERENCES event_vector_stores(vector_store_id) ON DELETE CASCADE
);

-- EVENT VECTORIZATION LOGS
CREATE TABLE IF NOT EXISTS event_vectorization_logs (
    vectorization_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    vector_store_id INTEGER NOT NULL,
    source_location TEXT NOT NULL,
    source_location_type VARCHAR(50) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    status VARCHAR(50) DEFAULT 'in_progress',
    files_indexed INTEGER DEFAULT 0,
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (vector_store_id) REFERENCES event_vector_stores(vector_store_id) ON DELETE CASCADE
);

-- Indexes (IF NOT EXISTS)
CREATE INDEX IF NOT EXISTS idx_vector_stores_event ON event_vector_stores(event_id);
CREATE INDEX IF NOT EXISTS idx_vector_stores_provider ON event_vector_stores(vector_store_provider);
CREATE INDEX IF NOT EXISTS idx_vector_stores_status ON event_vector_stores(status);
CREATE INDEX IF NOT EXISTS idx_vector_files_store ON vector_store_files(vector_store_id);
CREATE INDEX IF NOT EXISTS idx_scraping_logs_event ON event_scraping_logs(event_id);
CREATE INDEX IF NOT EXISTS idx_scraping_logs_status ON event_scraping_logs(status);
CREATE INDEX IF NOT EXISTS idx_vectorization_logs_event ON event_vectorization_logs(event_id);
