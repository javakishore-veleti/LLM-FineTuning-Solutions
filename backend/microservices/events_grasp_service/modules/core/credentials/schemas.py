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


def get_openai_api_key_schema() -> Dict[str, Any]:
    """OpenAI API Key authentication schema."""
    return {
        "fields": [
            {
                "name": "api_key",
                "label": "OpenAI API Key",
                "type": "password",
                "required": True,
                "placeholder": "sk-...",
                "description": "Your OpenAI API Key (starts with sk-)"
            },
            {
                "name": "organization_id",
                "label": "Organization ID",
                "type": "text",
                "required": False,
                "placeholder": "org-...",
                "description": "OpenAI Organization ID (optional)"
            }
        ]
    }


def get_openai_env_var_schema() -> Dict[str, Any]:
    """OpenAI environment variable authentication schema."""
    return {
        "fields": [
            {
                "name": "api_key_env_var",
                "label": "API Key Environment Variable",
                "type": "text",
                "required": True,
                "default": "OPENAI_API_KEY",
                "description": "Name of the environment variable containing OpenAI API key"
            },
            {
                "name": "org_id_env_var",
                "label": "Organization ID Environment Variable",
                "type": "text",
                "required": False,
                "placeholder": "OPENAI_ORG_ID",
                "description": "Name of the environment variable for Organization ID (optional)"
            }
        ]
    }


def get_aws_env_var_schema() -> Dict[str, Any]:
    """AWS environment variable authentication schema."""
    return {
        "fields": [
            {
                "name": "access_key_env_var",
                "label": "Access Key ID Environment Variable",
                "type": "text",
                "required": True,
                "default": "AWS_ACCESS_KEY_ID",
                "description": "Name of the environment variable containing AWS Access Key ID"
            },
            {
                "name": "secret_key_env_var",
                "label": "Secret Access Key Environment Variable",
                "type": "text",
                "required": True,
                "default": "AWS_SECRET_ACCESS_KEY",
                "description": "Name of the environment variable containing AWS Secret Access Key"
            },
            {
                "name": "region_env_var",
                "label": "Region Environment Variable",
                "type": "text",
                "required": False,
                "default": "AWS_REGION",
                "description": "Name of the environment variable for AWS region (optional)"
            }
        ]
    }


def get_azure_env_var_schema() -> Dict[str, Any]:
    """Azure environment variable authentication schema."""
    return {
        "fields": [
            {
                "name": "client_id_env_var",
                "label": "Client ID Environment Variable",
                "type": "text",
                "required": True,
                "default": "AZURE_CLIENT_ID",
                "description": "Name of the environment variable containing Azure Client ID"
            },
            {
                "name": "client_secret_env_var",
                "label": "Client Secret Environment Variable",
                "type": "text",
                "required": True,
                "default": "AZURE_CLIENT_SECRET",
                "description": "Name of the environment variable containing Azure Client Secret"
            },
            {
                "name": "tenant_id_env_var",
                "label": "Tenant ID Environment Variable",
                "type": "text",
                "required": True,
                "default": "AZURE_TENANT_ID",
                "description": "Name of the environment variable containing Azure Tenant ID"
            }
        ]
    }


def get_gcp_env_var_schema() -> Dict[str, Any]:
    """GCP environment variable authentication schema."""
    return {
        "fields": [
            {
                "name": "credentials_env_var",
                "label": "Credentials File Environment Variable",
                "type": "text",
                "required": True,
                "default": "GOOGLE_APPLICATION_CREDENTIALS",
                "description": "Name of the environment variable pointing to service account JSON file"
            },
            {
                "name": "project_id_env_var",
                "label": "Project ID Environment Variable",
                "type": "text",
                "required": False,
                "default": "GCP_PROJECT_ID",
                "description": "Name of the environment variable for GCP project ID (optional)"
            }
        ]
    }


def get_neo4j_env_var_schema() -> Dict[str, Any]:
    """Neo4j environment variable authentication schema."""
    return {
        "fields": [
            {
                "name": "uri_env_var",
                "label": "URI Environment Variable",
                "type": "text",
                "required": True,
                "default": "NEO4J_URI",
                "description": "Name of the environment variable containing Neo4j URI"
            },
            {
                "name": "username_env_var",
                "label": "Username Environment Variable",
                "type": "text",
                "required": True,
                "default": "NEO4J_USERNAME",
                "description": "Name of the environment variable containing Neo4j username"
            },
            {
                "name": "password_env_var",
                "label": "Password Environment Variable",
                "type": "text",
                "required": True,
                "default": "NEO4J_PASSWORD",
                "description": "Name of the environment variable containing Neo4j password"
            }
        ]
    }


def get_elasticsearch_env_var_schema() -> Dict[str, Any]:
    """Elasticsearch environment variable authentication schema."""
    return {
        "fields": [
            {
                "name": "url_env_var",
                "label": "URL Environment Variable",
                "type": "text",
                "required": True,
                "default": "ELASTICSEARCH_URL",
                "description": "Name of the environment variable containing Elasticsearch URL"
            },
            {
                "name": "api_key_env_var",
                "label": "API Key Environment Variable",
                "type": "text",
                "required": False,
                "default": "ELASTICSEARCH_API_KEY",
                "description": "Name of the environment variable for API key (if using API key auth)"
            }
        ]
    }


