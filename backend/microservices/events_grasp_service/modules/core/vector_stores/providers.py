"""Vector Store Provider types and configurations."""
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel


class VectorStoreProviderType(str, Enum):
    """Supported vector store provider types."""
    # AWS Native
    AWS_OPENSEARCH = "aws_opensearch"
    AWS_AURORA_PGVECTOR = "aws_aurora_pgvector"
    AWS_S3_VECTORS = "aws_s3_vectors"
    AWS_MEMORYDB = "aws_memorydb"
    AWS_NEPTUNE = "aws_neptune"
    AWS_DOCUMENTDB = "aws_documentdb"

    # MongoDB
    MONGODB_ATLAS = "mongodb_atlas"

    # Neo4j
    NEO4J = "neo4j"

    # Open Source / Self-Hosted
    MILVUS = "milvus"
    CHROMA = "chroma"
    QDRANT = "qdrant"
    WEAVIATE = "weaviate"
    FAISS = "faiss"
    PGVECTOR = "pgvector"
    REDIS = "redis"
    VESPA = "vespa"

    # Cloud Managed
    PINECONE = "pinecone"
    ELASTICSEARCH = "elasticsearch"

    # Azure
    AZURE_AI_SEARCH = "azure_ai_search"
    AZURE_COSMOS_DB = "azure_cosmos_db"

    # Google Cloud
    GCP_VERTEX_AI = "gcp_vertex_ai"
    GCP_ALLOYDB = "gcp_alloydb"


class ProviderStatus(str, Enum):
    """Provider implementation status."""
    AVAILABLE = "available"
    COMING_SOON = "coming_soon"
    BETA = "beta"


