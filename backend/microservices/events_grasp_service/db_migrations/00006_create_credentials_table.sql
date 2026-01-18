-- 00006_create_credentials_table.sql
-- Create credentials table to store provider credentials securely

CREATE TABLE IF NOT EXISTS credentials (
    credential_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    credential_name VARCHAR(255) NOT NULL,
    provider_type VARCHAR(100) NOT NULL,  -- aws, azure, gcp, neo4j, elasticsearch, redis, pgvector, mongodb, pinecone, custom
    auth_type VARCHAR(100) NOT NULL,      -- Provider-specific auth type (e.g., basic, iam_role, profile for AWS)
    credential_config_json TEXT,          -- Encrypted/encoded credential configuration
    description TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_credentials_customer ON credentials(customer_id);
CREATE INDEX IF NOT EXISTS idx_credentials_provider ON credentials(provider_type);
CREATE INDEX IF NOT EXISTS idx_credentials_active ON credentials(is_active);

-- Unique constraint: each customer can only have one credential with the same name
CREATE UNIQUE INDEX IF NOT EXISTS idx_credentials_customer_name ON credentials(customer_id, credential_name);
