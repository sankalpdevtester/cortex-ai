import redis
from typing import Any

class LLMCache:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def set(self, key: str, value: Any):
        self.redis_client.set(key, value)

    def get(self, key: str):
        return self.redis_client.get(key)

    def delete(self, key: str):
        self.redis_client.delete(key)