# Provider metadata and status
PROVIDER_METADATA: Dict[str, Dict[str, Any]] = {
    # AWS - Available
    VectorStoreProviderType.AWS_OPENSEARCH: {
        "name": "Amazon OpenSearch Service",
        "category": "AWS Native",
        "status": ProviderStatus.AVAILABLE,
        "description": "Scalable, high-performance vector search with built-in k-NN capabilities",
        "icon": "aws"
    },
    VectorStoreProviderType.AWS_AURORA_PGVECTOR: {
        "name": "Amazon Aurora PostgreSQL (pgvector)",
        "category": "AWS Native",
        "status": ProviderStatus.AVAILABLE,
        "description": "PostgreSQL with pgvector extension for vector similarity search",
        "icon": "aws"
    },
    VectorStoreProviderType.AWS_S3_VECTORS: {
        "name": "Amazon S3 Vectors",
        "category": "AWS Native",
        "status": ProviderStatus.COMING_SOON,
        "description": "Cost-optimized vector storage for large datasets",
        "icon": "aws"
    },
    VectorStoreProviderType.AWS_MEMORYDB: {
        "name": "Amazon MemoryDB (Redis)",
        "category": "AWS Native",
        "status": ProviderStatus.COMING_SOON,
        "description": "In-memory, low-latency vector search",
        "icon": "aws"
    },
    VectorStoreProviderType.AWS_NEPTUNE: {
        "name": "Amazon Neptune Analytics",
        "category": "AWS Native",
        "status": ProviderStatus.COMING_SOON,
        "description": "Graph-based data with vector search",
        "icon": "aws"
    },
    VectorStoreProviderType.AWS_DOCUMENTDB: {
        "name": "Amazon DocumentDB",
        "category": "AWS Native",
        "status": ProviderStatus.COMING_SOON,
        "description": "MongoDB-compatible document database with vector search",
        "icon": "aws"
    },

    # MongoDB - Available
    VectorStoreProviderType.MONGODB_ATLAS: {
        "name": "MongoDB Atlas Vector Search",
        "category": "Managed Cloud",
        "status": ProviderStatus.AVAILABLE,
        "description": "Integrated vector search in MongoDB Atlas",
        "icon": "mongodb"
    },

    # Neo4j - Available
    VectorStoreProviderType.NEO4J: {
        "name": "Neo4j",
        "category": "Graph Database",
        "status": ProviderStatus.AVAILABLE,
        "description": "Graph database with native vector support for Graph RAG",
        "icon": "neo4j"
    },

    # Open Source - Coming Soon
    VectorStoreProviderType.MILVUS: {
        "name": "Milvus",
        "category": "Open Source",
        "status": ProviderStatus.COMING_SOON,
        "description": "Highly scalable open-source vector database",
        "icon": "milvus"
    },
    VectorStoreProviderType.CHROMA: {
        "name": "Chroma",
        "category": "Open Source",
        "status": ProviderStatus.COMING_SOON,
        "description": "Popular for LLM app development, easy local setup",
        "icon": "chroma"
    },
    VectorStoreProviderType.QDRANT: {
        "name": "Qdrant",
        "category": "Open Source",
        "status": ProviderStatus.COMING_SOON,
        "description": "High-performance vector search written in Rust",
        "icon": "qdrant"
    },
    VectorStoreProviderType.WEAVIATE: {
        "name": "Weaviate",
        "category": "Open Source",
        "status": ProviderStatus.COMING_SOON,
        "description": "Cloud-native with semantic search and graph features",
        "icon": "weaviate"
    },
    VectorStoreProviderType.FAISS: {
        "name": "FAISS",
        "category": "Open Source",
        "status": ProviderStatus.COMING_SOON,
        "description": "Facebook AI library for efficient similarity search",
        "icon": "faiss"
    },
    VectorStoreProviderType.PGVECTOR: {
        "name": "pgvector (PostgreSQL)",
        "category": "Database Extension",
        "status": ProviderStatus.COMING_SOON,
        "description": "Vector search extension for PostgreSQL",
        "icon": "postgresql"
    },
    VectorStoreProviderType.REDIS: {
        "name": "Redis",
        "category": "In-Memory",
        "status": ProviderStatus.COMING_SOON,
        "description": "In-memory data store with vector capabilities",
        "icon": "redis"
    },
    VectorStoreProviderType.VESPA: {
        "name": "Vespa",
        "category": "Open Source",
        "status": ProviderStatus.COMING_SOON,
        "description": "Open-source serving engine for large-scale AI",
        "icon": "vespa"
    },
    VectorStoreProviderType.PINECONE: {
        "name": "Pinecone",
        "category": "Managed Cloud",
        "status": ProviderStatus.COMING_SOON,
        "description": "Fully managed, high-performance vector database",
        "icon": "pinecone"
    },
    VectorStoreProviderType.ELASTICSEARCH: {
        "name": "Elasticsearch",
        "category": "Search Engine",
        "status": ProviderStatus.COMING_SOON,
        "description": "Hybrid text and vector search capabilities",
        "icon": "elasticsearch"
    },

    # Azure - Coming Soon
    VectorStoreProviderType.AZURE_AI_SEARCH: {
        "name": "Azure AI Search",
        "category": "Azure",
        "status": ProviderStatus.COMING_SOON,
        "description": "Managed service with built-in vector search",
        "icon": "azure"
    },
    VectorStoreProviderType.AZURE_COSMOS_DB: {
        "name": "Azure Cosmos DB",
        "category": "Azure",
        "status": ProviderStatus.COMING_SOON,
        "description": "NoSQL with integrated vector database",
        "icon": "azure"
    },

    # GCP - Coming Soon
    VectorStoreProviderType.GCP_VERTEX_AI: {
        "name": "Vertex AI Vector Search",
        "category": "Google Cloud",
        "status": ProviderStatus.COMING_SOON,
        "description": "Highly scalable ANN search service",
        "icon": "gcp"
    },
    VectorStoreProviderType.GCP_ALLOYDB: {
        "name": "AlloyDB with pgvector",
        "category": "Google Cloud",
        "status": ProviderStatus.COMING_SOON,
        "description": "Enhanced PostgreSQL with vector search",
        "icon": "gcp"
    },
}


def get_available_providers() -> list:
    """Get list of all providers with their metadata."""
    return [
        {
            "provider_type": provider.value,
            **metadata
        }
        for provider, metadata in PROVIDER_METADATA.items()
    ]


def get_provider_status(provider_type: str) -> ProviderStatus:
    """Get the implementation status of a provider."""
    try:
        provider = VectorStoreProviderType(provider_type)
        return PROVIDER_METADATA.get(provider, {}).get("status", ProviderStatus.COMING_SOON)
    except ValueError:
        return ProviderStatus.COMING_SOON


def is_provider_available(provider_type: str) -> bool:
    """Check if a provider is available for use."""
    status = get_provider_status(provider_type)
    return status in [ProviderStatus.AVAILABLE, ProviderStatus.BETA]
