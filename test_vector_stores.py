#!/usr/bin/env python
"""Test script for vector stores service."""
import sys
sys.path.insert(0, '/Users/vavkkishore/PycharmProjects/LLM-FineTuning-Solutions')

print("Starting test...")

# First apply migrations
from backend.microservices.events_grasp_service.modules.core.integrations.migrator import apply_migrations
print("Applying migrations...")
apply_migrations()
print("Migrations done!")

from backend.microservices.events_grasp_service.modules.core.integrations.db import get_db_manager

try:
    db = get_db_manager()
    db.init_db()
    print("DB initialized")

    # Test with raw SQL first
    from sqlalchemy import text
    with db.session_scope() as session:
        query = text("SELECT COUNT(*) FROM event_vector_stores")
        result = session.execute(query)
        count = result.fetchone()[0]
        print(f"Vector stores count: {count}")

        # Try full query
        query2 = text("""
            SELECT 
                vs.vector_store_id,
                vs.event_id,
                e.event_name,
                vs.vector_store_provider,
                vs.vector_store_db_name,
                vs.vector_store_db_link,
                vs.status,
                vs.is_active,
                vs.created_at,
                vs.updated_at,
                COUNT(vsf.file_id) as files_count
            FROM event_vector_stores vs
            LEFT JOIN events e ON vs.event_id = e.event_id
            LEFT JOIN vector_store_files vsf ON vs.vector_store_id = vsf.vector_store_id
            GROUP BY vs.vector_store_id
            ORDER BY vs.created_at DESC
            LIMIT :limit
        """)
        result2 = session.execute(query2, {"limit": 100})
        rows = result2.fetchall()
        print(f"Query returned {len(rows)} rows")
        for row in rows:
            print(f"  Row: {row}")

    print("SUCCESS!")

except Exception as e:
    import traceback
    print(f'Error: {e}')
    traceback.print_exc()
