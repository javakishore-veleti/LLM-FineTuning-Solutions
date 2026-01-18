"""Authentication module initialization."""
from .customer_cache import CustomerCache, get_customer_cache
from .middleware import (
    AuthenticatedCustomer,
    get_current_customer,
    get_optional_customer,
    validate_customer,
    require_customer_id
)

__all__ = [
    'CustomerCache',
    'get_customer_cache',
    'AuthenticatedCustomer',
    'get_current_customer',
    'get_optional_customer',
    'validate_customer',
    'require_customer_id'
]
