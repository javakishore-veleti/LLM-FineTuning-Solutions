"""Neo4j Vector Store Configuration Handler."""
from typing import Dict, Any, Optional
from ..base import BaseVectorStoreConfigHandler
from ..providers import VectorStoreProviderType


class Neo4jConfigHandler(BaseVectorStoreConfigHandler):
    """Configuration handler for Neo4j with vector support."""

    @property
    def provider_type(self) -> str:
        return VectorStoreProviderType.NEO4J.value

    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate Neo4j configuration."""
        required_fields = ['index_name']

        for field in required_fields:
            if not config.get(field):
                return False, f"Missing required field: {field}"

        # Validate dimension if provided
        dimension = config.get('dimension')
        if dimension and (not isinstance(dimension, int) or dimension < 1 or dimension > 4096):
            return False, "Dimension must be an integer between 1 and 4096"

        return True, None

    def get_config_schema(self) -> Dict[str, Any]:
        """Get Neo4j configuration schema."""
        return {
            "fields": [
                {
                    "name": "database",
                    "label": "Database Name",
                    "type": "text",
                    "required": False,
                    "default": "neo4j",
                    "description": "Database name (default: neo4j)"
                },
                {
                    "name": "index_name",
                    "label": "Vector Index Name",
                    "type": "text",
                    "required": True,
                    "placeholder": "document_embeddings",
                    "description": "Name of the vector index"
                },
                {
                    "name": "node_label",
                    "label": "Node Label",
                    "type": "text",
                    "required": False,
                    "default": "Document",
                    "description": "Label for nodes containing embeddings"
                },
                {
                    "name": "embedding_property",
                    "label": "Embedding Property",
                    "type": "text",
                    "required": False,
                    "default": "embedding",
                    "description": "Property name for storing embeddings"
                },
                {
                    "name": "text_property",
                    "label": "Text Property",
                    "type": "text",
                    "required": False,
                    "default": "text",
                    "description": "Property name for storing source text"
                },
                {
                    "name": "dimension",
                    "label": "Vector Dimension",
                    "type": "number",
                    "required": True,
                    "default": 1536,
                    "min": 1,
                    "max": 4096,
                    "description": "Dimension of the embedding vectors"
                },
                {
                    "name": "similarity_function",
                    "label": "Similarity Function",
                    "type": "select",
                    "required": False,
                    "options": [
                        {"value": "cosine", "label": "Cosine Similarity"},
                        {"value": "euclidean", "label": "Euclidean Distance"},
                    ],
                    "default": "cosine",
                    "description": "Similarity function for vector search"
                },
                {
                    "name": "enable_graph_rag",
                    "label": "Enable Graph RAG",
                    "type": "checkbox",
                    "required": False,
                    "default": True,
                    "description": "Enable graph-based retrieval augmented generation"
                },
                {
                    "name": "relationship_types",
                    "label": "Relationship Types",
                    "type": "text",
                    "required": False,
                    "placeholder": "RELATED_TO,REFERENCES,CONTAINS",
                    "description": "Comma-separated relationship types for Graph RAG traversal",
                    "showIf": {"enable_graph_rag": True}
                },
                {
                    "name": "max_depth",
                    "label": "Max Traversal Depth",
                    "type": "number",
                    "required": False,
                    "default": 2,
                    "min": 1,
                    "max": 5,
                    "description": "Maximum depth for graph traversal in RAG",
                    "showIf": {"enable_graph_rag": True}
                }
            ]
        }

    def test_connection(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Test connection to Neo4j."""
        # TODO: Implement actual connection test using neo4j driver
        return True, "Connection test successful (simulated)"
