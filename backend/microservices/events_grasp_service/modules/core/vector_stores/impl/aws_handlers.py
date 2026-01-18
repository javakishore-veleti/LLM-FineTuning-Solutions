"""AWS Vector Store Configuration Handlers."""
from typing import Dict, Any, Optional
import json
from ..base import BaseVectorStoreConfigHandler
from ..providers import VectorStoreProviderType


class AWSOpenSearchConfigHandler(BaseVectorStoreConfigHandler):
    """Configuration handler for Amazon OpenSearch Service."""

    @property
    def provider_type(self) -> str:
        return VectorStoreProviderType.AWS_OPENSEARCH.value

    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate OpenSearch configuration."""
        required_fields = ['endpoint', 'index_name', 'region']

        for field in required_fields:
            if not config.get(field):
                return False, f"Missing required field: {field}"

        # Validate endpoint format
        endpoint = config.get('endpoint', '')
        if not endpoint.startswith('https://'):
            return False, "Endpoint must start with https://"

        # Validate region format
        region = config.get('region', '')
        if not region or len(region) < 5:
            return False, "Invalid AWS region"

        # Validate dimension if provided
        dimension = config.get('dimension')
        if dimension and (not isinstance(dimension, int) or dimension < 1 or dimension > 10000):
            return False, "Dimension must be an integer between 1 and 10000"

        return True, None

    def get_config_schema(self) -> Dict[str, Any]:
        """Get OpenSearch configuration schema."""
        return {
            "fields": [
                {
                    "name": "endpoint",
                    "label": "OpenSearch Endpoint",
                    "type": "text",
                    "required": True,
                    "placeholder": "https://your-domain.region.es.amazonaws.com",
                    "description": "The OpenSearch domain endpoint URL"
                },
                {
                    "name": "index_name",
                    "label": "Index Name",
                    "type": "text",
                    "required": True,
                    "placeholder": "my-vector-index",
                    "description": "Name of the vector index"
                },
                {
                    "name": "region",
                    "label": "AWS Region",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": "us-east-1", "label": "US East (N. Virginia)"},
                        {"value": "us-east-2", "label": "US East (Ohio)"},
                        {"value": "us-west-1", "label": "US West (N. California)"},
                        {"value": "us-west-2", "label": "US West (Oregon)"},
                        {"value": "eu-west-1", "label": "Europe (Ireland)"},
                        {"value": "eu-west-2", "label": "Europe (London)"},
                        {"value": "eu-central-1", "label": "Europe (Frankfurt)"},
                        {"value": "ap-south-1", "label": "Asia Pacific (Mumbai)"},
                        {"value": "ap-southeast-1", "label": "Asia Pacific (Singapore)"},
                        {"value": "ap-southeast-2", "label": "Asia Pacific (Sydney)"},
                        {"value": "ap-northeast-1", "label": "Asia Pacific (Tokyo)"},
                    ],
                    "description": "AWS region where OpenSearch is deployed"
                },
                {
                    "name": "dimension",
                    "label": "Vector Dimension",
                    "type": "number",
                    "required": False,
                    "default": 1536,
                    "min": 1,
                    "max": 10000,
                    "description": "Dimension of the embedding vectors (e.g., 1536 for OpenAI ada-002)"
                },
                {
                    "name": "auth_type",
                    "label": "Authentication Type",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": "iam", "label": "IAM Role"},
                        {"value": "basic", "label": "Basic Auth"},
                    ],
                    "default": "iam",
                    "description": "Authentication method for OpenSearch"
                },
                {
                    "name": "access_key_id",
                    "label": "AWS Access Key ID",
                    "type": "password",
                    "required": False,
                    "description": "AWS Access Key (leave empty to use IAM role)",
                    "showIf": {"auth_type": "basic"}
                },
                {
                    "name": "secret_access_key",
                    "label": "AWS Secret Access Key",
                    "type": "password",
                    "required": False,
                    "description": "AWS Secret Key (leave empty to use IAM role)",
                    "showIf": {"auth_type": "basic"}
                },
                {
                    "name": "similarity_metric",
                    "label": "Similarity Metric",
                    "type": "select",
                    "required": False,
                    "options": [
                        {"value": "cosine", "label": "Cosine Similarity"},
                        {"value": "l2", "label": "Euclidean Distance (L2)"},
                        {"value": "dot_product", "label": "Dot Product"},
                    ],
                    "default": "cosine",
                    "description": "Distance metric for vector similarity"
                }
            ]
        }

    def test_connection(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Test connection to OpenSearch."""
        # TODO: Implement actual connection test
        return True, "Connection test successful (simulated)"


