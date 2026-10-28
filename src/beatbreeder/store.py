import threading
import uuid

from cachetools import TTLCache

from .evolution_types import Genotype


class SolutionStore:
    def __init__(self, maxsize: int = 10000, ttl: float = 3600):
        self._cache: TTLCache[str, Genotype] = TTLCache[str, Genotype](maxsize=maxsize, ttl=ttl)
        self._lock: threading.Lock = threading.Lock() # Lock needed because flask is multithreaded

    def add(self, genotype: Genotype) -> str:
        id = uuid.uuid4().hex
        with self._lock:
            self._cache[id] = genotype
        return id

    def get(self, id: str) -> Genotype:
        with self._lock:
            return self._cache[id]

store = SolutionStore()
