"""Base interface for vector store configuration handlers."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json


class VectorStoreConfigBase(BaseModel):
    """Base configuration model for all vector stores."""
    provider_type: str
    display_name: str
    description: Optional[str] = None

    class Config:
        extra = "allow"  # Allow additional fields for provider-specific configs


class IVectorStoreConfigHandler(ABC):
    """Interface for vector store configuration handlers."""

    @property
    @abstractmethod
    def provider_type(self) -> str:
        """Return the provider type this handler supports."""
        pass

    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate the configuration.

        Args:
            config: Configuration dictionary from UI

        Returns:
            Tuple of (is_valid, error_message)
        """
        pass

    @abstractmethod
    def to_storage_format(self, config: Dict[str, Any]) -> str:
        """
        Convert UI configuration to JSON storage format.

        Args:
            config: Configuration dictionary from UI

        Returns:
            JSON string for database storage
        """
        pass

    @abstractmethod
    def from_storage_format(self, json_config: str) -> Dict[str, Any]:
        """
        Convert stored JSON configuration to UI format.

        Args:
            json_config: JSON string from database

        Returns:
            Configuration dictionary for UI
        """
        pass

    @abstractmethod
    def get_config_schema(self) -> Dict[str, Any]:
        """
        Get the configuration schema for UI rendering.

        Returns:
            Schema describing all configuration fields
        """
        pass

    @abstractmethod
    def test_connection(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Test connection to the vector store.

        Args:
            config: Configuration dictionary

        Returns:
            Tuple of (success, message)
        """
        pass


class BaseVectorStoreConfigHandler(IVectorStoreConfigHandler):
    """Base implementation with common functionality."""

    def to_storage_format(self, config: Dict[str, Any]) -> str:
        """Default implementation - serialize to JSON."""
        # Remove any sensitive data markers and prepare for storage
        storage_config = {
            "provider_type": self.provider_type,
            **config
        }
        return json.dumps(storage_config)

    def from_storage_format(self, json_config: str) -> Dict[str, Any]:
        """Default implementation - deserialize from JSON."""
        if not json_config:
            return {}
        try:
            return json.loads(json_config)
        except json.JSONDecodeError:
            return {}

    def test_connection(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Default implementation - always returns success (override in subclasses)."""
        return True, "Connection test not implemented for this provider"
