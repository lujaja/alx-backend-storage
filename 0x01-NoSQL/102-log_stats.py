#!/usr/bin/env python3
"""
Log stats - New version
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

    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("{} logs".format(total_logs))
    print("Methods:")
    for method in methods:
        print("\tmethod {}: {}".format(method, method_counts[method]))
    print("{} status check".format(status_check_count))

    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")