def get_redis_env_var_schema() -> Dict[str, Any]:
    """Redis environment variable authentication schema."""
    return {
        "fields": [
            {
                "name": "url_env_var",
                "label": "URL Environment Variable",
                "type": "text",
                "required": False,
                "default": "REDIS_URL",
                "description": "Name of the environment variable containing Redis URL (full connection string)"
            },
            {
                "name": "host_env_var",
                "label": "Host Environment Variable",
                "type": "text",
                "required": False,
                "default": "REDIS_HOST",
                "description": "Name of the environment variable for Redis host (if not using URL)"
            },
            {
                "name": "password_env_var",
                "label": "Password Environment Variable",
                "type": "text",
                "required": False,
                "default": "REDIS_PASSWORD",
                "description": "Name of the environment variable for Redis password"
            }
        ]
    }


def get_pgvector_env_var_schema() -> Dict[str, Any]:
    """PostgreSQL environment variable authentication schema."""
    return {
        "fields": [
            {
                "name": "database_url_env_var",
                "label": "Database URL Environment Variable",
                "type": "text",
                "required": False,
                "default": "DATABASE_URL",
                "description": "Name of the environment variable containing full database URL"
            },
            {
                "name": "host_env_var",
                "label": "Host Environment Variable",
                "type": "text",
                "required": False,
                "default": "PG_HOST",
                "description": "Name of the environment variable for PostgreSQL host"
            },
            {
                "name": "user_env_var",
                "label": "User Environment Variable",
                "type": "text",
                "required": False,
                "default": "PG_USER",
                "description": "Name of the environment variable for PostgreSQL user"
            },
            {
                "name": "password_env_var",
                "label": "Password Environment Variable",
                "type": "text",
                "required": False,
                "default": "PG_PASSWORD",
                "description": "Name of the environment variable for PostgreSQL password"
            }
        ]
    }


def get_mongodb_env_var_schema() -> Dict[str, Any]:
    """MongoDB environment variable authentication schema."""
    return {
        "fields": [
            {
                "name": "uri_env_var",
                "label": "URI Environment Variable",
                "type": "text",
                "required": True,
                "default": "MONGODB_URI",
                "description": "Name of the environment variable containing MongoDB connection URI"
            }
        ]
    }


def get_pinecone_env_var_schema() -> Dict[str, Any]:
    """Pinecone environment variable authentication schema."""
    return {
        "fields": [
            {
                "name": "api_key_env_var",
                "label": "API Key Environment Variable",
                "type": "text",
                "required": True,
                "default": "PINECONE_API_KEY",
                "description": "Name of the environment variable containing Pinecone API key"
            },
            {
                "name": "environment_env_var",
                "label": "Environment Variable for Pinecone Environment",
                "type": "text",
                "required": False,
                "default": "PINECONE_ENVIRONMENT",
                "description": "Name of the environment variable for Pinecone environment"
            }
        ]
    }


# Schema mapping
CREDENTIAL_SCHEMAS: Dict[str, Dict[str, Any]] = {
    # AWS
    "aws:basic": get_aws_basic_schema(),
    "aws:iam_role": get_aws_iam_role_schema(),
    "aws:profile": get_aws_profile_schema(),
    "aws:env_var": get_aws_env_var_schema(),
    # Azure
    "azure:service_principal": get_azure_service_principal_schema(),
    "azure:managed_identity": {"fields": []},  # No config needed
    "azure:connection_string": get_azure_connection_string_schema(),
    "azure:env_var": get_azure_env_var_schema(),
    # GCP
    "gcp:service_account": get_gcp_service_account_schema(),
    "gcp:application_default": {"fields": []},  # No config needed
    "gcp:env_var": get_gcp_env_var_schema(),
    # OpenAI
    "openai:api_key": get_openai_api_key_schema(),
    "openai:env_var": get_openai_env_var_schema(),
    # Neo4j
    "neo4j:basic": get_neo4j_basic_schema(),
    "neo4j:env_var": get_neo4j_env_var_schema(),
    # Elasticsearch
    "elasticsearch:basic": get_elasticsearch_basic_schema(),
    "elasticsearch:api_key": get_elasticsearch_api_key_schema(),
    "elasticsearch:env_var": get_elasticsearch_env_var_schema(),
    # Redis
    "redis:password": get_redis_password_schema(),
    "redis:acl": get_redis_password_schema(),  # Same schema, different usage
    "redis:env_var": get_redis_env_var_schema(),
    # pgvector
    "pgvector:basic": get_pgvector_basic_schema(),
    "pgvector:env_var": get_pgvector_env_var_schema(),
    # MongoDB
    "mongodb:connection_string": get_mongodb_connection_string_schema(),
    "mongodb:basic": get_mongodb_basic_schema(),
    "mongodb:env_var": get_mongodb_env_var_schema(),
    # Pinecone
    "pinecone:api_key": get_pinecone_api_key_schema(),
    "pinecone:env_var": get_pinecone_env_var_schema(),
}


def get_credential_schema(provider_type: str, auth_type: str) -> Dict[str, Any]:
    """Get the credential configuration schema for a provider and auth type."""
    key = f"{provider_type}:{auth_type}"
    return CREDENTIAL_SCHEMAS.get(key, {"fields": []})
