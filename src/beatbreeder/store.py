import threading
import uuid

from cachetools import TTLCache

from .evolution_types import Generation


class SolutionStore:
    def __init__(self, maxsize: int = 10000, ttl: float = 3600):
        self._cache: TTLCache[str, Generation] = TTLCache[str, Generation](maxsize=maxsize, ttl=ttl)
        self._lock: threading.Lock = threading.Lock() # Lock needed because flask is multithreaded

    def add(self, genotype: Generation) -> str:
        gid = uuid.uuid4().hex
        with self._lock:
            self._cache[gid] = genotype
        return gid

    def get(self, gid: str) -> Generation | None:
        with self._lock:
            return self._cache.get(gid)

# Singleton pattern in python
store = SolutionStore()
