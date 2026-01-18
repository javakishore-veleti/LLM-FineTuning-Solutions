-- 00004_ensure_email_uniqueness.sql
-- Ensure email uniqueness is case-insensitive and add index

-- Create a unique index on lowercase email to prevent case-insensitive duplicates
-- SQLite doesn't support functional indexes directly, so we'll use COLLATE NOCASE
-- First, let's ensure the existing constraint and add a case-insensitive index

-- Drop the old index if it exists and create a case-insensitive one
DROP INDEX IF EXISTS idx_customers_email_lower;
CREATE UNIQUE INDEX IF NOT EXISTS idx_customers_email_nocase ON customers(email COLLATE NOCASE);
