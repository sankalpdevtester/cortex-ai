import time
from typing import Any, Dict, Optional

class Cache:
    def __init__(self, ttl: int = 60):
        """
        Initialize the cache with a TTL (time to live) in seconds.

        Args:
        ttl (int): The time to live for each cache entry in seconds. Defaults to 60.
        """
        self.ttl = ttl
        self.cache: Dict[str, Any] = {}
        self.expiration: Dict[str, float] = {}

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Args:
        key (str): The key to retrieve from the cache.

        Returns:
        Optional[Any]: The cached value if it exists and is not expired, otherwise None.
        """
        if key in self.cache:
            if time.time() < self.expiration[key]:
                return self.cache[key]
            else:
                del self.cache[key]
                del self.expiration[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache.

        Args:
        key (str): The key to store in the cache.
        value (Any): The value to store in the cache.
        """
        self.cache[key] = value
        self.expiration[key] = time.time() + self.ttl

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache.

        Args:
        key (str): The key to delete from the cache.
        """
        if key in self.cache:
            del self.cache[key]
            del self.expiration[key]

def get_cache() -> Cache:
    """
    Get the global cache instance.

    Returns:
    Cache: The global cache instance.
    """
    cache = Cache()
    return cache

# Example usage:
cache = get_cache()
cache.set("github_api_response", {"status": 200, "data": {"user": "john"}})
print(cache.get("github_api_response"))  # prints: {'status': 200, 'data': {'user': 'john'}}
time.sleep(61)  # wait for the cache to expire
print(cache.get("github_api_response"))  # prints: None