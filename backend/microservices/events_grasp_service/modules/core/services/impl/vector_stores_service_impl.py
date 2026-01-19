"""Vector Stores service implementation."""
import logging
from typing import Optional
from sqlalchemy import text
from ..interfaces.vector_stores_service_interface import IVectorStoresService
from ..dtos.vector_stores import (
    VectorStoresCtx, VectorStoresResp, VectorStoreModel
)

# Set up logging
logger = logging.getLogger(__name__)


class VectorStoresService(IVectorStoresService):
    """Implementation of vector stores service."""

    def __init__(self, db_manager):
        self.db = db_manager
        logger.info("[VectorStoresService] Initialized")

    def list_vector_stores(self, ctx: VectorStoresCtx) -> VectorStoresCtx:
        """Get all vector stores with event names and file counts."""
        logger.info(f"[list_vector_stores] Starting - event_id={ctx.req.event_id}, customer_id={ctx.req.customer_id}, limit={ctx.req.limit}")
        try:
            with self.db.session_scope() as session:
                logger.debug("[list_vector_stores] Got database session")
                # Build query based on filters provided
                if ctx.req.event_id:
                    # Filter by specific event
                    query = text("""
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
                        WHERE vs.event_id = :event_id
                        GROUP BY vs.vector_store_id
                        ORDER BY vs.created_at DESC
                        LIMIT :limit
                    """)
                    result = session.execute(query, {
                        "event_id": ctx.req.event_id,
                        "limit": ctx.req.limit or 100
                    })
                    logger.debug(f"[list_vector_stores] Executed query for event_id={ctx.req.event_id}")
                elif ctx.req.customer_id:
                    # Filter by customer (get vector stores for all events owned by customer)
                    logger.debug(f"[list_vector_stores] Building query for customer_id={ctx.req.customer_id}")
                    query = text("""
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
                        WHERE e.customer_id = :customer_id
                        GROUP BY vs.vector_store_id
                        ORDER BY vs.created_at DESC
                        LIMIT :limit
                    """)
                    result = session.execute(query, {
                        "customer_id": ctx.req.customer_id,
                        "limit": ctx.req.limit or 100
                    })
                    logger.debug(f"[list_vector_stores] Executed query for customer_id={ctx.req.customer_id}")
                else:
                    # No filters - get all vector stores
                    logger.debug("[list_vector_stores] Building query with no filters")
                    query = text("""
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
                    result = session.execute(query, {"limit": ctx.req.limit or 100})
                    logger.debug("[list_vector_stores] Executed query with no filters")

                rows = result.fetchall()
                logger.debug(f"[list_vector_stores] Fetched {len(rows)} rows from database")

                vector_stores = []
                for row in rows:
                    vector_stores.append(VectorStoreModel(
                        vector_store_id=row[0],
                        event_id=row[1],
                        event_name=row[2],
                        vector_store_provider=row[3],
                        vector_store_db_name=row[4],
                        vector_store_db_link=row[5],
                        status=row[6] or 'pending',
                        is_active=bool(row[7]),
                        created_at=self._format_datetime(row[8]),
                        updated_at=self._format_datetime(row[9]),
                        files_count=row[10] or 0
                    ))

                ctx.set_resp(VectorStoresResp(
                    success=True,
                    vector_stores=vector_stores,
                    total_count=len(vector_stores)
                ))
                logger.info(f"[list_vector_stores] Success - returning {len(vector_stores)} vector stores")

        except Exception as e:
            logger.exception(f"[list_vector_stores] Exception occurred: {e}")
            ctx.set_resp(VectorStoresResp(
                success=False,
                message=f"Failed to fetch vector stores: {str(e)}"
            ))

        return ctx

    def get_vector_store(self, ctx: VectorStoresCtx, vector_store_id: int) -> VectorStoresCtx:
        """Get a specific vector store by ID."""
        try:
            with self.db.session_scope() as session:
                query = text("""
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
                    WHERE vs.vector_store_id = :vector_store_id
                    GROUP BY vs.vector_store_id
                """)
                result = session.execute(query, {"vector_store_id": vector_store_id})
                row = result.fetchone()

                if not row:
                    ctx.set_resp(VectorStoresResp(
                        success=False,
                        message="Vector store not found"
                    ))
                    return ctx

                vector_store = VectorStoreModel(
                    vector_store_id=row[0],
                    event_id=row[1],
                    event_name=row[2],
                    vector_store_provider=row[3],
                    vector_store_db_name=row[4],
                    vector_store_db_link=row[5],
                    status=row[6] or 'pending',
                    is_active=bool(row[7]),
                    created_at=self._format_datetime(row[8]),
                    updated_at=self._format_datetime(row[9]),
                    files_count=row[10] or 0
                )

                ctx.set_resp(VectorStoresResp(
                    success=True,
                    vector_store=vector_store
                ))

        except Exception as e:
            ctx.set_resp(VectorStoresResp(
                success=False,
                message=f"Failed to fetch vector store: {str(e)}"
            ))

        return ctx

    def create_vector_store(self, ctx: VectorStoresCtx, data: dict) -> VectorStoresCtx:
        """Create a new vector store."""
        try:
            with self.db.session_scope() as session:
                query = text("""
                    INSERT INTO event_vector_stores 
                    (event_id, credential_id, vector_store_provider, vector_store_db_name, vector_store_db_link, vector_config_json, status)
                    VALUES (:event_id, :credential_id, :provider, :db_name, :db_link, :config, 'pending')
                """)
                session.execute(query, {
                    "event_id": data.get("event_id"),
                    "credential_id": data.get("credential_id"),
                    "provider": data.get("vector_store_provider"),
                    "db_name": data.get("vector_store_db_name"),
                    "db_link": data.get("vector_store_db_link"),
                    "config": data.get("vector_config_json")
                })
                session.commit()

                # Get the created record
                result = session.execute(text("SELECT last_insert_rowid()"))
                new_id = result.fetchone()[0]

                ctx.set_resp(VectorStoresResp(
                    success=True,
                    message="Vector store created successfully",
                    vector_store=VectorStoreModel(
                        vector_store_id=new_id,
                        event_id=data.get("event_id"),
                        vector_store_provider=data.get("vector_store_provider"),
                        vector_store_db_name=data.get("vector_store_db_name"),
                        vector_store_db_link=data.get("vector_store_db_link"),
                        status='pending',
                        is_active=True,
                        files_count=0
                    )
                ))

        except Exception as e:
            ctx.set_resp(VectorStoresResp(
                success=False,
                message=f"Failed to create vector store: {str(e)}"
            ))

        return ctx

    def update_vector_store(self, ctx: VectorStoresCtx, vector_store_id: int, data: dict) -> VectorStoresCtx:
        """Update an existing vector store."""
        try:
            with self.db.session_scope() as session:
                # Build dynamic update query
                updates = []
                params = {"vector_store_id": vector_store_id}

                if data.get("vector_store_provider") is not None:
                    updates.append("vector_store_provider = :provider")
                    params["provider"] = data["vector_store_provider"]
                if data.get("vector_store_db_name") is not None:
                    updates.append("vector_store_db_name = :db_name")
                    params["db_name"] = data["vector_store_db_name"]
                if data.get("vector_store_db_link") is not None:
                    updates.append("vector_store_db_link = :db_link")
                    params["db_link"] = data["vector_store_db_link"]
                if data.get("status") is not None:
                    updates.append("status = :status")
                    params["status"] = data["status"]
                if data.get("is_active") is not None:
                    updates.append("is_active = :is_active")
                    params["is_active"] = data["is_active"]

                if not updates:
                    ctx.set_resp(VectorStoresResp(
                        success=False,
                        message="No fields to update"
                    ))
                    return ctx

                updates.append("updated_at = CURRENT_TIMESTAMP")
                query = text(f"UPDATE event_vector_stores SET {', '.join(updates)} WHERE vector_store_id = :vector_store_id")
                session.execute(query, params)
                session.commit()

                # Get updated record
                return self.get_vector_store(ctx, vector_store_id)

        except Exception as e:
            ctx.set_resp(VectorStoresResp(
                success=False,
                message=f"Failed to update vector store: {str(e)}"
            ))

        return ctx

    def delete_vector_store(self, ctx: VectorStoresCtx, vector_store_id: int) -> VectorStoresCtx:
        """Delete a vector store."""
        try:
            with self.db.session_scope() as session:
                query = text("DELETE FROM event_vector_stores WHERE vector_store_id = :vector_store_id")
                result = session.execute(query, {"vector_store_id": vector_store_id})
                session.commit()

                if result.rowcount == 0:
                    ctx.set_resp(VectorStoresResp(
                        success=False,
                        message="Vector store not found"
                    ))
                else:
                    ctx.set_resp(VectorStoresResp(
                        success=True,
                        message="Vector store deleted successfully"
                    ))

        except Exception as e:
            ctx.set_resp(VectorStoresResp(
                success=False,
                message=f"Failed to delete vector store: {str(e)}"
            ))

        return ctx

    def _format_datetime(self, dt) -> Optional[str]:
        """Format datetime to string."""
        if not dt:
            return None
        if isinstance(dt, str):
            return dt
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class VectorStoresServiceSingleton:
    """Singleton wrapper for VectorStoresService."""

    _instance = None

    def __new__(cls, db_manager=None):
        if cls._instance is None:
            if db_manager is None:
                raise ValueError("db_manager required for first instantiation")
            cls._instance = VectorStoresService(db_manager)
        return cls._instance

    @classmethod
    def reset(cls):
        """Reset singleton instance (useful for testing)."""
        cls._instance = None
