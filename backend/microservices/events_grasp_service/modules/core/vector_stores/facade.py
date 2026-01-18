"""Vector Store Configuration Facade - routes to appropriate handler based on provider."""
import logging
from typing import Dict, Any, Optional, Type
from .base import IVectorStoreConfigHandler
from .providers import (
    VectorStoreProviderType,
    ProviderStatus,
    PROVIDER_METADATA,
    get_available_providers,
    is_provider_available
)
from .impl.aws_handlers import AWSOpenSearchConfigHandler, AWSAuroraPgVectorConfigHandler
from .impl.mongodb_handler import MongoDBAtlasConfigHandler
from .impl.neo4j_handler import Neo4jConfigHandler
from .impl.coming_soon_handler import ComingSoonConfigHandler

logger = logging.getLogger(__name__)


class VectorStoreConfigFacade:
    """
    Facade for vector store configuration management.
    Routes operations to the appropriate provider-specific handler.
    """

    # Registry of available handlers
    _handlers: Dict[str, Type[IVectorStoreConfigHandler]] = {
        VectorStoreProviderType.AWS_OPENSEARCH.value: AWSOpenSearchConfigHandler,
        VectorStoreProviderType.AWS_AURORA_PGVECTOR.value: AWSAuroraPgVectorConfigHandler,
        VectorStoreProviderType.MONGODB_ATLAS.value: MongoDBAtlasConfigHandler,
        VectorStoreProviderType.NEO4J.value: Neo4jConfigHandler,
    }

    _handler_instances: Dict[str, IVectorStoreConfigHandler] = {}

    @classmethod
    def get_handler(cls, provider_type: str) -> IVectorStoreConfigHandler:
        """
        Get the appropriate handler for a provider type.
        Returns ComingSoonConfigHandler for unimplemented providers.
        """
        # Return cached instance if available
        if provider_type in cls._handler_instances:
            return cls._handler_instances[provider_type]

        # Create new instance
        if provider_type in cls._handlers:
            handler = cls._handlers[provider_type]()
        else:
            # Use ComingSoonConfigHandler for unimplemented providers
            handler = ComingSoonConfigHandler(provider_type)

        cls._handler_instances[provider_type] = handler
        return handler

    @classmethod
    def get_all_providers(cls) -> list:
        """Get all available providers with their metadata."""
        return get_available_providers()

    @classmethod
    def get_provider_categories(cls) -> Dict[str, list]:
        """Get providers grouped by category."""
        categories = {}
        for provider_data in get_available_providers():
            category = provider_data.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append(provider_data)
        return categories

    @classmethod
    def get_config_schema(cls, provider_type: str) -> Dict[str, Any]:
        """Get the configuration schema for a provider."""
        handler = cls.get_handler(provider_type)
        schema = handler.get_config_schema()

        # Add provider metadata
        try:
            provider_enum = VectorStoreProviderType(provider_type)
            metadata = PROVIDER_METADATA.get(provider_enum, {})
            schema["provider_type"] = provider_type
            schema["provider_name"] = metadata.get("name", provider_type)
            schema["provider_description"] = metadata.get("description", "")
            schema["provider_status"] = metadata.get("status", ProviderStatus.COMING_SOON).value
            schema["provider_category"] = metadata.get("category", "Other")
        except ValueError:
            schema["provider_type"] = provider_type
            schema["provider_status"] = ProviderStatus.COMING_SOON.value

        return schema

    @classmethod
    def validate_config(cls, provider_type: str, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate configuration for a provider.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not is_provider_available(provider_type):
            return False, f"Provider '{provider_type}' is not yet available"

        handler = cls.get_handler(provider_type)
        return handler.validate_config(config)

    @classmethod
    def to_storage_format(cls, provider_type: str, config: Dict[str, Any]) -> str:
        """Convert UI configuration to storage format (JSON string)."""
        handler = cls.get_handler(provider_type)
        return handler.to_storage_format(config)

    @classmethod
    def from_storage_format(cls, provider_type: str, json_config: str) -> Dict[str, Any]:
        """Convert stored configuration to UI format."""
        handler = cls.get_handler(provider_type)
        return handler.from_storage_format(json_config)

    @classmethod
    def test_connection(cls, provider_type: str, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Test connection to a vector store.

        Returns:
            Tuple of (success, message)
        """
        if not is_provider_available(provider_type):
            return False, f"Provider '{provider_type}' is not yet available"

        handler = cls.get_handler(provider_type)

        # First validate the config
        is_valid, error = handler.validate_config(config)
        if not is_valid:
            return False, f"Invalid configuration: {error}"

        # Then test connection
        return handler.test_connection(config)

    @classmethod
    def create_vector_store_config(
        cls,
        provider_type: str,
        display_name: str,
        config: Dict[str, Any]
    ) -> tuple[bool, Dict[str, Any], Optional[str]]:
        """
        Create a new vector store configuration.

        Args:
            provider_type: The provider type
            display_name: Display name for the vector store
            config: Provider-specific configuration

        Returns:
            Tuple of (success, result_data, error_message)
        """
        # Validate provider is available
        if not is_provider_available(provider_type):
            return False, {}, f"Provider '{provider_type}' is not yet available"

        # Validate configuration
        is_valid, error = cls.validate_config(provider_type, config)
        if not is_valid:
            return False, {}, error

        # Convert to storage format
        json_config = cls.to_storage_format(provider_type, config)

        result = {
            "provider_type": provider_type,
            "display_name": display_name,
            "config_json": json_config
        }

        logger.info(f"[VectorStoreFacade] Created config for provider: {provider_type}")
        return True, result, None
