import threading
import uuid

from cachetools import TTLCache

from .genetic_algorithms.genetic_algorithm import GA


class GAStore:
    def __init__(self, maxsize: int = 10000, ttl: float = 3600):
        self._cache: TTLCache[str, GA] = TTLCache[str, GA](maxsize=maxsize, ttl=ttl)
        self._lock: threading.Lock = threading.Lock() # Lock needed because flask is multithreaded

    def add(self, ga: GA) -> str:
        gid = uuid.uuid4().hex
        with self._lock:
            self._cache[gid] = ga
        return gid

    def get(self, gid: str) -> GA | None:
        with self._lock:
            ga = self._cache.get(gid)
            if ga is not None:
                self._cache[gid] = ga  # Refresh TTL so active sessions don't expire
            return ga

# Singleton pattern in python
store = GAStore()
