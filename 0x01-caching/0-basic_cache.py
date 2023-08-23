#!/usr/bin/env python3
"""
A caching system
"""

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """
    caching system that inherits from baseCaching.
    Attributes:
      put - method that adds a key/value pair to cache
      get - method that retrieves a key/value pair from cache
    """

    def put(self, key, item):
        """
        adds key/value pair to cache.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Returns value in 'key' of cache
        """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
