-- 00002_create_application_tables.sql
-- Create core application tables: events, providers, event_providers, scraping logs, vector stores, vectorization logs, vector_store_files, conversations, conversation_files, chats

-- EVENTS
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name VARCHAR(255) NOT NULL,
    event_description TEXT,
    source_url TEXT NOT NULL,
    source_location_type VARCHAR(50) DEFAULT 'http_url',
    customer_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE SET NULL
);

-- PROVIDERS
CREATE TABLE IF NOT EXISTS providers (
    provider_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_type VARCHAR(100) NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    credentials_json TEXT,
    customer_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE SET NULL
);

-- EVENT PROVIDERS (association)
CREATE TABLE IF NOT EXISTS event_providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    provider_config_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id) ON DELETE CASCADE
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

-- CONVERSATIONS
CREATE TABLE IF NOT EXISTS conversations (
    conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    conversation_name VARCHAR(255) NOT NULL,
    conversation_desc TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- CONVERSATION FILES
CREATE TABLE IF NOT EXISTS conversation_files (
    conversation_id INTEGER NOT NULL,
    file_id INTEGER NOT NULL,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (conversation_id, file_id),
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES vector_store_files(file_id) ON DELETE CASCADE
);

-- CHATS
CREATE TABLE IF NOT EXISTS chats (
    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    chat_log_json TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_events_active ON events(is_active);
CREATE INDEX IF NOT EXISTS idx_scraping_logs_event ON event_scraping_logs(event_id);
CREATE INDEX IF NOT EXISTS idx_vectorization_logs_event ON event_vectorization_logs(event_id);
CREATE INDEX IF NOT EXISTS idx_vector_stores_event ON event_vector_stores(event_id);
CREATE INDEX IF NOT EXISTS idx_vector_files_store ON vector_store_files(vector_store_id);
CREATE INDEX IF NOT EXISTS idx_conversations_event ON conversations(event_id);
CREATE INDEX IF NOT EXISTS idx_conversations_accessed ON conversations(last_accessed_at DESC);
CREATE INDEX IF NOT EXISTS idx_chats_conversation ON chats(conversation_id);
