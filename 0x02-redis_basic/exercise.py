#!/usr/bin/env python3
"""
Writing strings to Redis
"""
from redis import Redis
from uuid import uuid4


class Cache:
    """
    Cach class

    Attributes:
        _redis (Redis()): Redis client
    """
    def __init__(self):
        self._redis = Redis()
        self._redis.flushdb()

    def store(self, data):
        """
        store method

        Attributes:
            data (str): data to store
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key
