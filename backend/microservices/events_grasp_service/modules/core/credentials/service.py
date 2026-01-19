"""Credentials service for managing provider credentials."""
import logging
import json
from typing import Optional, List, Dict, Any
from sqlalchemy import text

from .providers import (
    CredentialProviderType,
    get_credential_providers,
    get_provider_auth_types,
    is_credential_provider_available,
    CREDENTIAL_PROVIDER_METADATA
)
from .schemas import get_credential_schema

logger = logging.getLogger(__name__)


class CredentialsService:
    """Service for managing credentials."""

    def __init__(self, db_manager):
        self.db = db_manager

    def list_credentials(self, customer_id: int, provider_type: Optional[str] = None) -> Dict[str, Any]:
        """List all credentials for a customer, optionally filtered by provider."""
        try:
            with self.db.session_scope() as session:
                if provider_type:
                    query = text("""
                        SELECT credential_id, customer_id, credential_name, provider_type, 
                               auth_type, description, is_active, created_at, updated_at
                        FROM credentials
                        WHERE customer_id = :customer_id AND provider_type = :provider_type AND is_active = 1
                        ORDER BY created_at DESC
                    """)
                    result = session.execute(query, {
                        "customer_id": customer_id,
                        "provider_type": provider_type
                    })
                else:
                    query = text("""
                        SELECT credential_id, customer_id, credential_name, provider_type, 
                               auth_type, description, is_active, created_at, updated_at
                        FROM credentials
                        WHERE customer_id = :customer_id AND is_active = 1
                        ORDER BY provider_type, created_at DESC
                    """)
                    result = session.execute(query, {"customer_id": customer_id})

                rows = result.fetchall()
                credentials = []
                for row in rows:
                    provider_meta = CREDENTIAL_PROVIDER_METADATA.get(
                        CredentialProviderType(row[3]) if row[3] in [e.value for e in CredentialProviderType] else None,
                        {}
                    )
                    credentials.append({
                        "credential_id": row[0],
                        "customer_id": row[1],
                        "credential_name": row[2],
                        "provider_type": row[3],
                        "provider_name": provider_meta.get("name", row[3]),
                        "provider_icon": provider_meta.get("icon", "default"),
                        "auth_type": row[4],
                        "description": row[5],
                        "is_active": bool(row[6]),
                        "created_at": str(row[7]) if row[7] else None,
                        "updated_at": str(row[8]) if row[8] else None
                    })

                return {
                    "success": True,
                    "credentials": credentials,
                    "total_count": len(credentials)
                }

        except Exception as e:
            logger.exception(f"[CredentialsService] Error listing credentials: {e}")
            return {
                "success": False,
                "message": f"Failed to list credentials: {str(e)}",
                "credentials": []
            }

    def get_credential(self, credential_id: int, customer_id: int) -> Dict[str, Any]:
        """Get a specific credential by ID."""
        try:
            with self.db.session_scope() as session:
                query = text("""
                    SELECT credential_id, customer_id, credential_name, provider_type, 
                           auth_type, credential_config_json, description, is_active, 
                           created_at, updated_at
                    FROM credentials
                    WHERE credential_id = :credential_id AND customer_id = :customer_id
                """)
                result = session.execute(query, {
                    "credential_id": credential_id,
                    "customer_id": customer_id
                })
                row = result.fetchone()

                if not row:
                    return {
                        "success": False,
                        "message": "Credential not found"
                    }

                # Don't return the actual config for security - return masked version
                config = json.loads(row[5]) if row[5] else {}
                masked_config = self._mask_sensitive_fields(config, row[3], row[4])

                provider_meta = CREDENTIAL_PROVIDER_METADATA.get(
                    CredentialProviderType(row[3]) if row[3] in [e.value for e in CredentialProviderType] else None,
                    {}
                )

                return {
                    "success": True,
                    "credential": {
                        "credential_id": row[0],
                        "customer_id": row[1],
                        "credential_name": row[2],
                        "provider_type": row[3],
                        "provider_name": provider_meta.get("name", row[3]),
                        "auth_type": row[4],
                        "config": masked_config,
                        "description": row[6],
                        "is_active": bool(row[7]),
                        "created_at": str(row[8]) if row[8] else None,
                        "updated_at": str(row[9]) if row[9] else None
                    }
                }

        except Exception as e:
            logger.exception(f"[CredentialsService] Error getting credential: {e}")
            return {
                "success": False,
                "message": f"Failed to get credential: {str(e)}"
            }

    def create_credential(self, customer_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new credential."""
        try:
            provider_type = data.get("provider_type")
            auth_type = data.get("auth_type")

            # Validate provider
            if not is_credential_provider_available(provider_type):
                return {
                    "success": False,
                    "message": f"Provider '{provider_type}' is not available"
                }

            with self.db.session_scope() as session:
                # Check for duplicate name
                check_query = text("""
                    SELECT COUNT(*) FROM credentials 
                    WHERE customer_id = :customer_id AND credential_name = :name
                """)
                result = session.execute(check_query, {
                    "customer_id": customer_id,
                    "name": data.get("credential_name")
                })
                if result.fetchone()[0] > 0:
                    return {
                        "success": False,
                        "message": "A credential with this name already exists"
                    }

                # Insert credential
                config_json = json.dumps(data.get("config", {}))
                query = text("""
                    INSERT INTO credentials 
                    (customer_id, credential_name, provider_type, auth_type, 
                     credential_config_json, description)
                    VALUES (:customer_id, :name, :provider_type, :auth_type, :config, :description)
                """)
                session.execute(query, {
                    "customer_id": customer_id,
                    "name": data.get("credential_name"),
                    "provider_type": provider_type,
                    "auth_type": auth_type,
                    "config": config_json,
                    "description": data.get("description", "")
                })
                session.commit()

                # Get the created ID
                result = session.execute(text("SELECT last_insert_rowid()"))
                new_id = result.fetchone()[0]

                logger.info(f"[CredentialsService] Created credential {new_id} for customer {customer_id}")

                return {
                    "success": True,
                    "message": "Credential created successfully",
                    "credential_id": new_id
                }

        except Exception as e:
            logger.exception(f"[CredentialsService] Error creating credential: {e}")
            return {
                "success": False,
                "message": f"Failed to create credential: {str(e)}"
            }

    def update_credential(self, credential_id: int, customer_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing credential."""
        try:
            with self.db.session_scope() as session:
                updates = []
                params = {"credential_id": credential_id, "customer_id": customer_id}

                if data.get("credential_name"):
                    updates.append("credential_name = :name")
                    params["name"] = data["credential_name"]
                if data.get("description") is not None:
                    updates.append("description = :description")
                    params["description"] = data["description"]
                if data.get("config"):
                    updates.append("credential_config_json = :config")
                    params["config"] = json.dumps(data["config"])
                if data.get("is_active") is not None:
                    updates.append("is_active = :is_active")
                    params["is_active"] = data["is_active"]

                updates.append("updated_at = CURRENT_TIMESTAMP")

                if not updates:
                    return {"success": False, "message": "No fields to update"}

                query = text(f"""
                    UPDATE credentials 
                    SET {', '.join(updates)}
                    WHERE credential_id = :credential_id AND customer_id = :customer_id
                """)
                result = session.execute(query, params)
                session.commit()

                if result.rowcount == 0:
                    return {"success": False, "message": "Credential not found"}

                return {"success": True, "message": "Credential updated successfully"}

        except Exception as e:
            logger.exception(f"[CredentialsService] Error updating credential: {e}")
            return {
                "success": False,
                "message": f"Failed to update credential: {str(e)}"
            }

    def delete_credential(self, credential_id: int, customer_id: int) -> Dict[str, Any]:
        """Delete a credential (soft delete by setting is_active = 0)."""
        try:
            with self.db.session_scope() as session:
                query = text("""
                    UPDATE credentials 
                    SET is_active = 0, updated_at = CURRENT_TIMESTAMP
                    WHERE credential_id = :credential_id AND customer_id = :customer_id
                """)
                result = session.execute(query, {
                    "credential_id": credential_id,
                    "customer_id": customer_id
                })
                session.commit()

                if result.rowcount == 0:
                    return {"success": False, "message": "Credential not found"}

                return {"success": True, "message": "Credential deleted successfully"}

        except Exception as e:
            logger.exception(f"[CredentialsService] Error deleting credential: {e}")
            return {
                "success": False,
                "message": f"Failed to delete credential: {str(e)}"
            }

    def get_credentials_for_provider(self, customer_id: int, provider_type: str) -> List[Dict[str, Any]]:
        """Get credentials that can be used with a specific vector store provider."""
        # Map vector store providers to credential providers
        provider_mapping = {
            "aws_opensearch": ["aws"],
            "aws_aurora_pgvector": ["aws", "pgvector"],
            "mongodb_atlas": ["mongodb"],
            "neo4j": ["neo4j"],
            "elasticsearch": ["elasticsearch", "aws"],
            "redis": ["redis", "aws"],
            "pgvector": ["pgvector"],
            "pinecone": ["pinecone"],
            "openai": ["openai"],
        }

        compatible_providers = provider_mapping.get(provider_type, [provider_type])

        result = self.list_credentials(customer_id)
        if not result["success"]:
            return []

        return [
            cred for cred in result["credentials"]
            if cred["provider_type"] in compatible_providers
        ]

    def _mask_sensitive_fields(self, config: Dict[str, Any], provider_type: str, auth_type: str) -> Dict[str, Any]:
        """Mask sensitive fields in the config for display."""
        schema = get_credential_schema(provider_type, auth_type)
        sensitive_fields = [
            f["name"] for f in schema.get("fields", [])
            if f.get("type") in ["password", "textarea"]
        ]

        masked = {}
        for key, value in config.items():
            if key in sensitive_fields and value:
                masked[key] = "********"
            else:
                masked[key] = value
        return masked


# Singleton instance
_credentials_service: Optional[CredentialsService] = None


def get_credentials_service(db_manager) -> CredentialsService:
    """Get the CredentialsService instance."""
    global _credentials_service
    if _credentials_service is None:
        _credentials_service = CredentialsService(db_manager)
    return _credentials_service
