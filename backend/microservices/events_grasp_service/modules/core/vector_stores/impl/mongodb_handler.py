"""MongoDB Vector Store Configuration Handler."""
from typing import Dict, Any, Optional
from ..base import BaseVectorStoreConfigHandler
from ..providers import VectorStoreProviderType


class MongoDBAtlasConfigHandler(BaseVectorStoreConfigHandler):
    """Configuration handler for MongoDB Atlas Vector Search."""

    @property
    def provider_type(self) -> str:
        return VectorStoreProviderType.MONGODB_ATLAS.value

    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate MongoDB Atlas configuration."""
        required_fields = ['connection_string', 'database_name', 'collection_name', 'index_name']

        for field in required_fields:
            if not config.get(field):
                return False, f"Missing required field: {field}"

        # Validate connection string format
        conn_string = config.get('connection_string', '')
        if not conn_string.startswith('mongodb+srv://') and not conn_string.startswith('mongodb://'):
            return False, "Connection string must start with mongodb:// or mongodb+srv://"

        # Validate dimension if provided
        dimension = config.get('dimension')
        if dimension and (not isinstance(dimension, int) or dimension < 1 or dimension > 4096):
            return False, "Dimension must be an integer between 1 and 4096"

        return True, None

    def get_config_schema(self) -> Dict[str, Any]:
        """Get MongoDB Atlas configuration schema."""
        return {
            "fields": [
                {
                    "name": "connection_string",
                    "label": "Connection String",
                    "type": "password",
                    "required": True,
                    "placeholder": "mongodb+srv://username:password@cluster.xxxxx.mongodb.net/",
                    "description": "MongoDB Atlas connection string (includes credentials)"
                },
                {
                    "name": "database_name",
                    "label": "Database Name",
                    "type": "text",
                    "required": True,
                    "placeholder": "my_database",
                    "description": "Name of the database"
                },
                {
                    "name": "collection_name",
                    "label": "Collection Name",
                    "type": "text",
                    "required": True,
                    "placeholder": "embeddings",
                    "description": "Name of the collection to store vectors"
                },
                {
                    "name": "index_name",
                    "label": "Vector Search Index Name",
                    "type": "text",
                    "required": True,
                    "placeholder": "vector_index",
                    "description": "Name of the Atlas Vector Search index"
                },
                {
                    "name": "embedding_field",
                    "label": "Embedding Field Name",
                    "type": "text",
                    "required": False,
                    "default": "embedding",
                    "description": "Field name for storing embeddings"
                },
                {
                    "name": "text_field",
                    "label": "Text Field Name",
                    "type": "text",
                    "required": False,
                    "default": "text",
                    "description": "Field name for storing source text"
                },
                {
                    "name": "dimension",
                    "label": "Vector Dimension",
                    "type": "number",
                    "required": False,
                    "default": 1536,
                    "min": 1,
                    "max": 4096,
                    "description": "Dimension of the embedding vectors"
                },
                {
                    "name": "similarity_metric",
                    "label": "Similarity Metric",
                    "type": "select",
                    "required": False,
                    "options": [
                        {"value": "cosine", "label": "Cosine Similarity"},
                        {"value": "euclidean", "label": "Euclidean Distance"},
                        {"value": "dotProduct", "label": "Dot Product"},
                    ],
                    "default": "cosine",
                    "description": "Distance metric for vector similarity"
                },
                {
                    "name": "num_candidates",
                    "label": "Number of Candidates",
                    "type": "number",
                    "required": False,
                    "default": 100,
                    "min": 10,
                    "max": 10000,
                    "description": "Number of candidates to consider during search"
                }
            ]
        }

    def test_connection(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Test connection to MongoDB Atlas."""
        # TODO: Implement actual connection test using pymongo
        return True, "Connection test successful (simulated)"
