#!/usr/bin/env python3
"""
LFU caching system
"""

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """
    A lfu caching system.
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
        self.uses = {}

    def put(self, key, item):
        """
        assign to self.cache_data the item value for the key key.
        if number of items in cache is higher that BaseCaching.MAX_ITEMS:
          discard the least frequently used item put in cache(LFU)
          if more than 1 item to discard, use LRU
          print DISCARD with the discarded key
        """
        if key is not None and item is not None:
            if (len(self.keys) == BaseCaching.MAX_ITEMS
                    and key not in self.keys):
                discard = self.keys.pop(self.keys.index(self.findLFU()))
                del self.cache_data[discard]
                del self.uses[discard]
                print(f'DISCARD: {discard}')
            self.cache_data[key] = item
            if key not in self.keys:
                self.keys.append(key)
                self.uses[key] = 0
            else:
                self.keys.append(self.keys.pop(self.keys.index(key)))
                self.uses[key] += 1

    def get(self, key):
        """
        Returns value in 'key' of cache
        """
        if key is not None and key in self.cache_data:
            self.keys.append(self.keys.pop(self.keys.index(key)))
            self.uses[key] += 1
            return self.cache_data[key]

    def findLFU(self):
        """
        returns least frequently used item key
        If more than 1 item if found, use lru
        """
        items = list(self.uses.items())
        freq = [item[1] for item in items]
        least = min(freq)
        lfu = [item[0] for item in items if item[1] == least]
        for key in self.keys:
            if key in lfu:
                return key
