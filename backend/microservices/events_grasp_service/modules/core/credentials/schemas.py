"""Credential configuration schemas for each provider."""
from typing import Dict, Any, List


def get_aws_basic_schema() -> Dict[str, Any]:
    """AWS Basic (Access Key) authentication schema."""
    return {
        "fields": [
            {
                "name": "access_key_id",
                "label": "AWS Access Key ID",
                "type": "text",
                "required": True,
                "placeholder": "AKIAIOSFODNN7EXAMPLE",
                "description": "Your AWS Access Key ID"
            },
            {
                "name": "secret_access_key",
                "label": "AWS Secret Access Key",
                "type": "password",
                "required": True,
                "placeholder": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                "description": "Your AWS Secret Access Key"
            },
            {
                "name": "region",
                "label": "Default Region",
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
                "description": "Default AWS region"
            }
        ]
    }


def get_aws_iam_role_schema() -> Dict[str, Any]:
    """AWS IAM Role authentication schema."""
    return {
        "fields": [
            {
                "name": "role_arn",
                "label": "IAM Role ARN",
                "type": "text",
                "required": True,
                "placeholder": "arn:aws:iam::123456789012:role/MyRole",
                "description": "The ARN of the IAM role to assume"
            },
            {
                "name": "external_id",
                "label": "External ID",
                "type": "text",
                "required": False,
                "placeholder": "Optional external ID",
                "description": "External ID for cross-account role assumption (optional)"
            },
            {
                "name": "region",
                "label": "Default Region",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "us-east-1", "label": "US East (N. Virginia)"},
                    {"value": "us-east-2", "label": "US East (Ohio)"},
                    {"value": "us-west-1", "label": "US West (N. California)"},
                    {"value": "us-west-2", "label": "US West (Oregon)"},
                    {"value": "eu-west-1", "label": "Europe (Ireland)"},
                    {"value": "eu-central-1", "label": "Europe (Frankfurt)"},
                ],
                "description": "Default AWS region"
            }
        ]
    }


def get_aws_profile_schema() -> Dict[str, Any]:
    """AWS Profile authentication schema."""
    return {
        "fields": [
            {
                "name": "profile_name",
                "label": "AWS Profile Name",
                "type": "text",
                "required": True,
                "placeholder": "default",
                "description": "Profile name from ~/.aws/credentials"
            },
            {
                "name": "region",
                "label": "Default Region",
                "type": "select",
                "required": False,
                "options": [
                    {"value": "us-east-1", "label": "US East (N. Virginia)"},
                    {"value": "us-east-2", "label": "US East (Ohio)"},
                    {"value": "us-west-2", "label": "US West (Oregon)"},
                    {"value": "eu-west-1", "label": "Europe (Ireland)"},
                ],
                "description": "Override region (uses profile default if not set)"
            }
        ]
    }


def get_azure_service_principal_schema() -> Dict[str, Any]:
    """Azure Service Principal authentication schema."""
    return {
        "fields": [
            {
                "name": "tenant_id",
                "label": "Tenant ID",
                "type": "text",
                "required": True,
                "placeholder": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "description": "Azure AD Tenant ID"
            },
            {
                "name": "client_id",
                "label": "Client ID (App ID)",
                "type": "text",
                "required": True,
                "placeholder": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "description": "Application (client) ID"
            },
            {
                "name": "client_secret",
                "label": "Client Secret",
                "type": "password",
                "required": True,
                "description": "Client secret value"
            },
            {
                "name": "subscription_id",
                "label": "Subscription ID",
                "type": "text",
                "required": False,
                "placeholder": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "description": "Azure Subscription ID (optional)"
            }
        ]
    }


def get_azure_connection_string_schema() -> Dict[str, Any]:
    """Azure Connection String authentication schema."""
    return {
        "fields": [
            {
                "name": "connection_string",
                "label": "Connection String",
                "type": "password",
                "required": True,
                "placeholder": "DefaultEndpointsProtocol=https;AccountName=...",
                "description": "Azure service connection string"
            }
        ]
    }


def get_gcp_service_account_schema() -> Dict[str, Any]:
    """GCP Service Account authentication schema."""
    return {
        "fields": [
            {
                "name": "service_account_json",
                "label": "Service Account JSON",
                "type": "textarea",
                "required": True,
                "placeholder": '{"type": "service_account", "project_id": "...", ...}',
                "description": "Paste the contents of your service account JSON key file"
            },
            {
                "name": "project_id",
                "label": "Project ID",
                "type": "text",
                "required": False,
                "placeholder": "my-gcp-project",
                "description": "Override project ID (uses key file default if not set)"
            }
        ]
    }


def get_neo4j_basic_schema() -> Dict[str, Any]:
    """Neo4j basic authentication schema."""
    return {
        "fields": [
            {
                "name": "uri",
                "label": "Connection URI",
                "type": "text",
                "required": True,
                "placeholder": "neo4j+s://xxxxx.databases.neo4j.io",
                "description": "Neo4j connection URI"
            },
            {
                "name": "username",
                "label": "Username",
                "type": "text",
                "required": True,
                "default": "neo4j",
                "description": "Database username"
            },
            {
                "name": "password",
                "label": "Password",
                "type": "password",
                "required": True,
                "description": "Database password"
            }
        ]
    }


def get_elasticsearch_basic_schema() -> Dict[str, Any]:
    """Elasticsearch basic authentication schema."""
    return {
        "fields": [
            {
                "name": "host",
                "label": "Host URL",
                "type": "text",
                "required": True,
                "placeholder": "https://my-cluster.es.amazonaws.com",
                "description": "Elasticsearch cluster URL"
            },
            {
                "name": "username",
                "label": "Username",
                "type": "text",
                "required": True,
                "description": "Elasticsearch username"
            },
            {
                "name": "password",
                "label": "Password",
                "type": "password",
                "required": True,
                "description": "Elasticsearch password"
            }
        ]
    }


