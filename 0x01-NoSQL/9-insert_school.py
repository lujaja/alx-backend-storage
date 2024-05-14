#!/usr/bin/env python3
"""
Insert a document in Python
"""

import pymongo


def insert_school(
        mongo_collection: 'pymongo.collection.Collection', **kwargs: 'dict'
) -> 'pymongo.objectid.ObjectId':
    """
    Insert a document in a MongoDB collection.

    Attributes:
        mongo_collection (pymongo.collection.Collection):
            A pymongo connection object representing a MongoDB collection.
        kwargs (dict):
            A dictionary of key-value pairs representing the document to -
              insert.

    Returns:
        ObjectId:
            The ObjectId of the inserted document.
    """
    return mongo_collection.insert(kwargs)
