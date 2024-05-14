#!/usr/bin/env python3
"""
Log stats
"""
from pymongo import MongoClient


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

print(f"{total_logs} logs")
print("Methods:")
for method in methods:
    print(f"\tmethod {method}: {method_counts[method]}")
print(f"{status_check_count} status check")