def get_elasticsearch_api_key_schema() -> Dict[str, Any]:
    """Elasticsearch API Key authentication schema."""
    return {
        "fields": [
            {
                "name": "host",
                "label": "Host URL",
                "type": "text",
                "required": True,
                "placeholder": "https://my-cluster.es.amazonaws.com",
                "description": "Elasticsearch cluster URL"
            },
            {
                "name": "api_key",
                "label": "API Key",
                "type": "password",
                "required": True,
                "description": "Elasticsearch API Key"
            }
        ]
    }


def get_redis_password_schema() -> Dict[str, Any]:
    """Redis password authentication schema."""
    return {
        "fields": [
            {
                "name": "host",
                "label": "Host",
                "type": "text",
                "required": True,
                "placeholder": "localhost",
                "description": "Redis host"
            },
            {
                "name": "port",
                "label": "Port",
                "type": "number",
                "required": True,
                "default": 6379,
                "description": "Redis port"
            },
            {
                "name": "password",
                "label": "Password",
                "type": "password",
                "required": False,
                "description": "Redis password (if required)"
            },
            {
                "name": "ssl",
                "label": "Use SSL/TLS",
                "type": "checkbox",
                "required": False,
                "default": False,
                "description": "Enable SSL/TLS connection"
            }
        ]
    }


def get_pgvector_basic_schema() -> Dict[str, Any]:
    """PostgreSQL (pgvector) basic authentication schema."""
    return {
        "fields": [
            {
                "name": "host",
                "label": "Host",
                "type": "text",
                "required": True,
                "placeholder": "localhost",
                "description": "PostgreSQL host"
            },
            {
                "name": "port",
                "label": "Port",
                "type": "number",
                "required": True,
                "default": 5432,
                "description": "PostgreSQL port"
            },
            {
                "name": "database",
                "label": "Database",
                "type": "text",
                "required": True,
                "placeholder": "postgres",
                "description": "Database name"
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
                "name": "ssl_mode",
                "label": "SSL Mode",
                "type": "select",
                "required": False,
                "options": [
                    {"value": "disable", "label": "Disable"},
                    {"value": "require", "label": "Require"},
                    {"value": "verify-ca", "label": "Verify CA"},
                    {"value": "verify-full", "label": "Verify Full"},
                ],
                "default": "require",
                "description": "SSL connection mode"
            }
        ]
    }


def get_mongodb_connection_string_schema() -> Dict[str, Any]:
    """MongoDB connection string authentication schema."""
    return {
        "fields": [
            {
                "name": "connection_string",
                "label": "Connection String",
                "type": "password",
                "required": True,
                "placeholder": "mongodb+srv://user:pass@cluster.mongodb.net/",
                "description": "MongoDB connection string (includes credentials)"
            }
        ]
    }


def get_mongodb_basic_schema() -> Dict[str, Any]:
    """MongoDB basic authentication schema."""
    return {
        "fields": [
            {
                "name": "host",
                "label": "Host",
                "type": "text",
                "required": True,
                "placeholder": "cluster.mongodb.net",
                "description": "MongoDB host"
            },
            {
                "name": "port",
                "label": "Port",
                "type": "number",
                "required": False,
                "default": 27017,
                "description": "MongoDB port"
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
                "name": "auth_database",
                "label": "Auth Database",
                "type": "text",
                "required": False,
                "default": "admin",
                "description": "Authentication database"
            }
        ]
    }


def get_pinecone_api_key_schema() -> Dict[str, Any]:
    """Pinecone API Key authentication schema."""
    return {
        "fields": [
            {
                "name": "api_key",
                "label": "API Key",
                "type": "password",
                "required": True,
                "description": "Pinecone API Key"
            },
            {
                "name": "environment",
                "label": "Environment",
                "type": "text",
                "required": True,
                "placeholder": "us-west1-gcp",
                "description": "Pinecone environment"
            }
        ]
    }


# Schema mapping
CREDENTIAL_SCHEMAS: Dict[str, Dict[str, Any]] = {
    # AWS
    "aws:basic": get_aws_basic_schema(),
    "aws:iam_role": get_aws_iam_role_schema(),
    "aws:profile": get_aws_profile_schema(),
    # Azure
    "azure:service_principal": get_azure_service_principal_schema(),
    "azure:managed_identity": {"fields": []},  # No config needed
    "azure:connection_string": get_azure_connection_string_schema(),
    # GCP
    "gcp:service_account": get_gcp_service_account_schema(),
    "gcp:application_default": {"fields": []},  # No config needed
    # Neo4j
    "neo4j:basic": get_neo4j_basic_schema(),
    # Elasticsearch
    "elasticsearch:basic": get_elasticsearch_basic_schema(),
    "elasticsearch:api_key": get_elasticsearch_api_key_schema(),
    # Redis
    "redis:password": get_redis_password_schema(),
    "redis:acl": get_redis_password_schema(),  # Same schema, different usage
    # pgvector
    "pgvector:basic": get_pgvector_basic_schema(),
    # MongoDB
    "mongodb:connection_string": get_mongodb_connection_string_schema(),
    "mongodb:basic": get_mongodb_basic_schema(),
    # Pinecone
    "pinecone:api_key": get_pinecone_api_key_schema(),
}


def get_credential_schema(provider_type: str, auth_type: str) -> Dict[str, Any]:
    """Get the credential configuration schema for a provider and auth type."""
    key = f"{provider_type}:{auth_type}"
    return CREDENTIAL_SCHEMAS.get(key, {"fields": []})
