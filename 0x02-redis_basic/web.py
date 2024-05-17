import requests
from cachetools import TTLCache, cached
from functools import wraps

# Initialize a cache with expiration time of 10 seconds
cache = TTLCache(maxsize=100, ttl=10)

def get_page(url: str) -> str:
    # Check if the URL is in the cache
    if url in cache:
        # If URL is in cache, return the cached content
        return cache[url]

    # If URL is not in cache, fetch the content using requests
    response = requests.get(url)
    content = response.text

    # Store the content in the cache with the URL as key
    cache[url] = content

    return content

def cache_decorator(func):
    @wraps(func)
    @cached(cache) # Use cachetools cached decorator to handle caching
    def wrapper(url):
        return func(url)
    return wrapper

@cache_decorator
def get_page_with_cache(url: str) -> str:
    response = requests.get(url)
    return response.text
