#!/usr/bin/env python3
"""
Writing strings to Redis
"""
from redis import Redis
from uuid import uuid4
from typing import Union


class Cache:
    """
    Cach class

    Attributes:
        _redis (Redis()): Redis client
    """
    def __init__(self) -> None:
        """
        __init__ method
        """
        self._redis = Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store method

        Attributes:
            data (str): data to store
        """
        # Use Redis's PIPELINE feature to store data
        # in a single write operation
        key = str(uuid4())
        pipeline = self._redis.pipeline()
        pipeline.set(key, data)
        pipeline.execute()
        return key
