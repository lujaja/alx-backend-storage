#!/usr/bin/env python3
"""
Log stats
"""
from pymongo import MongoClient


if __name__ == '__main__':
    """
    provide some stats about nginx logs
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    collection = db.nginx
    total_logs = collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    method_counts = {
        method: collection.count_documents(
            {"method": method}
        ) for method in methods
    }

    status_check_count = collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print("{} logs".format(total_logs))
    print("Methods:")
    for method in methods:
        print("\tmethod {}: {}".format(method, method_counts[method]))
    print("{} status check".format(status_check_count))
    client.close()
