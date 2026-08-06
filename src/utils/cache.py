import time
from typing import Any, Dict, Optional
from collections import OrderedDict

class Cache:
    def __init__(self, ttl: int = 60):
        """
        Initialize the cache with a time-to-live (TTL) value.

        Args:
        ttl (int): The time-to-live value in seconds. Defaults to 60.
        """
        self.ttl = ttl
        self.cache: Dict[str, Any] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Args:
        key (str): The key to retrieve.

        Returns:
        Optional[Any]: The cached value if it exists and is not expired, otherwise None.
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
        key (str): The key to store.
        value (Any): The value to store.
        """
        expiry = time.time() + self.ttl
        self.cache[key] = (value, expiry)
        self.cache.move_to_end(key)

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

# Example usage:
cache = get_cache()

def fetch_github_data(repo: str) -> str:
    """
    Fetch GitHub data for a repository.

    Args:
    repo (str): The repository name.

    Returns:
    str: The fetched data.
    """
    # Simulate an API call
    time.sleep(1)
    return f"Data for {repo}"

def get_github_data(repo: str) -> str:
    """
    Get GitHub data for a repository, using the cache if available.

    Args:
    repo (str): The repository name.

    Returns:
    str: The fetched data.
    """
    cached_data = cache.get(repo)
    if cached_data is not None:
        return cached_data
    else:
        data = fetch_github_data(repo)
        cache.set(repo, data)
        return data

# Test the cache
print(get_github_data("facebook/react"))  # Fetches data and caches it
print(get_github_data("facebook/react"))  # Retrieves data from cache
print(get_github_data("google/tensorflow"))  # Fetches data and caches it