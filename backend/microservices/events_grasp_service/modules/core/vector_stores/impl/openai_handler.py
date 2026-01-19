"""OpenAI Vector Stores Configuration Handler."""
from typing import Dict, Any, Optional
from ..base import BaseVectorStoreConfigHandler
from ..providers import VectorStoreProviderType


class OpenAIVectorStoresConfigHandler(BaseVectorStoreConfigHandler):
    """Configuration handler for OpenAI Vector Stores (Assistants API)."""

    @property
    def provider_type(self) -> str:
        return VectorStoreProviderType.OPENAI.value

    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate OpenAI Vector Stores configuration."""
        required_fields = ['vector_store_name']

        for field in required_fields:
            if not config.get(field):
                return False, f"Missing required field: {field}"

        # Validate chunking strategy if provided
        chunking_strategy = config.get('chunking_strategy', 'auto')
        if chunking_strategy not in ['auto', 'static']:
            return False, "Chunking strategy must be 'auto' or 'static'"

        # Validate chunk size if static chunking
        if chunking_strategy == 'static':
            max_tokens = config.get('max_chunk_size_tokens')
            if max_tokens and (not isinstance(max_tokens, int) or max_tokens < 100 or max_tokens > 4096):
                return False, "Max chunk size must be between 100 and 4096 tokens"

            overlap = config.get('chunk_overlap_tokens')
            if overlap and (not isinstance(overlap, int) or overlap < 0 or overlap > 400):
                return False, "Chunk overlap must be between 0 and 400 tokens"

        # Validate expiration days if provided
        expires_after_days = config.get('expires_after_days')
        if expires_after_days and (not isinstance(expires_after_days, int) or expires_after_days < 1 or expires_after_days > 365):
            return False, "Expiration days must be between 1 and 365"

        return True, None

    def get_config_schema(self) -> Dict[str, Any]:
        """Get OpenAI Vector Stores configuration schema."""
        return {
            "fields": [
                {
                    "name": "vector_store_name",
                    "label": "Vector Store Name",
                    "type": "text",
                    "required": True,
                    "placeholder": "my-event-knowledge-base",
                    "description": "Name for the OpenAI Vector Store"
                },
                {
                    "name": "chunking_strategy",
                    "label": "Chunking Strategy",
                    "type": "select",
                    "required": False,
                    "options": [
                        {"value": "auto", "label": "Auto (Recommended)"},
                        {"value": "static", "label": "Static (Custom sizes)"},
                    ],
                    "default": "auto",
                    "description": "How to split documents into chunks for embedding"
                },
                {
                    "name": "max_chunk_size_tokens",
                    "label": "Max Chunk Size (tokens)",
                    "type": "number",
                    "required": False,
                    "default": 800,
                    "min": 100,
                    "max": 4096,
                    "description": "Maximum tokens per chunk (only for static chunking)",
                    "showIf": {"chunking_strategy": "static"}
                },
                {
                    "name": "chunk_overlap_tokens",
                    "label": "Chunk Overlap (tokens)",
                    "type": "number",
                    "required": False,
                    "default": 400,
                    "min": 0,
                    "max": 400,
                    "description": "Token overlap between chunks (only for static chunking)",
                    "showIf": {"chunking_strategy": "static"}
                },
                {
                    "name": "expires_after_days",
                    "label": "Expires After (days)",
                    "type": "number",
                    "required": False,
                    "min": 1,
                    "max": 365,
                    "description": "Auto-delete after this many days of inactivity (leave empty for no expiration)"
                },
                {
                    "name": "metadata_tags",
                    "label": "Metadata Tags",
                    "type": "text",
                    "required": False,
                    "placeholder": "event:conference,year:2026",
                    "description": "Comma-separated key:value pairs for metadata"
                }
            ]
        }

    def test_connection(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Test connection to OpenAI API."""
        # This would use the credential's API key to test
        # For now, return simulated success
        return True, "OpenAI API connection test successful (simulated)"

    def create_config(self, display_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create the final configuration for storage."""
        import json

        final_config = {
            "vector_store_name": config.get("vector_store_name", display_name),
            "chunking_strategy": config.get("chunking_strategy", "auto"),
        }

        # Add static chunking params if applicable
        if final_config["chunking_strategy"] == "static":
            final_config["max_chunk_size_tokens"] = config.get("max_chunk_size_tokens", 800)
            final_config["chunk_overlap_tokens"] = config.get("chunk_overlap_tokens", 400)

        # Add optional fields if provided
        if config.get("expires_after_days"):
            final_config["expires_after_days"] = config["expires_after_days"]

        if config.get("metadata_tags"):
            # Parse comma-separated key:value pairs
            tags = {}
            for pair in config["metadata_tags"].split(","):
                if ":" in pair:
                    key, value = pair.strip().split(":", 1)
                    tags[key.strip()] = value.strip()
            final_config["metadata"] = tags

        return {
            "display_name": display_name,
            "config_json": json.dumps(final_config)
        }
