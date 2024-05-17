#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def replay(method: Callable):
    """
    Display the history of calls of a particular function.

    Args:
        method (Callable): The function to replay the history for.
    """
    self = method.__self__
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    inputs = self._redis.lrange(inputs_key, 0, -1)
    outputs = self._redis.lrange(outputs_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input, output in zip(inputs, outputs):
        print(
            f"{method.__qualname__}(*{input.decode('utf-8')}) -> "
            f"{output.decode('utf-8')}"
        )


def count_calls(method: Callable) -> Callable:
    """
    Count calls decorator
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Call history decorator
    """
    @wraps(method)
    def wrapper(self, *args):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(inputs_key, str(args))

        output = method(self, *args)

        self._redis.rpush(outputs_key, str(output))
        return str(output)

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

    @call_history
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
