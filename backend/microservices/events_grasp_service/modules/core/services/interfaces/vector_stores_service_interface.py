"""Vector Stores service interface."""
from abc import ABC, abstractmethod
from ..dtos.vector_stores import VectorStoresCtx


class IVectorStoresService(ABC):
    """Interface for vector stores service operations."""

    @abstractmethod
    def list_vector_stores(self, ctx: VectorStoresCtx) -> VectorStoresCtx:
        """
        Get all vector stores, optionally filtered by event.

        Args:
            ctx: Context with request data containing optional event_id

        Returns:
            VectorStoresCtx with response containing list of vector stores
        """
        pass

    @abstractmethod
    def get_vector_store(self, ctx: VectorStoresCtx, vector_store_id: int) -> VectorStoresCtx:
        """
        Get a specific vector store by ID.

        Args:
            ctx: Context with request data
            vector_store_id: The vector store ID

        Returns:
            VectorStoresCtx with response containing the vector store
        """
        pass

    @abstractmethod
    def create_vector_store(self, ctx: VectorStoresCtx, data: dict) -> VectorStoresCtx:
        """
        Create a new vector store.

        Args:
            ctx: Context with request data
            data: Vector store data

        Returns:
            VectorStoresCtx with response containing the created vector store
        """
        pass

    @abstractmethod
    def update_vector_store(self, ctx: VectorStoresCtx, vector_store_id: int, data: dict) -> VectorStoresCtx:
        """
        Update an existing vector store.

        Args:
            ctx: Context with request data
            vector_store_id: The vector store ID
            data: Updated vector store data

        Returns:
            VectorStoresCtx with response containing the updated vector store
        """
        pass

    @abstractmethod
    def delete_vector_store(self, ctx: VectorStoresCtx, vector_store_id: int) -> VectorStoresCtx:
        """
        Delete a vector store.

        Args:
            ctx: Context with request data
            vector_store_id: The vector store ID

        Returns:
            VectorStoresCtx with response indicating success/failure
        """
        pass
