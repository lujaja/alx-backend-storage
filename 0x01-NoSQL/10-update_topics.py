#!/usr/bin/env python3
"""
 Change school topics
"""


def update_topics(mongo_collection, name, topics):
    """
    Function - update_topics

    Attributes:
        mongo_collection (pymongo.collection.Collection):
            A pymongo connection object representing a MongoDB collection.
        name (str):
            The name of the school to update.
        topics (list):
            A list of topics that the school has.

    Returns:
        The number of documents updated.
    """
    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
