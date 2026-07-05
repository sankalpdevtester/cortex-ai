import time
from typing import Any, Dict, Optional

class Cache:
    def __init__(self, ttl: int = 60):
        """
        Initialize the cache with a time-to-live (TTL) value.

        Args:
        - ttl (int): The time-to-live value in seconds. Defaults to 60 seconds.
        """
        self.cache: Dict[str, Any] = {}
        self.ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Args:
        - key (str): The key to retrieve from the cache.

        Returns:
        - The cached value if it exists and is not expired, otherwise None.
        """
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache.

        Args:
        - key (str): The key to store in the cache.
        - value (Any): The value to store in the cache.
        """
        expiry = time.time() + self.ttl
        self.cache[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache.

        Args:
        - key (str): The key to delete from the cache.
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
    Get the cache instance.

    Returns:
    - The cache instance.
    """
    return Cache()


def cache_api_response(ttl: int = 60):
    """
    Decorator to cache API responses.

    Args:
    - ttl (int): The time-to-live value in seconds. Defaults to 60 seconds.
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
@cache_api_response(ttl=30)
def fetch_github_data(owner: str, repo: str) -> Dict:
    # Simulate an API call to GitHub
    time.sleep(2)
    return {"owner": owner, "repo": repo}

# Test the cache
cache = get_cache()
print(cache.get("test_key"))  # Should print None
cache.set("test_key", "test_value")
print(cache.get("test_key"))  # Should print "test_value"
cache.delete("test_key")
print(cache.get("test_key"))  # Should print None

# Test the cache decorator
print(fetch_github_data("octocat", "hello-world"))  # Should print the response and cache it
print(fetch_github_data("octocat", "hello-world"))  # Should print the cached response