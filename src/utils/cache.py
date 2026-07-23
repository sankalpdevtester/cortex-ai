import time
from typing import Any, Dict

class Cache:
    def __init__(self, ttl: int = 60):
        """
        Initialize the cache with a time-to-live (TTL) value.

        Args:
        ttl (int): The time-to-live value in seconds. Defaults to 60.
        """
        self.cache: Dict[str, Any] = {}
        self.ttl = ttl

    def get(self, key: str) -> Any:
        """
        Get a value from the cache.

        Args:
        key (str): The key to retrieve from the cache.

        Returns:
        Any: The cached value or None if not found or expired.
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
        key (str): The key to store in the cache.
        value (Any): The value to store in the cache.
        """
        expiry = time.time() + self.ttl
        self.cache[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache.

        Args:
        key (str): The key to delete from the cache.
        """
        if key in self.cache:
            del self.cache[key]

def get_cache() -> Cache:
    """
    Get the cache instance.

    Returns:
    Cache: The cache instance.
    """
    return Cache()

# Example usage:
cache = get_cache()

def fetch_openai_api(prompt: str) -> str:
    """
    Fetch the OpenAI API response.

    Args:
    prompt (str): The prompt to send to the OpenAI API.

    Returns:
    str: The OpenAI API response.
    """
    # Simulate an API call
    time.sleep(1)
    return f"Response for {prompt}"

def get_openai_api_response(prompt: str) -> str:
    """
    Get the OpenAI API response from the cache or fetch it if not cached.

    Args:
    prompt (str): The prompt to send to the OpenAI API.

    Returns:
    str: The OpenAI API response.
    """
    cached_response = cache.get(prompt)
    if cached_response:
        return cached_response
    else:
        response = fetch_openai_api(prompt)
        cache.set(prompt, response)
        return response

# Test the cache
print(get_openai_api_response("Hello, World!"))  # Fetches the API response
print(get_openai_api_response("Hello, World!"))  # Retrieves from cache
cache.delete("Hello, World!")
print(get_openai_api_response("Hello, World!"))  # Fetches the API response again