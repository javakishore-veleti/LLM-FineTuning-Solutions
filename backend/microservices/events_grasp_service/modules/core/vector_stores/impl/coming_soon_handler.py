"""Generic handler for providers that are coming soon."""
from typing import Dict, Any, Optional
from ..base import BaseVectorStoreConfigHandler
from ..providers import VectorStoreProviderType, PROVIDER_METADATA


class ComingSoonConfigHandler(BaseVectorStoreConfigHandler):
    """Generic configuration handler for providers that are not yet implemented."""

    def __init__(self, provider_type: str):
        self._provider_type = provider_type

    @property
    def provider_type(self) -> str:
        return self._provider_type

    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Coming soon providers cannot be configured."""
        return False, f"Provider '{self._provider_type}' is coming soon and not yet available for configuration"

    def get_config_schema(self) -> Dict[str, Any]:
        """Return minimal schema with coming soon message."""
        metadata = PROVIDER_METADATA.get(VectorStoreProviderType(self._provider_type), {})
        provider_name = metadata.get("name", self._provider_type)

        return {
            "coming_soon": True,
            "provider_name": provider_name,
            "message": f"{provider_name} integration is coming soon! We're working hard to bring you this feature.",
            "fields": []
        }

    def test_connection(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Coming soon providers cannot be tested."""
        return False, "This provider is not yet available"
