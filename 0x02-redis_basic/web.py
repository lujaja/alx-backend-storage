#!/usr/bin/env python3
"""
Web Caching
"""
import requests
import redis
from typing import Callable

r = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    def wrapper(*args, **kwargs):
        key = f"count:{args[0]}"
        r.incr(key)
        return method(*args, **kwargs)

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    Fetch the HTML content of the given URL and cache it
     in Redis with an expiration time.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    url = """
    http://slowwly.robertomurray.co.uk/delay/3000/url/https://www.example.com
    """
    cache_key = f"cached:{url}"
    cached_page = r.get(cache_key)

    if cached_page:
        return cached_page.decode('utf-8')

    response = requests.get(url)
    html_content = response.text

    r.setex(cache_key, 10, html_content)

    return html_content
