#!/usr/bin/env python3
"""
List all documents in Python
"""
import pymongo
from typing import List


def list_all(
        mongo_collection: 'pymongo.collection.Collection'
) -> List['dict']:
    """
    List all documents in a MongoDB collection.

    Attributes:
        mongo_collection (pymongo.collection.Collection):
            A pymongo connection object representing a MongoDB collection.

    Returns:
        List[dict]: List of all documents in the collection.
    """
    if mongo_collection.count_documents({}) == 0:
        return []
    return list(mongo_collection.find())
