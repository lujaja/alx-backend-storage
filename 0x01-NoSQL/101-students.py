#!/usr/bin/env python3
"""
Top Students
"""


def top_students(mongo_collection):
    """
    Function - top_students

    Attributes:
        mongo_collection (pymongo.collection.Collection):

    Returns:
        list
    """
    return mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ])
