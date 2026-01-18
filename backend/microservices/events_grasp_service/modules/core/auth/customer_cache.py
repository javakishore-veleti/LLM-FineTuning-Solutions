"""Customer authentication cache with LRU eviction policy.

Uses in-memory cachetools by default, switches to Redis if configured.
"""
import logging
import os
from typing import Optional
import threading

logger = logging.getLogger(__name__)

# Cache TTL in seconds (1 hour)
CACHE_TTL_SECONDS = 3600

# Try to import Redis, but don't fail if not available
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    redis = None
    REDIS_AVAILABLE = False
    logger.info("Redis not installed - using in-memory cache")

# Import cachetools for in-memory LRU cache
from cachetools import TTLCache


class CustomerCache:
    """
    Customer authentication cache with LRU eviction policy.
    Uses in-memory TTLCache by default, Redis if configured.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self._redis_client: Optional[redis.Redis] = None
        self._memory_cache: TTLCache = TTLCache(maxsize=1000, ttl=CACHE_TTL_SECONDS)
        self._cache_lock = threading.Lock()

        # Check if Redis is configured
        redis_url = os.environ.get('REDIS_URL') or os.environ.get('REDIS_CACHE_URL')

        if redis_url and REDIS_AVAILABLE:
            try:
                self._redis_client = redis.from_url(redis_url, decode_responses=True)
                # Test connection
                self._redis_client.ping()
                logger.info(f"[CustomerCache] Connected to Redis cache")
            except Exception as e:
                logger.warning(f"[CustomerCache] Failed to connect to Redis: {e}. Using in-memory cache.")
                self._redis_client = None
        else:
            logger.info("[CustomerCache] Using in-memory TTL cache (Redis not configured)")

    def _get_cache_key(self, customer_id: int) -> str:
        """Generate cache key for customer ID."""
        return f"customer:valid:{customer_id}"

    def is_customer_valid(self, customer_id: int) -> Optional[bool]:
        """
        Check if customer ID is in cache and valid.

        Returns:
            True if customer is cached and valid
            False if customer is cached and invalid
            None if customer is not in cache (cache miss)
        """
        if customer_id is None:
            return False

        cache_key = self._get_cache_key(customer_id)

        # Try Redis first if available
        if self._redis_client:
            try:
                value = self._redis_client.get(cache_key)
                if value is not None:
                    logger.debug(f"[CustomerCache] Redis cache hit for customer {customer_id}")
                    return value == "1"
                logger.debug(f"[CustomerCache] Redis cache miss for customer {customer_id}")
                return None
            except Exception as e:
                logger.warning(f"[CustomerCache] Redis error: {e}. Falling back to memory cache.")

        # Fall back to memory cache
        with self._cache_lock:
            value = self._memory_cache.get(cache_key)
            if value is not None:
                logger.debug(f"[CustomerCache] Memory cache hit for customer {customer_id}")
                return value
            logger.debug(f"[CustomerCache] Memory cache miss for customer {customer_id}")
            return None

    def set_customer_valid(self, customer_id: int, is_valid: bool) -> None:
        """
        Cache customer validity status.

        Args:
            customer_id: The customer ID
            is_valid: Whether the customer is valid
        """
        if customer_id is None:
            return

        cache_key = self._get_cache_key(customer_id)

        # Try Redis first if available
        if self._redis_client:
            try:
                self._redis_client.setex(
                    cache_key,
                    CACHE_TTL_SECONDS,
                    "1" if is_valid else "0"
                )
                logger.debug(f"[CustomerCache] Cached customer {customer_id} in Redis (valid={is_valid})")
                return
            except Exception as e:
                logger.warning(f"[CustomerCache] Redis error: {e}. Falling back to memory cache.")

        # Fall back to memory cache
        with self._cache_lock:
            self._memory_cache[cache_key] = is_valid
            logger.debug(f"[CustomerCache] Cached customer {customer_id} in memory (valid={is_valid})")

    def invalidate_customer(self, customer_id: int) -> None:
        """
        Remove customer from cache (e.g., on logout or account changes).

        Args:
            customer_id: The customer ID to invalidate
        """
        if customer_id is None:
            return

        cache_key = self._get_cache_key(customer_id)

        # Try Redis first if available
        if self._redis_client:
            try:
                self._redis_client.delete(cache_key)
                logger.debug(f"[CustomerCache] Invalidated customer {customer_id} in Redis")
            except Exception as e:
                logger.warning(f"[CustomerCache] Redis error on invalidate: {e}")

        # Also invalidate in memory cache
        with self._cache_lock:
            self._memory_cache.pop(cache_key, None)
            logger.debug(f"[CustomerCache] Invalidated customer {customer_id} in memory")

    def clear_all(self) -> None:
        """Clear all cached customer data."""
        if self._redis_client:
            try:
                # Delete all customer keys
                keys = self._redis_client.keys("customer:valid:*")
                if keys:
                    self._redis_client.delete(*keys)
                logger.info("[CustomerCache] Cleared all Redis cache entries")
            except Exception as e:
                logger.warning(f"[CustomerCache] Redis error on clear: {e}")

        with self._cache_lock:
            self._memory_cache.clear()
            logger.info("[CustomerCache] Cleared all memory cache entries")

    def get_stats(self) -> dict:
        """Get cache statistics."""
        stats = {
            "backend": "redis" if self._redis_client else "memory",
            "memory_cache_size": len(self._memory_cache),
            "memory_cache_maxsize": self._memory_cache.maxsize,
            "ttl_seconds": CACHE_TTL_SECONDS
        }

        if self._redis_client:
            try:
                keys = self._redis_client.keys("customer:valid:*")
                stats["redis_cache_size"] = len(keys)
            except Exception:
                stats["redis_cache_size"] = "unknown"

        return stats


# Singleton instance
_customer_cache: Optional[CustomerCache] = None


def get_customer_cache() -> CustomerCache:
    """Get the singleton CustomerCache instance."""
    global _customer_cache
    if _customer_cache is None:
        _customer_cache = CustomerCache()
    return _customer_cache
