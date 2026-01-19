"""Credentials provider types and configurations."""
from enum import Enum
from typing import Dict, Any, List


class CredentialProviderType(str, Enum):
    """Supported credential provider types."""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    OPENAI = "openai"
    NEO4J = "neo4j"
    ELASTICSEARCH = "elasticsearch"
    REDIS = "redis"
    PGVECTOR = "pgvector"
    MONGODB = "mongodb"
    PINECONE = "pinecone"
    CUSTOM = "custom"


class AWSAuthType(str, Enum):
    """AWS authentication types."""
    BASIC = "basic"           # Access Key + Secret Key
    IAM_ROLE = "iam_role"     # IAM Role ARN
    PROFILE = "profile"       # AWS Profile Name (local development)


class AzureAuthType(str, Enum):
    """Azure authentication types."""
    SERVICE_PRINCIPAL = "service_principal"  # Client ID + Secret + Tenant
    MANAGED_IDENTITY = "managed_identity"    # Managed Identity
    CONNECTION_STRING = "connection_string"  # Connection String


class GCPAuthType(str, Enum):
    """GCP authentication types."""
    SERVICE_ACCOUNT = "service_account"  # Service Account JSON
    APPLICATION_DEFAULT = "application_default"  # ADC


class ProviderStatus(str, Enum):
    """Provider implementation status."""
    AVAILABLE = "available"
    COMING_SOON = "coming_soon"