class AWSAuroraPgVectorConfigHandler(BaseVectorStoreConfigHandler):
    """Configuration handler for Amazon Aurora PostgreSQL with pgvector."""

    @property
    def provider_type(self) -> str:
        return VectorStoreProviderType.AWS_AURORA_PGVECTOR.value

    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate Aurora PostgreSQL configuration."""
        required_fields = ['host', 'port', 'database', 'username']

        for field in required_fields:
            if not config.get(field):
                return False, f"Missing required field: {field}"

        # Validate port
        port = config.get('port')
        if not isinstance(port, int) or port < 1 or port > 65535:
            return False, "Port must be a valid port number (1-65535)"

        return True, None

    def get_config_schema(self) -> Dict[str, Any]:
        """Get Aurora PostgreSQL configuration schema."""
        return {
            "fields": [
                {
                    "name": "host",
                    "label": "Host",
                    "type": "text",
                    "required": True,
                    "placeholder": "your-cluster.cluster-xxxxx.region.rds.amazonaws.com",
                    "description": "Aurora cluster endpoint"
                },
                {
                    "name": "port",
                    "label": "Port",
                    "type": "number",
                    "required": True,
                    "default": 5432,
                    "description": "PostgreSQL port (default: 5432)"
                },
                {
                    "name": "database",
                    "label": "Database Name",
                    "type": "text",
                    "required": True,
                    "placeholder": "vectordb",
                    "description": "Name of the database"
                },
                {
                    "name": "username",
                    "label": "Username",
                    "type": "text",
                    "required": True,
                    "description": "Database username"
                },
                {
                    "name": "password",
                    "label": "Password",
                    "type": "password",
                    "required": True,
                    "description": "Database password"
                },
                {
                    "name": "table_name",
                    "label": "Vector Table Name",
                    "type": "text",
                    "required": False,
                    "default": "embeddings",
                    "description": "Name of the table to store vectors"
                },
                {
                    "name": "dimension",
                    "label": "Vector Dimension",
                    "type": "number",
                    "required": False,
                    "default": 1536,
                    "min": 1,
                    "max": 16000,
                    "description": "Dimension of the embedding vectors"
                },
                {
                    "name": "ssl_mode",
                    "label": "SSL Mode",
                    "type": "select",
                    "required": False,
                    "options": [
                        {"value": "require", "label": "Require"},
                        {"value": "verify-ca", "label": "Verify CA"},
                        {"value": "verify-full", "label": "Verify Full"},
                        {"value": "disable", "label": "Disable"},
                    ],
                    "default": "require",
                    "description": "SSL connection mode"
                },
                {
                    "name": "index_type",
                    "label": "Index Type",
                    "type": "select",
                    "required": False,
                    "options": [
                        {"value": "hnsw", "label": "HNSW (recommended)"},
                        {"value": "ivfflat", "label": "IVFFlat"},
                    ],
                    "default": "hnsw",
                    "description": "Vector index type for similarity search"
                }
            ]
        }

    def test_connection(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Test connection to Aurora PostgreSQL."""
        # TODO: Implement actual connection test
        return True, "Connection test successful (simulated)"
