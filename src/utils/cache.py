import time
from typing import Any, Dict, Optional

class Cache:
    def __init__(self, ttl: int = 60):
        """
        Initialize the cache with a time-to-live (TTL) in seconds.

        Args:
        ttl (int): The time-to-live in seconds. Defaults to 60.
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Args:
        key (str): The key to retrieve.

        Returns:
        Optional[Any]: The cached value or None if not found or expired.
        """
        if key in self.cache:
            value = self.cache[key]
            if time.time() - value["timestamp"] < self.ttl:
                return value["data"]
        return None

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache.

        Args:
        key (str): The key to store.
        value (Any): The value to store.
        """
        self.cache[key] = {"data": value, "timestamp": time.time()}

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache.

        Args:
        key (str): The key to delete.
        """
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> None:
        """
        Clear the entire cache.
        """
        self.cache.clear()

def get_cache() -> Cache:
    """
    Get the global cache instance.

    Returns:
    Cache: The global cache instance.
    """
    return Cache()

def cache_api_response(ttl: int = 60):
    """
    Decorator to cache API responses.

    Args:
    ttl (int): The time-to-live in seconds. Defaults to 60.
    """
    cache = get_cache()

    def decorator(func):
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached_response = cache.get(key)
            if cached_response is not None:
                return cached_response
            response = func(*args, **kwargs)
            cache.set(key, response)
            return response
        return wrapper
    return decorator

# Example usage:
cache = get_cache()

@cache_api_response(ttl=30)
def example_api_call():
    # Simulate an API call
    time.sleep(1)
    return {"data": "Example API response"}

print(example_api_call())  # Cache miss
print(example_api_call())  # Cache hit