# Provider metadata
CREDENTIAL_PROVIDER_METADATA: Dict[str, Dict[str, Any]] = {
    CredentialProviderType.AWS: {
        "name": "Amazon Web Services (AWS)",
        "icon": "aws",
        "status": ProviderStatus.AVAILABLE,
        "description": "AWS credentials for OpenSearch, Aurora, S3, and other AWS services",
        "auth_types": [
            {"value": AWSAuthType.BASIC.value, "label": "Access Key & Secret", "description": "Use AWS Access Key ID and Secret Access Key"},
            {"value": AWSAuthType.IAM_ROLE.value, "label": "IAM Role", "description": "Assume an IAM Role (for EC2, Lambda, ECS)"},
            {"value": AWSAuthType.PROFILE.value, "label": "AWS Profile", "description": "Use named profile from ~/.aws/credentials (local dev)"},
            {"value": "env_var", "label": "Environment Variables", "description": "Use AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY env vars"},
        ]
    },
    CredentialProviderType.AZURE: {
        "name": "Microsoft Azure",
        "icon": "azure",
        "status": ProviderStatus.AVAILABLE,
        "description": "Azure credentials for AI Search, Cosmos DB, and other Azure services",
        "auth_types": [
            {"value": AzureAuthType.SERVICE_PRINCIPAL.value, "label": "Service Principal", "description": "Client ID, Secret, and Tenant ID"},
            {"value": AzureAuthType.MANAGED_IDENTITY.value, "label": "Managed Identity", "description": "Azure Managed Identity (for Azure VMs, Functions)"},
            {"value": AzureAuthType.CONNECTION_STRING.value, "label": "Connection String", "description": "Service-specific connection string"},
            {"value": "env_var", "label": "Environment Variables", "description": "Use AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID env vars"},
        ]
    },
    CredentialProviderType.GCP: {
        "name": "Google Cloud Platform",
        "icon": "gcp",
        "status": ProviderStatus.AVAILABLE,
        "description": "GCP credentials for Vertex AI, Cloud SQL, and other GCP services",
        "auth_types": [
            {"value": GCPAuthType.SERVICE_ACCOUNT.value, "label": "Service Account Key", "description": "Upload service account JSON key file"},
            {"value": GCPAuthType.APPLICATION_DEFAULT.value, "label": "Application Default", "description": "Use Application Default Credentials (local dev)"},
            {"value": "env_var", "label": "Environment Variable", "description": "Use GOOGLE_APPLICATION_CREDENTIALS env var"},
        ]
    },
    CredentialProviderType.OPENAI: {
        "name": "OpenAI",
        "icon": "openai",
        "status": ProviderStatus.AVAILABLE,
        "description": "OpenAI API credentials for Vector Stores and Assistants",
        "auth_types": [
            {"value": "api_key", "label": "API Key", "description": "OpenAI API Key"},
            {"value": "env_var", "label": "Environment Variable", "description": "Use environment variable for API key"},
        ]
    },
    CredentialProviderType.NEO4J: {
        "name": "Neo4j",
        "icon": "neo4j",
        "status": ProviderStatus.AVAILABLE,
        "description": "Neo4j database credentials for graph vector store",
        "auth_types": [
            {"value": "basic", "label": "Username & Password", "description": "Neo4j username and password authentication"},
            {"value": "env_var", "label": "Environment Variables", "description": "Use NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD env vars"},
        ]
    },
    CredentialProviderType.ELASTICSEARCH: {
        "name": "Elasticsearch",
        "icon": "elasticsearch",
        "status": ProviderStatus.AVAILABLE,
        "description": "Elasticsearch/OpenSearch credentials",
        "auth_types": [
            {"value": "basic", "label": "Username & Password", "description": "Basic authentication"},
            {"value": "api_key", "label": "API Key", "description": "Elasticsearch API Key"},
            {"value": "env_var", "label": "Environment Variables", "description": "Use ELASTICSEARCH_URL, ELASTICSEARCH_API_KEY env vars"},
        ]
    },
    CredentialProviderType.REDIS: {
        "name": "Redis",
        "icon": "redis",
        "status": ProviderStatus.AVAILABLE,
        "description": "Redis credentials for in-memory vector store",
        "auth_types": [
            {"value": "password", "label": "Password", "description": "Redis password authentication"},
            {"value": "acl", "label": "ACL User", "description": "Redis ACL username and password"},
            {"value": "env_var", "label": "Environment Variables", "description": "Use REDIS_URL or REDIS_HOST, REDIS_PASSWORD env vars"},
        ]
    },
    CredentialProviderType.PGVECTOR: {
        "name": "PostgreSQL (pgvector)",
        "icon": "postgresql",
        "status": ProviderStatus.AVAILABLE,
        "description": "PostgreSQL database credentials for pgvector extension",
        "auth_types": [
            {"value": "basic", "label": "Username & Password", "description": "PostgreSQL username and password"},
            {"value": "env_var", "label": "Environment Variables", "description": "Use DATABASE_URL or PG_HOST, PG_USER, PG_PASSWORD env vars"},
        ]
    },
    CredentialProviderType.MONGODB: {
        "name": "MongoDB",
        "icon": "mongodb",
        "status": ProviderStatus.AVAILABLE,
        "description": "MongoDB Atlas credentials for vector search",
        "auth_types": [
            {"value": "connection_string", "label": "Connection String", "description": "MongoDB connection string with credentials"},
            {"value": "basic", "label": "Username & Password", "description": "MongoDB username and password"},
            {"value": "env_var", "label": "Environment Variables", "description": "Use MONGODB_URI env var"},
        ]
    },
    CredentialProviderType.PINECONE: {
        "name": "Pinecone",
        "icon": "pinecone",
        "status": ProviderStatus.AVAILABLE,
        "description": "Pinecone API credentials",
        "auth_types": [
            {"value": "api_key", "label": "API Key", "description": "Pinecone API Key"},
            {"value": "env_var", "label": "Environment Variables", "description": "Use PINECONE_API_KEY, PINECONE_ENVIRONMENT env vars"},
        ]
    },
    CredentialProviderType.CUSTOM: {
        "name": "Custom",
        "icon": "custom",
        "status": ProviderStatus.COMING_SOON,
        "description": "Custom credential configuration",
        "auth_types": []
    },
}


def get_credential_providers() -> List[Dict[str, Any]]:
    """Get all credential providers with metadata."""
    return [
        {
            "provider_type": provider.value,
            **metadata
        }
        for provider, metadata in CREDENTIAL_PROVIDER_METADATA.items()
    ]


def get_provider_auth_types(provider_type: str) -> List[Dict[str, Any]]:
    """Get authentication types for a provider."""
    try:
        provider = CredentialProviderType(provider_type)
        return CREDENTIAL_PROVIDER_METADATA.get(provider, {}).get("auth_types", [])
    except ValueError:
        return []


def is_credential_provider_available(provider_type: str) -> bool:
    """Check if a credential provider is available."""
    try:
        provider = CredentialProviderType(provider_type)
        status = CREDENTIAL_PROVIDER_METADATA.get(provider, {}).get("status", ProviderStatus.COMING_SOON)
        return status == ProviderStatus.AVAILABLE
    except ValueError:
        return False
