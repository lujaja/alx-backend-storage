#!/usr/bin/env python3
"""
 Where can I learn Python?
"""


def schools_by_topic(mongo_collection, topic):
    """
    Function - schools_by_topic

    Attributes:
        mongo_collection (pymongo.collection.Collection):
            A pymongo connection object representing a MongoDB collection.
        topic (str):
            The name of the topic to search for.
    """
    return mongo_collection.find({"topics": topic})
