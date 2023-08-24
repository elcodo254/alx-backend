#!/usr/bin/env python3
"""
LRU caching system
"""

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """
    A lru caching system.
    Attributes:
      __init__ - initializes class instance
      put - method that adds a key/value pair to cache
      get - method that retrieves a key/value pair from cache
    """

    def __init__(self):
        """
        initialize class instance
        """
        super().__init__()
        self.keys = []

    def put(self, key, item):
        """
        assign to self.cache_data the item value for the key key.
        if number of items in cache is higher that BaseCaching.MAX_ITEMS:
          discard the least recently used item put in cache(LRU)
          print DISCARD with the discarded key
        """
        if key is not None and item is not None:
            self.cache_data[key] = item
            if key not in self.keys:
                self.keys.append(key)
            else:
                self.keys.append(self.keys.pop(self.keys.index(key)))
            if len(self.keys) > BaseCaching.MAX_ITEMS:
                discard = self.keys.pop(0)
                del self.cache_data[discard]
                print(f'DISCARD: {discard}')

    def get(self, key):
        """
        Returns value in 'key' of cache
        """
        if key is not None and key in self.cache_data:
            self.keys.append(self.keys.pop(self.keys.index(key)))
            return self.cache_data[key]
