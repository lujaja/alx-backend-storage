#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Count calls decorator
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    Cach class

    Attributes:
        _redis (Redis()): Redis client
    """
    def __init__(self) -> None:
        """
        Initialize Redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store method

        Attributes:
            data (str): data to store
        """
        key: str = str(uuid4())
        pipeline = self._redis.pipeline()
        pipeline.set(key, data)
        pipeline.execute()
        return (key)

    def get(
            self,
            key: str,
            fn: Optional[Callable[[str], Union[str, bytes, int, float]]] = None
    ) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis

        Args:
            key (str): Key to retrieve
            fn (Optional[Callable[[str], Union[str, bytes, int, float]]],
            optional): Function to apply to value if exists. Defaults to None.

        Returns:
            Optional[Union[str, bytes, int, float]]: Value stored at key or
              None if key does not exist
        """
        value = self._redis.get(key)
        if value is None:
            return None
        return (fn(value) if fn else value)

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve string from Redis

        Args:
            key (str): Key to retrieve

        Returns:
            Optional[str]: Value stored at key or None if key does not exist
        """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve integer from Redis

        Args:
            key (str): Key to retrieve

        Returns:
            Optional[int]: Value stored at key or None if key does not exist
        """
        return self.get(key, lambda x: int(x))
